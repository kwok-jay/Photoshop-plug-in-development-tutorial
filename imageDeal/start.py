#!/usr/bin/env python
# Author:Kwok-Jay
import os
import sys
import re
from psd_tools import PSDImage
from colorama import init

init(autoreset=True)
dirs_filter = ['副本',"0", '新建文件夹', '.idea', '.vscode', '已裁剪','ok']
local_path = os.getcwd()

# 创建目录
def mkdir(path):
    """
    创建目录
    :param path: 文件路径
    :return:
    """
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        os.makedirs(path)
        print('创建目录',path)
        return True
    else:
        return False

# 返回至少两位数剧集号
def search_part_num(dir_name):
    partNum = re.findall('\d+', dir_name)
    if len(partNum) > 0:
        partNum = int(partNum[-1])
        if partNum<10:
            partNum = '0' + str(partNum)
        else:
            partNum = str(partNum)
    return partNum

def search_piece_num(file_name):
    pieceNum = re.findall('\d+', os.path.splitext(file_name)[0])
    if len(pieceNum) > 0:
        pieceNum = int(pieceNum[-1])
        if pieceNum<10:
            pieceNum = '0'+str(pieceNum)
        else:
            pieceNum = str(pieceNum)
    return pieceNum
# 检测 源文件 分辨率
def check_ori():
    count = 0
    err_count_w = 0
    err_count_h = 0
    err_res = []
    # 遍历当前目录的项目
    for cartoon_item in os.listdir(local_path):
        if os.path.isfile(cartoon_item): continue
        filter_flag = False
        for dir_filter in dirs_filter:
            if filter_flag is True: break
            if dir_filter in cartoon_item:
                filter_flag = True
                continue
        if filter_flag is True: continue
        cartoon_path = os.path.join(local_path, cartoon_item)
        if os.path.isdir(cartoon_path):
            # print(path,'is dir')
            # 漫画名
            cartoonName = cartoon_item
            print('*=' * 30, 'cartoonName:', cartoonName)
            for parts_item in os.listdir(cartoon_path):
                part_path = os.path.join(cartoon_path, parts_item)
                if os.path.isdir(part_path):
                    if 'JPG' in parts_item: continue
                    # partdir_path = os.path.join(cartoon_path, part_path)
                    # 检测psd
                    for psd_item in os.listdir(part_path):
                        psd_path = os.path.join(part_path, psd_item)
                        if os.path.isfile(psd_path):
                            psd_format = os.path.splitext(psd_path)[1]
                            if (psd_format == '.psd') | (psd_format == '.psb'):
                                count += 1
                                psd = PSDImage.open(psd_path)
                                if psd.width == 1280:
                                    flag_width = True
                                else:
                                    flag_width = False
                                    err_count_w += 1
                                if psd.height < 14000:
                                    flag_height = True
                                else:
                                    flag_height = False
                                    err_count_h += 1
                                print(psd_path, psd.width, '*', psd.height, flag_width, flag_height)
                                if not flag_width&flag_height:
                                    err_text = str(psd_path) + ' ' + str(psd.width) + '*' + str(psd.height) + ' ' + str(flag_width) + ' ' + str(flag_height)
                                    err_res.append(err_text)
                    print('-' * 45)
    print('\033[0;32;40m\*****', '检测完成！宽错误、长错误/合计PSD',err_count_w,err_count_h,'/',count,'\033[0m')
    for text in err_res:
        print(text)




