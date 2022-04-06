#!/usr/bin/python
# -*- coding:utf8 -*-

# author:liuhaichao
# description:压缩指定模块里的大图为webp格式
# create date：2020-09-24 on 1:20 PM
import os

# 查找指定文件夹里大于指定kb的图片列表
def findBigImageFile(folder, size):
    bigFiles = []
    for foldername, subfolders, filenames in os.walk(folder):
        # 对文件进行遍历
        for filename in filenames:
            # .getsize(path)必须是完整路径
            file = os.path.join(foldername, filename)
            # size*1024，使参数size单位为kb
            if os.path.getsize(file) > size * 1024:
                file = os.path.abspath(file)
                suffix = os.path.splitext(file)[1]
                if (suffix == ".png" or suffix == ".jpg") and file.find(".9.png") == -1:
                    bigFiles.append(file)
    return bigFiles

# modules为当前同级目录下的图片文件夹列表
folders = ["assets/images",]

# 将大于指定kb的文件都存到bigFiles里
bigFiles = []
for folder in folders:
    # 查找指定文件夹里大于指定kb的图片列表
    bigFiles += findBigImageFile(folder, 50)

# 压缩前的大小
beforeCompressSize = 0
# 压缩后的大小
afterCompressSize = 0
for bigFile in bigFiles:
    absFileName = os.path.splitext(bigFile)[0]
    before = os.path.getsize(bigFile) / 1024
    beforeCompressSize += before
    print "压缩前", before, "kb"
    try:
        cmd = "cwebp -quiet 75 " + bigFile + " -o " + absFileName + ".webp"
        print cmd
        os.system(cmd)
    except BaseException as err:
        print err
    else:
        after = os.path.getsize(absFileName + ".webp") / 1024
        afterCompressSize += after
        print "压缩后", after, "kb", "压缩比", after * 100 / before, "%"
        print ""
for bigFile in bigFiles:
    # 转为webp后删除原文件
    os.remove(bigFile)

if beforeCompressSize > 0:
    print "总压缩比", afterCompressSize * 100 / beforeCompressSize, "%"
