from django.shortcuts import render
from django.http import HttpResponse

from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import pickle
from django.core.files.storage import FileSystemStorage
from shell.models import *

def home(request):
    


    return render(request, 'shell/home.html')

def details(request):
    

    def predict(image_path):
        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

        # Load the model
        model = load_model("./savedmodels/keras_model.h5", compile=False)

        # Load the labels
        class_names = open("./savedmodels/labels.txt", "r").readlines()

        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # Replace this with the path to your image
        image = Image.open(image_path).convert("RGB")

        # resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.LANCZOS)

        # turn the image into a numpy array
        image_array = np.asarray(image)

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # Predicts the model
        prediction = model.predict(data)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        #Print prediction and confidence score
        print("Class:", class_name[2:], end="")
        print("Confidence Score:", confidence_score)
        return index;
    
    x = 0
    def result(image_path):
         x = predict(image_path)
         if x == 0:
            return True;
         else:
             return False;

    p = result('./media/images/download.jpeg');
    print(p)
     
    
    person= {'building': p, 'val': x}
    item_list = {"Chocolate": 4, "Pen": 10, "Pencil": 3}
    order_number= "000132342"
    context= {
        'person': person,
        'item_list': item_list,
        'order_number': order_number,
        'current_date': 44,
        }
    

    return render(request, 'shell/details.html', context)



def upload(request):
    print("request handleling .......")
    pic = request.FILES['image']
    shellImage = Shell(pic = pic)
    shellImage.save()
    return render(request, 'shell/home.html')