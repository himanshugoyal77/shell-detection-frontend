from django.shortcuts import render
from django.http import HttpResponse

from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import pickle
from django.core.files.storage import FileSystemStorage
from shell.models import *
import os

def home(request):
    return render(request, 'shell/home.html')

def details(request):
    #upload(request)
    c_name = "None"
    c_score = 0

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
        c_name = class_name[2:]
        print("Confidence Score:", confidence_score)
        c_score = confidence_score
        return [confidence_score, class_name[2:], index];
    
    x = 0
    def result(image_path):
         xx = predict(image_path)
         x = xx[2]
         if x == 0:
            return True;
         else:
             return False;

    p = result('./media/images/build.jpg');
    print(p)

    print('lemon')
    op = predict('./media/images/build.jpg')
    l = op[0] * 100
    c_name = op[1]
     
    
    person= {'isBuilding': p, 'val': x, 'cname': c_name, 'cscore': l}
    item_list = {"Chocolate": 4, "Pen": 10, "Pencil": 3}
    order_number= "000132342"
    context= {
        'person': person,
        'item_list': item_list,
        'order_number': order_number,
        'current_date': 44,
        }
    

    return render(request, 'shell/details.html', context)

def rename(oldname):
    print(f"./media/images/{oldname}")
    os.rename(f"./media/images/{oldname}", './media/images/build.jpg')

def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)

def upload(request):
    print("request handleling .......")
    _delete_file('./media/images/build.jpg')
    pic = request.FILES['image']
    #print(pic)
    shellImage = Shell(pic = pic)
    shellImage.save()
    rename(pic)
    
    return render(request, 'shell/details.html')