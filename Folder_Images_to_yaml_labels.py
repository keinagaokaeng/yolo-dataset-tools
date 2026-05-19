import pandas as pd
import os
import urllib.request
import cv2
import numpy as np

def get_image_size(poly):
    arr_seg_row = []
    arr_seg_col = []
    
    if poly is not np.nan:
        for p in eval(poly):
                        
            seg_col = p[0]
            seg_row = p[1]

            arr_seg_col.append(seg_col)
            arr_seg_row.append(seg_row)

        p_row_top    = min(arr_seg_row)
        p_row_bottom = max(arr_seg_row)
        p_col_left   = min(arr_seg_col)
        p_col_right  = max(arr_seg_col)

        obj_w = p_col_right-p_col_left
        obj_h = p_row_bottom-p_row_top
    else:
        obj_w = 1
        obj_h = 1
    return(obj_w,obj_h)
    

def get_sq_image_data(dict_cfg):
    try:
        c_label_name_jpg = os.path.basename(dict_cfg['path_img'])
        c_label_name_new = c_label_name_jpg.replace('.jpg','')
        df_sel = df[df['label.name.new'] == c_label_name_new]
        url    = df_sel['point.media.path_best'].iloc[0]
        resp   = urllib.request.urlopen(url)
        img_ip   = np.asarray(bytearray(resp.read()), dtype="uint8")
        img_ip   = cv2.imdecode(img_ip, cv2.IMREAD_COLOR)
        #path_img = os.path.join(dict_cfg['dir_image'],c_label_name_jpg)
        c_label_name_jpg = os.path.basename(url)
        path_img = os.path.join(dict_cfg['dir_image'],c_label_name_jpg)
        os.makedirs(os.path.dirname(path_img), exist_ok=True)
        cv2.imwrite(path_img,img_ip)

        path_txt  = os.path.join(dict_cfg['dir_label'],c_label_name_jpg.replace('.jpg','.txt'))
        os.makedirs(os.path.dirname(path_txt), exist_ok=True)
        x_center = df_sel['point.x'].iloc[0]
        y_center = df_sel['point.y'].iloc[0]
        poly     = df_sel['point.polygon'].iloc[0]

        obj_w,obj_h = get_image_size(poly)

        str_write = str(dict_cfg['class']) + ' ' + str(x_center) + ' ' + str(y_center) + ' ' + str(obj_w) + ' ' + str(obj_h)

        if os.path.isfile(path_txt):
            with open(path_txt,'a+') as f_txt:
                f_txt.write('\n' + str_write)
            f_txt.close()
        else:
            with open(path_txt,'w') as f_txt:
                f_txt.write(str_write)
            f_txt.close()

    except ValueError as e:
        print('Error > ' + c_label_name_jpg +  ' > ' + str(e))



def get_sq_image_data_local(dict_cfg):
    c_label_name_jpg = os.path.basename(dict_cfg['path_img'])
    c_label_name_new = c_label_name_jpg.replace('.jpg','')
    df_sel           = df[df['label.name.new'] == c_label_name_new]
    c_label_name_jpg = (df_sel['point.media.key'].iloc[0]) + '.jpg'

    path_img_src = dict_cfg['path_img']
    path_img_dst = os.path.join(dict_cfg['dir_image'],c_label_name_jpg)

    img      = cv2.imread(path_img_src)
    #img_blur = cv2.blur(img,(20,20))
    #path_img = os.path.join(dict_cfg['dir_image'],c_label_name_jpg)
    #shutil.copy2(path_img_src,path_img_dst)

    path_txt  = os.path.join(dict_cfg['dir_label'],c_label_name_jpg.replace('.jpg','.txt'))
    x_center = df_sel['point.x'].iloc[0]
    y_center = df_sel['point.y'].iloc[0]
    poly     = df_sel['point.polygon'].iloc[0]

    try:

        obj_w,obj_h = get_image_size(poly)
        
        os.makedirs(os.path.dirname(path_img_dst), exist_ok=True)
        cv2.imwrite(path_img_dst,img)

        str_write = str(dict_cfg['class']) + ' ' + str(x_center) + ' ' + str(y_center) + ' ' + str(obj_w) + ' ' + str(obj_h)
        
        os.makedirs(os.path.dirname(path_txt), exist_ok=True)

        if os.path.isfile(path_txt):
            with open(path_txt,'a+') as f_txt:
                f_txt.write('\n' + str_write)
            f_txt.close()
        else:
            with open(path_txt,'w') as f_txt:
                f_txt.write(str_write)
            f_txt.close()

    except ValueError as e:
        print('Skipping > ' + c_label_name_jpg +  ' > ' + str(e))



if __name__ == '__main__':


    path_archive  = '/Users/keinagaoka/Desktop/Earleria Bruuni /Scripts/export/archive.csv'
    dir_images    = '/Users/keinagaoka/Desktop/Earleria Bruuni /Scripts/export/Kurose/KMROV143/test/images'
    dir_save_base = '/Users/keinagaoka/Desktop/Earleria Bruuni /Scripts/export/Kurose/KMROV143/dataset'


    df = pd.read_csv(path_archive)

    l_files = os.listdir(dir_images)
    l_files = [s for s in l_files if '.DS' not in s and s.endswith('.jpg')]
    # ファイル名からクラス名（ハイフンより前）を抽出して重複を削除
    l_classes = list(set([s.split('-')[0] for s in l_files if '-' in s]))
    l_classes.sort()

    dict_names = {}
    ctr = 0
    for c_class in l_classes:
        dict_names[c_class] = ctr
        ctr = ctr + 1

    dir_save        = dir_save_base
    dir_save_images = os.path.join(dir_save,'images') 
    dir_save_labels = os.path.join(dir_save,'labels')
    path_yaml       = os.path.join(dir_save,'dataset.yaml')

    for c_dir in [dir_save,dir_save_images,dir_save_labels]:
        os.makedirs(c_dir,exist_ok=True)

    print('Folders created.. press Enter to continue')

    with open(path_yaml,'w') as f_yaml:
        f_yaml.write('path: '  + dir_save + '\n')
        f_yaml.write('train: ' + 'images/train' + '\n')
        f_yaml.write('val: '   + 'images/validate' + '\n')
        f_yaml.write('test:'   + '\n')
        f_yaml.write('\n')
        f_yaml.write('names:'   + '\n')
        for c_class in dict_names:
            f_yaml.write('  ' + str(dict_names[c_class]) + ': ' + c_class + '\n')
        f_yaml.close()

    print('YAML created.. press Enter to continue')


    l_files = os.listdir(dir_images)
    for c_class in l_classes:
        # クラス名に前方一致するファイルのみを取得 (例: Chauliodus-0.jpg)
        l_images_class = [s for s in l_files if s.startswith(c_class + '-') and s.endswith('.jpg')]
        l_path_img_class = [os.path.join(dir_images,s) for s in l_images_class]
        img_ctr = 0
        for c_path_img_class in l_path_img_class:
            dict_cfg = {
                'path_img':c_path_img_class,
                'class':dict_names[c_class],
                'dir_image':dir_save_images,
                'dir_label':dir_save_labels
            }
            get_sq_image_data_local(dict_cfg)
            print('Number of images > ' + str(img_ctr) + '/' + str(len(l_path_img_class)))

            img_ctr = img_ctr + 1

