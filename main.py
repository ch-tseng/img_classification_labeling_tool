<<<<<<< HEAD
# -*- coding: utf-8 -*-
import os, sys
import easygui, imutils
import cv2

class_file = "datasets/human/class_map.txt"
img_source = "D:/temp2/Human_sex/male/"
target_ds_path = "D:/temp2/Human_sex/"
img_display_size = (240, 360)

#-----------------------------------------------------------------------
ds_images_path = os.path.join(target_ds_path, 'images')
ds_labels_path = os.path.join(target_ds_path, 'labels')
ds_deleted_path = os.path.join(target_ds_path, 'deleted')

if not os.path.exists(ds_images_path):
    os.makedirs(ds_images_path)
if not os.path.exists(ds_labels_path):
    os.makedirs(ds_labels_path)
if not os.path.exists(ds_deleted_path):
    os.makedirs(ds_deleted_path)

d_classes, t_classes = [], []
classes_def = {}
with  open(class_file, 'r', encoding="utf-8") as fp:
    id = 0
    for line in fp:        
        line = line.replace('\n','').strip()
        if(line[0:1]=='#'):
            continue
            
        try:
            d1, d2, txt_classes = line.split('|')
        except:
            easygui.msgbox("設定檔的對應格式不對, 每行應有3個|分隔字元.")
            sys.exit(0)

        display_classes = d1.split('/')
        map_classes = d2.split('/')      

        for cid, class_name in enumerate(display_classes):
            class_name = class_name.strip()
            display_classes[cid] = class_name
            try:
                classes_def.update( { str(id)+'_'+class_name:map_classes[cid].strip() } )            
            except:
                easygui.msgbox("設定檔的對應格式不對, 請檢查此行:\n  {}".format(txt_classes), "載入設定檔")
                sys.exit(0)

        d_classes.append(display_classes)
        t_classes.append(txt_classes)

        id+=1

print(classes_def)

for id, file in enumerate(os.listdir(img_source)):
    file_path = os.path.join(img_source, file)

    if(os.path.isfile(file_path)):
        filename, file_extension = os.path.splitext(file)

        if(file_extension.lower() in ('.jpg', '.png', '.jpeg')):
            img_class_file = os.path.join(ds_labels_path, filename+'.txt')
            if(not os.path.isfile(img_class_file)):
                img = cv2.imread(file_path)
                img_display = imutils.resize(img, height=img_display_size[1])
                if(img_display.shape[1]>img_display_size[0]):
                    img_display = imutils.resize(img_display, width=img_display_size[0])

                cv2.imwrite("tmp.jpg", img_display)

                answers = []
                txt_inform = ""
                for q_id, question in enumerate(d_classes):

                    #choice = easygui.choicebox(msg, title, choices)
                    if("*Skip" not in question):
                        question.append("*Skip")
                    if("*Delete" not in question):
                        question.append("*Delete")

                    reply = easygui.buttonbox(image="tmp.jpg", title=t_classes[q_id]+':'+file, choices=question)

                    if(reply not in ["*Skip", "*Delete"]):
                        map_class_id = classes_def[str(q_id)+"_"+reply]                        
                        answers.append(map_class_id)
                        txt_inform += t_classes[q_id]+': '+reply + '\n'
                    else:
                        if(reply=="*Delete"):
                            print("delete the image file", file_path)
                            os.rename(file_path, os.path.join(ds_deleted_path,file))

                        break
                
                print(file_path, answers)
                if(reply not in ["*Skip", "*Delete"]):

                    confirm = easygui.boolbox(image="tmp.jpg", msg="下方資訊是否正確?\n"+txt_inform, 
                        title=t_classes[q_id]+':'+file, choices=["正確", "不正確"])

                    if(confirm):
                        with open(img_class_file, 'w') as fp:
                            for i, ans in enumerate(answers):
                                if(i>0): fp.write(',')
                                fp.write(ans)

                        cv2.imwrite(os.path.join(ds_images_path,filename+'.jpg'), img)

=======
# -*- coding: utf-8 -*-
import os
import easygui, imutils
import cv2

class_file = "datasets/human/class_map.txt"
img_source = "D:/temp2/Human_sex/male/"
target_ds_path = "D:/temp2/Human_sex/"
img_display_size = (240, 360)

#-----------------------------------------------------------------------
ds_images_path = os.path.join(target_ds_path, 'images')
ds_labels_path = os.path.join(target_ds_path, 'labels')

if not os.path.exists(ds_images_path):
    os.makedirs(ds_images_path)
if not os.path.exists(ds_labels_path):
    os.makedirs(ds_labels_path)

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

for id, file in enumerate(os.listdir(img_source)):
    file_path = os.path.join(img_source, file)

    if(os.path.isfile(file_path)):
        filename, file_extension = os.path.splitext(file)

        if(file_extension.lower() in ('.jpg', '.png', '.jpeg')):
            img_class_file = os.path.join(ds_labels_path, filename+'.txt')
            if(not os.path.isfile(img_class_file)):
                img = cv2.imread(file_path)
                img_display = imutils.resize(img, height=img_display_size[1])
                if(img_display.shape[1]>img_display_size[0]):
                    img_display = imutils.resize(img_display, width=img_display_size[0])

                cv2.imwrite("tmp.jpg", img_display)

                answers = []
                txt_inform = ""
                for q_id, question in enumerate(d_classes):
                    #choice = easygui.choicebox(msg, title, choices)
                    if("*Skip" not in question):
                        question.append("*Skip")
                    if("*Delete" not in question):
                        question.append("*Delete")

                    reply = easygui.buttonbox(image="tmp.jpg", title=t_classes[q_id]+':'+file, choices=question)

                    if(reply not in ["*Skip", "*Delete"]):
                        map_class_id = classes_def[str(q_id)+"_"+reply]                        
                        answers.append(map_class_id)
                        txt_inform += t_classes[q_id]+': '+reply + '\n'
                    else:
                        if(reply=="*Delete"):
                            print("delete the image file", file_path)
                            os.remove(file_path)

                        break
                
                print(file_path, answers)
                if(reply not in ["*Skip", "*Delete"]):

                    confirm = easygui.boolbox(image="tmp.jpg", msg="下方資訊是否正確?\n"+txt_inform, 
                        title=t_classes[q_id]+':'+file, choices=["正確", "不正確"])

                    if(confirm):
                        with open(img_class_file, 'w') as fp:
                            for i, ans in enumerate(answers):
                                if(i>0): fp.write(',')
                                fp.write(ans)

                        cv2.imwrite(os.path.join(ds_images_path,filename+'.jpg'), img)

>>>>>>> 3ee75420cdb6d6a8af7592fed912fc50c8d25f46
