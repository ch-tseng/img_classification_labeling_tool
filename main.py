# -*- coding: utf-8 -*-
import os, sys
import easygui, imutils
import cv2

class_file = "human_class_map.txt" #分類的各項設定, 可針對不同dataset有不同的設定檔
img_source = "H:/Dataset/Mine/Human/Human_sex/female/"  #需要分類的影像path
target_ds_path = "output_dataset/"  #分類結果(包含image及分類txt檔)要放置的位置 (此資料夾會自動create)
img_display_size = (240, 360)  #分類時, 圖片顯示的大小 (寬,長)

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

def statics():
    global classes_count

    for class_name in classes_count:
        classes_count.update( {class_name:0} )

    for file in os.listdir(ds_images_path):
        filename, file_extension = os.path.splitext(file)
        txtfile = os.path.join(ds_labels_path, filename+'.txt')
        if(os.path.exists(txtfile)):
            with  open(txtfile, 'r', encoding="utf-8") as fp:
                for line in fp:
                    line = line.strip()
                    line = line.replace('\n','')
                    dataline = line.split(',')
                    #print(txtfile,  "DATA", dataline)
                    for id, data in enumerate(dataline):
                        name_data = str(id)+'_'+str(data)

                        try:
                            counts = classes_count[name_data]+1
                        except:
                            print(txtfile, "有問題.")

                        classes_count.update( { str(id)+'_'+str(data):counts } )


    last_data1, line_sta = '0', ''
    print('==============================================================================================')
    for id_name in classes_count:
        data1, data2 = id_name.split('_')
        if(last_data1!=data1):
            print(line_sta)
            print('--------------------------------------------------------------------------------------------------')
            line_sta = ''
        
        string = all_classes[id_name] + ':' + str(classes_count[id_name])
        if(len(string)>8): length = len(string)
        line_sta += string.center(8,' ')

        last_data1 = data1



def label_win(file):
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
                    if("*上張" not in question):
                        question.append("*上張")                    
                    if("*跳過" not in question):
                        question.append("*跳過")
                    if("*刪除" not in question):
                        question.append("*刪除")
                    if("*結束" not in question):
                        question.append("*結束")

                    reply = easygui.buttonbox(image="tmp.jpg", title=t_classes[q_id]+':'+file, choices=question)


                    if(reply not in ["*上張", "*跳過", "*刪除", "*結束"]):
                        map_class_id = classes_def[str(q_id)+"_"+reply]                        
                        answers.append(map_class_id)
                        txt_inform += t_classes[q_id]+': '+reply + '\n'                        

                    else:
                        if(reply=="*結束"):
                            sys.exit(0)                        

                        elif(reply=="*刪除"):
                            print("delete the image file", file_path)
                            os.rename(file_path, os.path.join(ds_deleted_path,file))

                        elif(reply=="*上張"):
                            return -1

                        return 0
                
                #print(file_path, answers)
                if(reply not in ["*跳過", "*刪除", "*結束"]):

                    confirm = easygui.boolbox(image="tmp.jpg", msg="下方資訊是否正確?\n"+txt_inform, 
                        title=t_classes[q_id]+':'+file, choices=["正確", "不正確"])

                    if(confirm):
                        with open(img_class_file, 'w') as fp:
                            for i, ans in enumerate(answers):
                                if(i>0): fp.write(',')
                                fp.write(ans)

                        cv2.imwrite(os.path.join(ds_images_path,filename+'.jpg'), img)
                        statics()

d_classes, t_classes, all_classes, classes_count = [], [], {}, {}
classes_def = {}
with  open(class_file, 'r', encoding="utf-8") as fp:
    id, id_line = 0, 0
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
            all_classes.update( { str(id_line)+'_'+str(cid):class_name } )
            classes_count.update( {str(id_line)+'_'+str(cid):0} )
            try:
                classes_def.update( { str(id)+'_'+class_name:map_classes[cid].strip() } )            
            except:
                easygui.msgbox("設定檔的對應格式不對, 請檢查此行:\n  {}".format(txt_classes), "載入設定檔")
                sys.exit(0)

        d_classes.append(display_classes)
        t_classes.append(txt_classes)

        id+=1
        id_line += 1


filelist = os.listdir(img_source)
i = 0

#for file in filelist:
while True:
    
    file = filelist[i]
    rtn = label_win(file)

    if(rtn==-1):        
        i = i-1
        if(i<0): i = 0
    else:
        i += 1
        if(i > (len(filelist)-1)): i = len(filelist)-1