# 重命名 源文件
def rename_ori():
    count = 0
    # 遍历当前目录的项目
    for cartoon_item in os.listdir(local_path):
        if os.path.isfile(cartoon_item): continue
        filter_flag = False
        for dir_filter in dirs_filter:
            if filter_flag is True:break
            if dir_filter in cartoon_item:
                filter_flag = True
                continue
        if filter_flag is True: continue
        cartoon_path = os.path.join(local_path, cartoon_item)
        if os.path.isdir(cartoon_path):
            # print(path,'is dir')
            # 漫画名
            cartoonName = cartoon_item
            try:
                cartoonName = cartoonName.replace('psd', '', -1).replace('PSD', '', -1).replace('韩文','',1).strip()
            except:
                pass
            print('*****cartoonName:', cartoonName, '*****')
            for parts_item in os.listdir(cartoon_path):
                part_path = os.path.join(cartoon_path, parts_item)
                if os.path.isdir(part_path):
                    if 'JPG' in parts_item: continue
                    partNum = search_part_num(parts_item) # 获取集数
                    new_partdir = (cartoonName + " " + partNum)
                    new_partdir_path = os.path.join(cartoon_path, new_partdir)
                    if part_path!=new_partdir_path:
                        os.rename(part_path, new_partdir_path)
                        print("重新命名剧集目录", new_partdir_path)
                    else:
                        print("命名已经符合规范",new_partdir_path)
                    # 创建已裁剪文件夹
                    cuted_path = os.path.join(new_partdir_path, (cartoonName + ' ' + partNum))
                    mkdir(cuted_path)
                    # 重命名psd
                    for psd_item in os.listdir(new_partdir_path):
                        psd_path = os.path.join(new_partdir_path, psd_item)
                        if os.path.isfile(psd_path):
                            psd_format = os.path.splitext(psd_path)[1]
                            if (psd_format == '.psd') | (psd_format == '.psb'):
                                count += 1
                                pieceNum = search_piece_num(psd_item)
                                new_psdname = cartoonName + ' ' + partNum + '-' + pieceNum + '-' + psd_format
                                new_psdpath = os.path.join(new_partdir_path, new_psdname)
                                if psd_path!=new_psdpath:
                                    os.rename(psd_path, new_psdpath)
                                    print("重命名文件*", new_psdpath)
                                else:
                                    print("命名已规范-",psd_path)

    print('\033[0;32;40m\*****', '重命名完成！',count,'\033[0m')


# 生成JPG/PNG
def gen_png():
    count = 0
    count_exist = 0
    count_new = 0
    # 遍历当前目录的项目
    for cartoon_item in os.listdir(local_path):
        filter_flag = False
        for dir_filter in dirs_filter:
            if dir_filter in cartoon_item:
                filter_flag = True
                continue
        if filter_flag is True: continue
        cartoon_path = os.path.join(local_path, cartoon_item)
        if os.path.isdir(cartoon_path):
            # print(path,'is dir')
            # 漫画名
            cartoonName = cartoon_item
            try:
                cartoonName = cartoonName.replace('psd', '', -1).replace('PSD', '', -1).replace('韩文','',1).strip()
            except:
                pass
            print('*=' * 30, 'cartoonName:', cartoonName)
            # 创建JPG目录
            jpg_dir = os.path.join(cartoon_path,'JPG')
            mkdir(jpg_dir)
            for parts_item in os.listdir(cartoon_path):
                part_path = os.path.join(cartoon_path, parts_item)
                if os.path.isdir(part_path):
                    if 'JPG' in parts_item:continue
                    partdir_path = os.path.join(cartoon_path, part_path)
                    # 创建剧集JPG目录
                    partNum = search_part_num(parts_item)
                    jpg_part_dir = os.path.join(jpg_dir, partNum + ' JPG')
                    mkdir(jpg_part_dir)
                    # 遍历psd生成图片
                    temp_count_success = 0
                    temp_count_all = 0
                    for psd_item in os.listdir(partdir_path):
                        psd_path = os.path.join(partdir_path, psd_item)
                        if os.path.isfile(psd_path):
                            psd_format = os.path.splitext(psd_path)[1]
                            if (psd_format == '.psd') | (psd_format == '.psb'):
                                count += 1
                                temp_count_all += 1
                                pieceNum = search_piece_num(psd_item)
                                png_name = pieceNum + '.png'
                                png_path = os.path.join(jpg_part_dir, png_name)
                                if not os.path.exists(png_path):
                                    psd = PSDImage.open(psd_path)
                                    psd.composite().save(png_path)
                                    count_new += 1
                                    print("JPG:", png_path,psd.width, "*", psd.height)
                                    temp_count_success += 1
                                    continue
                                else:
                                    print("JPG:", png_path,'已存在')
                                    count_exist += 1
                    print("JPG:", jpg_part_dir,'完成率',temp_count_success,'/',temp_count_all)
                    print('-' * 45)
    print('\033[0;32;40m\*****', '转换完成！',count_new,'/',count,'\033[0m')



