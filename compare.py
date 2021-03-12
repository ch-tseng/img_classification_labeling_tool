# img_viewer.py

import PySimpleGUI as sg
import os.path, io, re
from PIL import Image
import codecs

width_space = 20

d_classes, t_classes, all_classes, classes_count = [], [], {}, {}
path_user_works, path_img_dataset = '', ''
users_lbl_content, users_lbl_list = {}, []
#--------------------------------------------------------------------------------------------------

def load_class_file(class_file):
    global d_classes, t_classes, all_classes

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
                sg.popup_ok("設定檔的對應格式不對, 每行應有3個|分隔字元.", title='發生錯誤', keep_on_top=True)
                return
            
            display_classes = d1.split('/')
            map_classes = d2.split('/')      

            for cid, class_name in enumerate(display_classes):
                class_name = class_name.strip()
                display_classes[cid] = class_name
                all_classes.update( { str(id_line)+'_'+str(cid):class_name } )
                try:
                    classes_def.update( { str(id)+'_'+class_name:map_classes[cid].strip() } )            
                except:
                    sg.popup_ok("設定檔的對應格式不對, 請檢查此行:\n  {}".format(txt_classes), title='發生錯誤', keep_on_top=True)
                    return

            d_classes.append(display_classes)
            t_classes.append(txt_classes)

            id+=1
            id_line += 1

def get_label(img_file):
    globalusers_lbl_content, users_lbl_list = {}, []

    filename, file_extension = os.path.splitext(img_file)
    path_img = os.path.join(path_img_dataset, img_file)
    path_lbl = None

    if(os.path.exists(path_img)):
        for folder in os.listdir(path_user_works):
            path_user= os.path.join(path_user_works, folder)
            path_user_lbl = os.path.join(path_user, filename+'.txt')

            if(os.path.exists(path_user_lbl)):
                with  open(path_user_lbl, 'r', encoding="utf-8") as fp:
                    for line in fp:
                        line = line.strip()
                        line = line.replace('\n','')
                        dataline = line.split(',')
                        class_names = list2name(dataline)

            else:
                dataline = None
                class_names = None

            users_lbl_content.update( {folder:[path_user_lbl, class_names]} )
            users_lbl_list.append(dataline)


    return users_lbl_content, users_lbl_list 

def compare_labels(datas): #datas: [ [data1, data2, data2 ] ]
    if(not len(datas)>0):
        return None, []

    
    none_count = 0
    for udata in datas:
        if udata is None:
            none_count += 1

    if none_count==len(datas)-1:
        return None, []  #All are none, the image is not labeled by anyone

    c = True
    diff_list = []
    for i1 in range(0, len(datas)):
        for i2 in range(i1+1, len(datas)):
            if datas[i1] != datas[i2]:
                c = False
                for id, d in enumerate(datas[i1]):
                    if d != datas[i2][id]:
                        diff_list.append(id)

    
    return c, diff_list

def format_width(data, length):
    width = 0
    for char in data:
        if len(char.encode('utf8'))==3:
            width += 2
        else:
            width += 1

    spaces = length-width
    if spaces<0: spaces=0

    return data.ljust(spaces)

    

def list2name(datas):  #將某個txt檔的標記代碼轉為對應標記名稱
    rtn = []
    if datas is not None:
        #print("TEST1", len(d_classes), len(datas))
        #print("TEST2", d_classes, datas)
        if len(d_classes) == len(datas):
            for i, data in enumerate(datas):
                #print("TEST", data, d_classes[i])
                ans = d_classes[i][int(data)]
                qus = t_classes[i]
                rtn.append("{}:{}".format(qus,ans))

        else:
            #print(len(d_classes) ,len(datas))
            rtn = ["數量不對"]
    else:
        rtn = ["無標記"]

    return rtn

def to_png(imgfile_path, img_size=(400,400)):
    image = Image.open(imgfile_path)
    image.thumbnail(img_size)
    bio = io.BytesIO()
    image.save(bio, format="PNG")

    return bio.getvalue()

def update_file_listbox(listtype=0, update_ui=True):
    global window
    counts_img_list = 0
    #try:
    if True:
        # Get list of files in folder
        file_list = []
        all_file_list = os.listdir(path_img_dataset)
        if listtype == 0:
            file_list = all_file_list.copy()
            counts_img_list = len(all_file_list)
        else:
            for iid, img_file in enumerate(all_file_list):
                #filename, file_extension = os.path.splitext(img_file)
                users_lbl_content, users_lbl_list = get_label(img_file)
                #print('test', users_lbl_list)
                compares, _ = compare_labels(users_lbl_list)
                #if(users_lbl_list[0] is not None and users_lbl_list[1] is not None):
                #    print(compares, '--->', users_lbl_list)

                if compares is False:
                    if listtype == 1:  #有user的標記不一樣
                        file_list.append(img_file)
                        counts_img_list += 1
                if compares is None:
                    if listtype == 2:  #皆未標記
                        file_list.append(img_file)
                        counts_img_list += 1
                if compares is True:
                    if listtype == 3:  #相同的
                        file_list.append(img_file)
                        counts_img_list += 1

    #except:
    #    file_list = []
    

    fnames = [
        f
        for f in file_list
        if os.path.isfile(os.path.join(path_img_dataset, f))
            and f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp"))
        ]
    
    if update_ui is True:
        window["-COUNTS-"].update("圖片張數: {} 張".format(counts_img_list))
        window["-FILE LIST-"].update(fnames)

    else:
        expot_list = ''
        types = ['全部', '不同', '未標', '相同']
        filename = "{}_圖片分類列表.csv".format(types[listtype])
        f = codecs.open(filename, "w", "utf-8")
        expot_list += filename+ '\n'
        for line in fnames:
            f.write(line + '\n')
            users_lbl_content, users_lbl_list = get_label(line)
            compares, diffs = compare_labels(users_lbl_list)

            if listtype==1:
                display_txt = get_lbl_compate(line, diffs)
                f.write(display_txt + '\n')
                f.write('-------------------------------------------------------------------------------------------------\n')

        f.close()

        return expot_list

