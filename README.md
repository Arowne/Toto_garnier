# TOTO House plan generator

[![N|Solid](assets/logo.png)]()

TOTO is floor plan generator that allow you to generate 2D floor plan easily importable to blender for 3D modelisation.

# Choose the number of rooms generated !

Toto will generate multiple plan with the choosen number of rooms (3 to 5).

# Choose the size of house !

Toto also allow to choose the size of your size by fill the height and the width of your house.


# Get started

### Required
Make sure you have the following dependence installed:
    Python3
    ,Tensorflow 2.0
    ,Numpy
    ,Matplotlib
    ,PIL/pillow
    ,Sklearn
    
### TOTO ROOM CLASSIFIER

To train TOTO with your data simply put it each type of plan in the ROBIN folder in a categorical subfolder ROBIN/0/ (for 3 room category) , ROBIN/1/ (for 4 room category) to recognize the number of rooms in a plan ...

```
from RoomClassifier import RoomClassifier

room_classifier = RoomClassifier()
room_classifier.train()

```

### TOTO ROOM PREDICTION

Toto also allow you to recognize the type of house you have (by counting number of rooms)

```
from RoomClassifier import RoomClassifier

room_classifier = RoomClassifier()
room_classifier.predict('PREDICTION_FOLDER/', number_of_images, images_height, image_width)

```
# Toto_garnier