# 检测 裁剪后的文件 分辨率
def check_new():
    count = 0
    err_count_w = 0
    err_count_h = 0
    err_res = []
    # 遍历当前目录的项目
    for cartoon_item in os.listdir(local_path):
        if os.path.isfile(cartoon_item): continue
        filter_flag = False
        for dir_filter in dirs_filter:
            if filter_flag is True: break
            if dir_filter in cartoon_item:
                filter_flag = True
                continue
        if filter_flag is True: continue
        cartoon_path = os.path.join(local_path, cartoon_item)
        if os.path.isdir(cartoon_path):
            # print(path,'is dir')
            # 漫画名
            cartoonName = cartoon_item
            try:
                cartoonName = cartoonName.replace('psd', '', -1).replace('PSD', '', -1).replace('韩文','',1).strip()
            except:
                pass
            print('*=' * 30, 'cartoonName:', cartoonName)
            for parts_item in os.listdir(cartoon_path):
                part_path = os.path.join(cartoon_path, parts_item)
                cuted_part_path = os.path.join(part_path, parts_item)
                if os.path.isdir(cuted_part_path):
                    if 'JPG' in parts_item: continue
                    # partdir_path = os.path.join(cartoon_path, part_path)
                    # 检测psd
                    if len(os.listdir(cuted_part_path)) == 0: print('还未裁剪', cuted_part_path)
                    for psd_item in os.listdir(cuted_part_path):
                        psd_path = os.path.join(cuted_part_path, psd_item)
                        if os.path.isfile(psd_path):
                            psd_format = os.path.splitext(psd_path)[1]
                            if (psd_format == '.psd') | (psd_format == '.psb'):
                                count += 1
                                psd = PSDImage.open(psd_path)
                                if psd.width == 1280:
                                    flag_width = True
                                else:
                                    flag_width = False
                                    err_count_w += 1
                                if psd.height < 14000:
                                    flag_height = True
                                else:
                                    flag_height = False
                                    err_count_h += 1
                                print(psd_path, psd.width, '*', psd.height, flag_width, flag_height)
                                if not flag_width&flag_height:
                                    err_text = str(psd_path) + ' ' + str(psd.width) + '*' + str(psd.height) + ' ' + str(flag_width) + ' ' + str(flag_height)
                                    err_res.append(err_text)
                    print('-' * 45)
    print('\033[0;32;40m\*****', '检测完成！宽错误、长错误/合计PSD',err_count_w,err_count_h,'/',count,'\033[0m')
    for text in err_res:
        print(text)



# 移动 裁剪后的文件
def move_cuted():
    import shutil
    count = 0
    # 遍历当前目录的项目
    for cartoon_item in os.listdir(local_path):
        filter_flag = False
        for dir_filter in dirs_filter:
            if dir_filter in cartoon_item:
                filter_flag = True
                continue
        if filter_flag is True: continue
        cartoon_path = os.path.join(local_path, cartoon_item)
        if os.path.isdir(cartoon_path):
            # print(path,'is dir')
            # 漫画名
            cartoonName = cartoon_item
            try:
                cartoonName = cartoonName.replace('psd', '', -1).replace('PSD', '', -1).replace('韩文','',1).strip()
            except:
                pass
            print('*=' * 30, 'cartoonName:', cartoonName)
            cuted_dir = os.path.join(cartoon_path,'韩文《'+cartoonName+'》已裁剪')
            mkdir(cuted_dir)
            for parts_item in os.listdir(cartoon_path):
                part_path = os.path.join(cartoon_path, parts_item)
                cuted_part_path = os.path.join(part_path, parts_item)
                if os.path.isdir(cuted_part_path):
                    if 'JPG' in parts_item: continue
                    if len(os.listdir(cuted_part_path)) == 0:
                        print('还未裁剪', cuted_part_path)
                        continue
                    new_cuted_part_path = os.path.join(cuted_dir,parts_item)
                    shutil.move(cuted_part_path,new_cuted_part_path)
                    print(cuted_part_path, ' ==> ',new_cuted_part_path, '移动成功')
                    count += 1
            print('-' * 45)
    print('\033[0;32;40m\*****', '移动完成！',count,'\033[0m')

