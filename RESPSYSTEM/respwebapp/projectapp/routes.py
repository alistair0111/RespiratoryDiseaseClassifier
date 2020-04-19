import secrets
import os
from PIL import Image
from projectapp.models import User, Audio
from projectapp import app, bcrypt, db
from flask import Flask, render_template, url_for, request, flash, redirect
from projectapp.forms import RegistrationForm, LoginForm, FileForm, UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required


from os import listdir
import librosa
import numpy as np
from tensorflow.keras.models import load_model

def extract_features(file_name):
    try:
            max_pad_len = 862
            audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast', duration=20) 
            mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
            pad_width = max_pad_len - mfccs.shape[1]
            mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
    except Exception as e:
            print("Error encountered while parsing file: ", file_name)
            return None
    return mfccs


ALLOWED_EXTENSIONS = set(['wav'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


def save_audio(form_audio):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_audio.filename)
    audio_fn = random_hex + f_ext
    audio_path = os.path.join(app.root_path,'static/audio',audio_fn)
    form_audio.save(audio_path)
    return audio_path,audio_fn


@app.route('/prediction_page',methods=['GET','POST'])
@login_required
def prediction_page():
    form = FileForm()
    if request.method=='POST':
        audio_filepath,audio_fn = save_audio(form.audio.data)
        data = extract_features(audio_filepath)
        modelfn =  os.path.join(app.root_path,'mymodel2_268.h5')
        model=load_model(modelfn)
        np.set_printoptions(suppress=True)
        data = data.reshape([1,40,862,1])
        pred = model.predict([data])
        print(pred)
        c_names = ['Bronchiectasis', 'Bronchiolitis', 'COPD', 'Healthy', 'Pneumonia', 'URTI']
        index = np.argmax(pred)
        print(index)
        result = c_names[index]
        audio_db = Audio(audio = audio_fn, classification = result, user_id=current_user.id)
        db.session.add(audio_db)
        db.session.commit()
        return render_template('prediction_page.html', form=form, title='Classifier', result=result)
    else:
        return render_template('prediction_page.html', form=form, title='Classifier')




def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pic',picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn



@app.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email 
    image_file = url_for('static', filename='profile_pic/'+current_user.image_file)
    return render_template('profile.html', title='Profile', form=form, image_file=image_file)


@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created For {form.username.data}!','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register', form=form)


@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Login Successful. Welcome {user.username}','success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login unsuccessful. Please check email and password!','danger')
    return render_template('login.html',title='Login', form=form)


@app.route('/record',methods=['GET','POST'])
@login_required
def record():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    print(user)
    print(current_user.id)
    records = Audio.query.filter_by(user_id=current_user.id)\
        .order_by(Audio.record_date.desc())
    count_rec = Audio.query.filter_by(user_id=current_user.id)\
        .order_by(Audio.record_date.desc()).count()
    print(count_rec)
    return render_template('record.html',records=records, title=current_user.username, user=user, count_rec=count_rec)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
