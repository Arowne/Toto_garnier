import os, sys, uuid
import numpy as np
import cv2
import glob
from PIL import Image
from sklearn.utils import shuffle
import PIL
import random
import time


# from RoomClassifier import RoomClassifier


class GeneratePlan():

    def __init__(self,  rooms_list=[], quantity_list=[], size_list=[]):
        self.rooms_list = rooms_list
        self.quantity_list = quantity_list
        self.size_list = size_list

        self.existing_images = []
        self.layout_list = []
        self.layout_type = []
    
    def create_space_layers(self):

        image_list = []
        rooms_list = self.rooms_list
        size_list = self.size_list
        room_counter = 0
        quantity_list = self.quantity_list
        quantity_list.reverse()

        # Resize image
        for x in range(len(rooms_list)):
            number_of_room_of_current_type = int(quantity_list[x])
            for y in range(number_of_room_of_current_type):
                layout_image = "./ROBIN/module/" + str(rooms_list[x]) + "/" + str(rooms_list[x]) + str(x) + '.jpg'
                src = cv2.imread(layout_image)

                img = cv2.resize(src, tuple(size_list[room_counter]))
                img_path = "./PREDICTION/space_layout/" + str(uuid.uuid1()) + '.jpg'
                cv2.imwrite(img_path, img)

                self.layout_list.append(img_path)
                self.layout_type.append(rooms_list[x])
                room_counter += 1

    def generate_image(self):

        image_names = self.layout_list

        # Get get space layout max width
        max_width = self.get_max_width()
        max_height = self.get_max_height(max_width)
        index = 0

        house = str(
"                             _..-:-.._\n"+
"                      _..--''    :    ``--..\n"
"               _..--''           :           ``--.._\n"+
"           _..-''                :                .'``--.._\n"+
"  _..--'' `.                     :              .'         |\n"+
" |          `.              _.-''|``-._       .'           |\n"+
" |            `.       _.-''     |     ``-._.'       _.-.  |\n"+
" |   |`-._      `._.-''          |  ;._     |    _.-'   |  |\n"+
" |   |    `-._    |     _.-|     |  |  `-.  |   |    _.-'  |  TOTO\n"+
" |_   `-._    |   |    |   |     |  `-._ |  |   |_.-'   _.-'   ..\n"+
"   `-._   `-._|   |    |.  |  _.-'-._   `'  |       _.-'   ..::::::..\n"+
"       `-._       |    |  _|-'  *    `-._   |   _.-'   ..::::::::''\n"+
"           `-._   |   _|-'.::. \|/  *    `-.|.-'   ..::::::::''\n"+
"               `-.|.-' *`:::::::.. \|/  *      ..::::::::''\n"+
"                       \|/  *`:::::::.. \|/ ..::::::::''\n"+
"                           \|/  *`:::::::.::::::::''\n"+
"                               \|/  *`::::::::''\n"+
"                                   \|/  `:''\n"
        )

        print(house)
        bar = [
            "[BUILD                ]",
            "[ BUILD               ]",
            "[  BUILD              ]",
            "[   BUILD             ]",
            "[    BUILD            ]",
            "[     BUILD           ]",
            "[      BUILD          ]",
            "[       BUILD         ]",
            "[        BUILD        ]",
            "[         BUILD       ]",
            "[          BUILD      ]",
            "[           BUILD     ]",
            "[            BUILD    ]",
            "[             BUILD   ]",
            "[              BUILD  ]",
            "[               BUILD ]",
            "[                BUILD]",
            "[                 BUIL]",
        ]

        os.system('touch ./GENERATED/foo && rm ./GENERATED/*')

        for image in image_names:
            for image in image_names:
                print(bar[index % len(bar)], end="\r")
                index += 1
                self.create_plan(max_width, max_height)
        print("\n", end="\r")      
        print(str(len(self.existing_images)) + " plans generated.")
        os.system('http-server "./web/html/" --proxy http://localhost:8080')

    def get_max_width (self):

        image_names = self.layout_list
        image_type = self.layout_type

        max_width = 0
        
        for index, file in enumerate(image_names):
            
            path = os.path.expanduser(file)
            img = Image.open(path)
            w, h = img.size
            
            if w > max_width:
                max_width = w

        return max_width


    def get_max_height(self, max_width):

        image_names = self.layout_list
        image_type = self.layout_type
        
        # Take first layer
        path = os.path.expanduser(image_names[0])
        img = Image.open(path)
        w, h = img.size

        previous_h = h
            
        stage_width = 0
        max_height = h
        
        for index, file in enumerate(image_names):
            
            path = os.path.expanduser(file)
            img = Image.open(path)
            w, h = img.size

            if stage_width + w > max_width:
                max_height += h
                # print(max_height)
                previous_h = h
                stage_width = 0
            else:
                stage_width += w
                if h > previous_h:
                    max_height -= previous_h 
                    max_height += h

        return max_height


    def create_plan(self, max_width, max_height):
        
        result = Image.new('RGB', (1000, 1000), color=(240, 240,0))
        
        images_name = self.layout_list
        images_name = shuffle(images_name)

        path = os.path.expanduser(images_name[0])
        img = Image.open(path)
        w, h = img.size

        x = 0
        y = 0
        current_concat_w = 0
        current_concat_h = 0
        row_h = 0
        row_w = 0
        stage_index = 0

        for index, file in enumerate(images_name):
            
            path = os.path.expanduser(file)
            current_img = Image.open(path)
            w, h = current_img.size
            
            if row_w + w > max_width and index > 0:

                path = os.path.expanduser(images_name[index-1])
                previous_img = Image.open(path)
                previous_w, previous_h = previous_img.size

                row_w = 0
                row_h += previous_h
            
            result.paste(current_img, (row_w, row_h, row_w + w, row_h + h))
            row_w += w
        
        data = np.array(result)
        data[np.where((data>=[240, 240, 0]).all(axis=2))] = (255, 255, 255)
        
        data_list = data.tolist()
        if list(data_list) not in self.existing_images:
            self.existing_images.append(list(data_list))

            result = Image.fromarray(data, mode='RGB')
            
            img_path = "./GENERATED/" + str(uuid.uuid1()) + '.jpg'
            result.save(os.path.expanduser(img_path))
            data = np.array(result)

            data[np.where((data>=[20, 20, 20]).all(axis=2))] = (255, 255, 255)
            data[np.where((data>=[110, 0, 0]).all(axis=2))] = (255, 255, 255)
            data[np.where((data>=[0, 110, 0]).all(axis=2))] = (255, 255, 255)
            data[np.where((data>=[0, 0, 110]).all(axis=2))] = (255, 255, 255)
            data[np.where((data>[10, 10, 10]).all(axis=2))] = (255, 255, 255)
            data = 255 - data
            data = 255 - data
            result = Image.fromarray(data, mode='RGB')
            

            result.save(os.path.expanduser('white-output.png'))
            os.system('convert -channel GRAY white-output.png output.pgm && potrace -s output.pgm && mv output.svg  ./web/html/models/svg/white-output.svg')
            os.system('mv ' + img_path +  ' ./web/html/models/svg/colored-output.png')


    def schema_one(self, total_height, living_room_w, living_room_h, result, number_of_stage):
        image_names = self.layout_list
        image_type = self.layout_type
        
        stage_index = 0
        total_w = -50

        for index, file in enumerate(image_names):
            
            # Living room path
            path = os.path.expanduser(image_names[0])
            img = Image.open(path)
            w, living_room_h = img.size
            room_base = int(total_height/2 - living_room_h/2) + living_room_h
            room_base_negative = int(total_height/2 - living_room_h/2) - living_room_h

            room_base_negative = 0 - int(room_base)

            path = os.path.expanduser(file)
            img = Image.open(path)
            w, h = img.size

            if image_type[index] == 'living_room':
                if number_of_stage >= 1:
                    x = 0
                    y = int(total_height/2 - h/2)
                    room_base = y
                else:
                    x = 0
                    y = 0
                result.paste(img, (x, y, x + w, y + h))
            else:

                # Check if we add stage index for room
                if total_w + w >= living_room_w:
                    stage_index += stage_index + 1
                
                # Concat rooms
                if total_w + w >= living_room_w:
                    x = 0
                    total_w = 0
                else:
                    x = total_w + w
                    total_w = x
                
                print(stage_index)
                if stage_index > 0:
                    y = int(total_height/2) - living_room_h
                else:
                    y = room_base + h * stage_index

                result.paste(img, (x, y, x + w, y + h))
                
        result.save(os.path.expanduser('new.png'))
        data = np.array(result)

        data[np.where((data>=[20, 20, 20]).all(axis=2))] = (255, 255, 255)
        data[np.where((data>=[110, 0, 0]).all(axis=2))] = (255, 255, 255)
        data[np.where((data>=[0, 110, 0]).all(axis=2))] = (255, 255, 255)
        data[np.where((data>=[0, 0, 110]).all(axis=2))] = (255, 255, 255)
        data[np.where((data>[10, 10, 10]).all(axis=2))] = (255, 255, 255)
        data = 255 - data
        data = 255 - data
        result = Image.fromarray(data, mode='RGB')

        result.save(os.path.expanduser('white-output.png'))
        os.system('convert -channel GRAY white-output.png output.pgm && potrace -s output.pgm && mv output.svg  ./web/html/models/svg/white-output.svg')
        os.system('mv new.png  ./web/html/models/svg/colored-output.png')


    # def schema_one(self, total_height, living_room_w, living_room_h, result, number_of_stage):
    #     image_names = self.layout_list
    #     image_type = self.layout_type
        
    #     stage_index = 0
    #     total_w = -50

    #     for index, file in enumerate(image_names):

    #         path = os.path.expanduser(file)
    #         img = Image.open(path)
    #         w, h = img.size

    #         if image_type[index] == 'living_room':
    #             if number_of_stage > 1:
    #                 x = 0
    #                 y = (living_room_h/2 - h/2)
    #             else:
    #                 x = 0
    #                 y = 0
    #             result.paste(img, (x, y, x + w, y + h))
    #         else:

    #             # Check if we add stage index for room
    #             if total_w + w >= living_room_w:
    #                 stage_index += 1
                
    #             # Concat rooms
    #             if total_w + w >= living_room_w:
    #                 x = 0
    #                 total_w = 0
    #             else:
    #                 x = total_w + w
    #                 total_w = x
                
                
    #             y = 0 + living_room_h + h * stage_index

    #             result.paste(img, (x, y, x + w, y + h))

def text_to_list(hashtags):
    return hashtags.strip('[]').replace('\'', '').replace(' ', '').split(',')

# Get design information
def argument_checker():
    argv = sys.argv
    argv.reverse()
    argv.pop()

    rooms_list = []
    quantity_list = []
    size_list = []
    available_type = ['living_room', 'room', 'toilets', 'kitchen', 'bath_room', 'size']

    for arg in argv:
        space_layout_type = arg.split("=")
        if space_layout_type[0] not in available_type:
            print("Error: Space type not recognized")
            exit

        if space_layout_type[0] == "size":
            get_size_list = text_to_list(space_layout_type[1])
            for room_size in get_size_list:
                room_size = room_size.split('x')
                room_size = (int(room_size[0]), int(room_size[1]))
                size_list.append(room_size)
        else:            
            rooms_list.append(space_layout_type[0])  
            quantity_list.append(space_layout_type[1])

    rooms_list.reverse()
    return (rooms_list, quantity_list, size_list)

if __name__ == "__main__":
    # Get command line argument
    rooms_list, quantity_list, size_list = argument_checker()
    plan = GeneratePlan(rooms_list=rooms_list, quantity_list=quantity_list, size_list=size_list)
    plan.create_space_layers()
    plan.generate_image()
    pass
    