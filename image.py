# -*- coding: utf-8 -*-
#将图片中的像素点提取出来，储存在zc中
from PIL import Image
import numpy as np
import math

"""计算两个颜色在LAB空间下的色差
:param c1: <int>预计算的颜色值1(10进制)
:param c2: <int>预计算的颜色值2(10进制) 
:return: <int>LAB空间下的色差
完成人：靳浩昊
"""
def getColorDistance(c1,c2):
    c1=n10Torgb(c1)
    c2=n10Torgb(c2)
    ar=c1[0]+c2[0]
    ar=ar/2
    dr=c1[0]-c2[0]
    dg=c1[1]-c2[1]
    db=c1[2]-c2[2]
    dc=(2+ar/256)*dr*dr+4*dg*dg+(2+(255-dr)/256)*db*db
    dc=math.sqrt(dc)
    return dc


"""取得嘴唇图片中嘴唇部分的颜色
:param imagepath: <str>图片的路径
:return: <int>嘴唇部分的颜色(10进制)
完成人：靳浩昊
"""
def getLipsColor(imagepath):
    zc1=np.array(Image.open(imagepath))
    #将每一个像素点的RGB值存储在一个列表中，所有列表储存在zc2中
    zc2=[]
    for i in zc1:
       for j in i:
           zc2.append(j)
    #将非口红的颜色RGB值变为0
    for i in zc2:
       if i[1] in range(97,256):
           i[1]=0
       if i[2] in range(251,256):
           i[2]=0
    R=[]
    G=[]
    B=[]
    #将每一个像素点对应的R,G,B值提取出来，分别存储在三个列表中
    for i in zc2:
        R.append(i[0])
        G.append(i[1])
        B.append(i[2])
    #定义一个函数来除去已变为0的点，并计算各值的平均值
    def removeZero(x):
       for i in x:
          if i==0:
              x.remove(i)
    removeZero(R)
    removeZero(G)
    removeZero(B)
    ar=int(sum(R)/len(R))
    ag=int(sum(G)/len(G))
    ab=int(sum(B)/len(B))
    return rgbTo10(ar, ag, ab)

"""将一个RGB颜色值转化为10进制颜色值
:param R,G,B: <int>颜色分量值
:return: <int>10进制颜色值
完成人：靳浩昊
"""
def rgbTo10(r,g,b):
    return r*65536+g*256+b

"""将一个10进制颜色值转化rgb颜色值
:param n10: <int>10进制颜色值
:return: <tuple><int(R,G,B)>颜色分量值
完成人：靳浩昊
"""
def n10Torgb(n10):
    r=n10/65536
    r=int(r)
    g=(n10-r*65536)/256
    g=int(g)
    b=(n10-r*65536-g*256)
    b=int(b)
    return (r,g,b)

"""将一个16进制数转换为10进制数
:param hex: <str>欲被转换的16进制数
:return: <int>10进制转换结果
完成人：靳浩昊
"""
#定义一个函数，将一个16进制数转为一个10进制数
def hexTo10(nhex):
    nhex=int(nhex,16)
    return nhex

"""将一个16进制数转换为R,G,B颜色分量
:param hex: <str>欲被转换的16进制数
:return: <tuple:rgb>r,g,b颜色分量
完成人：靳浩昊
"""
#定义一个函数，将列表中的十六进制颜色值转换为RGB颜色值
def hexToRgb(nhex):
    nhex=hexTo10(nhex)
    r=nhex/65536
    r=int(r)
    g=(nhex-r*65536)/256
    g=int(g)
    b=(nhex-r*65536-g*256)
    b=int(b)
    return (r,g,b)



