<h1> Respiratory Disease Classifier.</h1>
<br>
## The disease that can be classified are 
<li>Bronchiectasis </li>
<li>Bronchiolitis</li>
<li>COPD</li>
<li>Pneumonia</li>
<li>URTI</li>
<li>Healthy</li>
<br>
The model makes use of audio file recorded via a digital stethoscope.
## Model Architecture.
1. Our model is a Convolutional Neural Network (CNN) using Keras and Tensorflow backend.
2. I have used a sequential model, with a simple model architecture, consisting of four Conv2D convolution layers, with our final output layer being a dense layer.
The convolution layers are designed for feature detection. 
3. It works by sliding a filter window over the input and performing a matrix multiplication and storing the result in a feature map. This operation is known as a convolution.
4. The filter parameter specifies the number of nodes in each layer. 
5. Each layer will increase in size from 16, 32, 64 to 128, while the kernel_size parameter specifies the size of the kernel window which in this case is 2 resulting in a 2x2 filter matrix.
6. The first layer will receive the input shape of (40, 862, 1) where 40 is the number of MFCC's, 862 is the number of frames taking padding into account and the 1 signifying that the audio is mono.
7. The activation function I have used for our convolutional layers is ReLU. I have used a small Dropout value of 20% on our convolutional layers.
8. Each convolutional layer has an associated pooling layer of MaxPooling2D type with the final convolutional layer having a GlobalAveragePooling2D type. 
9. The pooling layer is to reduce the dimensionality of the model (by reducing the parameters and subsequent computation requirements) which serves to shorten the training time and reduce overfitting. 
10. The Max Pooling type takes the  maximum size for each window and the Global Average Pooling type takes the average which is suitable for feeding into our dense output layer.
11. Our output layer will have 6 nodes (num_labels) which matches the number of possible classifications. 
12. The activation for our output layer is softmax. 
13. Softmax makes the output sum up to 1 so the output can be interpreted as probabilities. 
14. The model will then make its prediction based on which option has the highest probability.

## How to get started!
1. Run CMD/terminal and navigate to the folder where requirements.txt is located.
2. Type in "pip install -r requirements.txt" to download the required modules/packages.
3. Before running the project we need to create our .db file
    a. Navigate to the same folder where run.py is present
    b. Open python interpretor on cmd/terminal by typing python.
    c. Run the following commands:
        i. from projectapp.models import User,Audio
        ii. from projectapp import db
        iii. db.create_all()
    d. The above steps will create a site.db wile where are database will be stored.
4. To run the WebApp type in python run.py in cmd/terminal.
5. Open the project in any browser preferably chrome or firefox by navigating to the url displayed in the terminal which is usually localhost:5000 or 127.0.0.1:5000
    