def win_layout():
    file_list_column = [
        [
            sg.Text("ClassMap檔案"),
            sg.In(size=(25, 1), enable_events=True, key="-FILE_CLASS_MAP-"),
            sg.FileBrowse(),
        ],
        [
            sg.Text("圖片檔資料夾"),
            sg.In(size=(25, 1), enable_events=True, key="-FOLDER_IMAGE-"),
            sg.FolderBrowse(),
        ],
        [
            sg.Text("標記檔資料夾"),
            sg.In(size=(25, 1), enable_events=True, key="-FOLDER_USERS-"),
            sg.FolderBrowse(),
        ],
        [sg.Radio('全部', 'listType', size=(8, 1), key='-LIST_TYPE_ALL-', enable_events=True), \
            sg.Radio('不一致', 'listType', size=(8, 1), key='-LIST_TYPE_DIFF-', enable_events=True), \
            sg.Radio('未標記', 'listType', size=(8, 1), key='-LIST_TYPE_NONE-', enable_events=True), \
            sg.Radio('相同', 'listType', size=(8, 1), key='-LIST_TYPE_SAME-', enable_events=True)],

        [sg.Text('_'  * 50)],
        [sg.Text("圖片張數:          ", key="-COUNTS-")],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(50, 10), key="-FILE LIST-"
            )
        ],
    ]

    # For now will only show the name of the file that was chosen
    image_viewer_column = [
        [sg.Text(size=(50, 1), key="-TOUT-")],
        [sg.Image(key="-IMAGE-")],
    ]

    label_list_row = [
        [sg.Text('_'  * 150)],
        [sg.Text(size=(150, 10), key="-LABELS_LIST-")],
        [sg.Button('匯出結果' ,key='-EXPORT-'), sg.Exit()]
    ]

    # ----- Full layout -----
    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
            sg.Column(image_viewer_column),
        ],[
            sg.Column(label_list_row),
        ]
    ]

    return  sg.Window("Image Viewer", layout)

def get_lbl_compate(file_name, difflist):
    users_lbl_content, users_lbl_list = get_label(file_name)
    #print("test", users_lbl_content, users_lbl_list )
    display_txt = ""
    for user_name in users_lbl_content:
        user_name2 = '[{}]'.format(user_name)
        display_txt += '\n{}'.format(format_width(user_name2, width_space))
        if users_lbl_content[user_name][1] is not None:
            for id, ldata in enumerate(users_lbl_content[user_name][1]):
                content = ldata.split(':')[1]
                if(id in difflist):
                    display_txt += "{} ".format(format_width(content, width_space))
                #else:
                #    display_txt += "{} ".format(format_width(content, width_space))

    return display_txt

#--------------------------------------------------------------------------------------------------

window = win_layout()

# Run the Event Loop
while True:

    event, values = window.read()

    if event in [None ,'Exit']:
        confirm_exit = sg.popup_ok_cancel('你確定要結束嗎?', title='確定', keep_on_top=True)
        if confirm_exit == 'OK':
            window.close()
            break


    # Folder name was filled in, make a list of files in the folder
    if event == "-FILE_CLASS_MAP-":
        path_class_map = values["-FILE_CLASS_MAP-"]
        load_class_file(path_class_map)

    if(os.path.exists(path_user_works) and os.path.exists(path_img_dataset) and len(d_classes)>0 ):
        if event == "-LIST_TYPE_ALL-":  update_file_listbox(listtype=0, update_ui=True)
        if event == "-LIST_TYPE_DIFF-": update_file_listbox(listtype=1, update_ui=True)
        if event == "-LIST_TYPE_NONE-": update_file_listbox(listtype=2, update_ui=True)
        if event == "-LIST_TYPE_SAME-": update_file_listbox(listtype=3, update_ui=True)    


    if event == "-FOLDER_USERS-":
        path_user_works = values["-FOLDER_USERS-"]

    if event == "-FOLDER_IMAGE-":
        path_img_dataset = values["-FOLDER_IMAGE-"]


    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        #try:
        if len(values["-FILE LIST-"])>0:
            #try:

            users_lbl_content, users_lbl_list = get_label(values["-FILE LIST-"][0])
            compares, diffs = compare_labels(users_lbl_list)
            display_txt = get_lbl_compate(values["-FILE LIST-"][0], diffs)
            #except:
            #    continue

            window["-LABELS_LIST-"].update(display_txt)

            filename = os.path.join(
                path_img_dataset, values["-FILE LIST-"][0]
            )
            #print('filename', filename)
            #print('exists', os.path.exists(filename))
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(data=to_png(filename, (400,300)))
            
    elif event == "-EXPORT-":
        if(os.path.exists(path_user_works) and os.path.exists(path_img_dataset) and len(d_classes)>0 ):
            print("Export")
            window.FindElement('-EXPORT-').Update(disabled=True)
            f1 = update_file_listbox(listtype=0, update_ui=False)
            f2 = update_file_listbox(listtype=1, update_ui=False)
            f3 = update_file_listbox(listtype=2, update_ui=False)
            f4 = update_file_listbox(listtype=3, update_ui=False)
            window.FindElement('-EXPORT-').Update(disabled=False)

            sg.popup_ok('已匯出csv檔案:\n   {}   {}   {}   {}'.format(f1,f2,f3,f4), title='匯出列表', keep_on_top=True)
        #except:
        #    pass