# 移动原有的psd
def move_ori_psd():
    import shutil
    count = 0
    # 遍历当前目录的项目
    for cartoon_item in os.listdir(local_path):
        filter_flag = False
        for dir_filter in dirs_filter:
            if dir_filter in cartoon_item:
                filter_flag = True
                continue
        if filter_flag is True: continue
        cartoon_path = os.path.join(local_path, cartoon_item)
        if os.path.isdir(cartoon_path):
            # print(path,'is dir')
            # 漫画名
            cartoonName = cartoon_item
            print('*=' * 30, 'cartoonName:', cartoonName)
            ori_psd_dir = os.path.join(cartoon_path,'PSD')
            mkdir(ori_psd_dir)
            for parts_item in os.listdir(cartoon_path):
                part_path = os.path.join(cartoon_path, parts_item)
                if os.path.isdir(part_path):
                    if 'JPG' in parts_item: continue
                    if '已裁剪' in parts_item: continue
                    if 'PSD' in parts_item: continue
                    new_ori_part_path = os.path.join(ori_psd_dir,parts_item)
                    shutil.move(part_path,new_ori_part_path)
                    print(part_path, ' ==> ',new_ori_part_path, '移动成功')
                    count += 1
            print('-' * 45)
    print('\033[0;32;40m\*****', '移动完成！',count,'\033[0m')

    # 重命名 源文件
def rename_quick():
    count = 0
    # 遍历当前目录的项目
    for cartoon_item in os.listdir(local_path):
        if os.path.isfile(cartoon_item): continue
        filter_flag = False
        for dir_filter in dirs_filter:
            if filter_flag is True:break
            if dir_filter in cartoon_item:
                filter_flag = True
                continue
        if filter_flag is True: continue
        cartoon_path = os.path.join(local_path, cartoon_item)
        if os.path.isdir(cartoon_path):
            # print(path,'is dir')
            # 漫画名
            cartoonName = cartoon_item
            try:
                cartoonName = cartoonName.replace('psd', '', -1).replace('PSD', '', -1).replace('韩文','',1).strip()
            except:
                pass
            print('*****cartoonName:', cartoonName, '*****')
            cuted_path = os.path.join(cartoon_path, ('《'+cartoonName + '》已裁剪'))
            mkdir(cuted_path)
            for parts_item in os.listdir(cartoon_path):
                part_path = os.path.join(cartoon_path, parts_item)
                if os.path.isfile(part_path):
                    part_format = os.path.splitext(part_path)[1]
                    if (part_format == '.png') | (part_format == '.jpg'):
                        count += 1
                    partNum = search_part_num(parts_item) # 获取集数
                    new_partname= (cartoonName + " " + partNum+ '-' + part_format)
                    new_partpath = os.path.join(cartoon_path, new_partname)
                    if part_path!=new_partpath:
                        os.rename(part_path, new_partpath)
                        print("重命名文件*", new_partpath)
                    else:
                        print("命名已规范-",part_path)                  
                    # 创建已裁剪文件夹
                    cuted_part_path = os.path.join(cuted_path, (cartoonName + ' ' + partNum))
                    mkdir(cuted_part_path)
                    # 重命名psd
    print('\033[0;32;40m\*****', '重命名完成！',count,'\033[0m')
    
while True:
    print("\033[31;1m==========>裁剪辅助脚本<==========\033[1m")
    print('\033[31;1m1.重命名 源文件\033[1m')
    print('\033[31;1m2.检测 源文件 分辨率\033[1m')
    print('\033[31;1m3.请使用ps批量调整尺寸\033[1m')
    print('\033[31;1m4.生成JPG/PNG\033[1m')
    print('\033[31;1m5.请使用ps裁剪另存\033[1m')
    print('\033[31;1m6.检测 裁剪后的文件 分辨率\033[1m')
    print('\033[31;1m7.移动 裁剪后的文件\033[1m')
    print('\033[31;1m8.移动 源文件至PSD文件夹\033[1m')
    print('')
    print('\033[31;1m9.粗裁 重命名PNG\033[1m')
    user_chioce = input("请输入你的选择(按0退出系统)：")
    print("\033[0m")
    # 根据用户的选择展示不同的内容
    if user_chioce == '1':
        rename_ori()
    elif user_chioce == '2':
        check_ori()
    elif user_chioce == '3':
        print('请使用ps批量调整尺寸')
    elif user_chioce == '4':
        gen_png()
    elif user_chioce == '5':
        print('请使用ps裁剪另存')
    elif user_chioce == '6':
        check_new()
    elif user_chioce == '7':
        move_cuted()
    elif user_chioce == '8':
        move_ori_psd()
    elif user_chioce == '9':
        rename_quick()
    elif user_chioce == '0':
    # elif user_chioce.lower() == 'q':
        break
    else:
        print("***你输入的菜单名不存在，请重新输入！***")
        continue
