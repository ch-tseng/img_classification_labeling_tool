# -*- coding: utf-8 -*-
import os
import easygui, imutils
import cv2

class_file = "datasets/human/class_map.txt"
ds_path = "datasets/human"
img_display_size = (180, 280)

#-----------------------------------------------------------------------
ds_images_path = os.path.join(ds_path, 'images')
ds_labels_path = os.path.join(ds_path, 'labels')

d_classes, t_classes = [], []
classes_def = {}
with  open(class_file, 'r', encoding="utf-8") as fp:
    id = 0
    for line in fp:
        line = line.replace('\n','')
        d1, d2, txt_classes = line.split(',')

        display_classes = d1.split('/')
        map_classes = d2.split('/')

        for cid, class_name in enumerate(display_classes):
            classes_def.update( { str(id)+'_'+class_name:map_classes[cid] } )            

        d_classes.append(display_classes)
        t_classes.append(txt_classes)

        id+=1

print(classes_def)

for id, file in enumerate(os.listdir(ds_images_path)):
    file_path = os.path.join(ds_images_path, file)

    if(os.path.isfile(file_path)):
        filename, file_extension = os.path.splitext(file)

        if(file_extension.lower() in ('.jpg', '.png', '.jpeg')):
            img = cv2.imread(file_path)
            img_display = imutils.resize(img, height=img_display_size[1])
            if(img_display.shape[1]>img_display_size[0]):
                img_display = imutils.resize(img_display, width=img_display_size[0])

            cv2.imwrite("tmp.jpg", img_display)

            answers = []
            for q_id, question in enumerate(d_classes):
                #choice = easygui.choicebox(msg, title, choices)
                reply = easygui.buttonbox(image="tmp.jpg", title=t_classes[q_id], choices=d_classes[q_id])
                map_class_id = classes_def[str(q_id)+"_"+reply]
                print("Select:", reply, map_class_id)
                answers.append(map_class_id)

            img_class_file = os.path.join(ds_labels_path, filename+'.txt')
            with open(img_class_file, 'w') as fp:
                for i, ans in enumerate(answers):
                    if(i>0): fp.write(',')
                    fp.write(ans)
