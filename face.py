# -*- coding: utf-8 -*-

import face_recognition
from PIL import Image

class iface:
    
    """初始化一个iface对象
    :param imagepath: <str>图像的路径
    完成人：耿茂荣
    """
    def __init__(self,imagepath):
        self.path=imagepath
        self.img=face_recognition.load_image_file(imagepath)
        
    """检测iface对象中是否存在人脸
    :return <BOOL>
    完成人：耿茂荣
    """
    def hasFace(self):
        self.locations=(face_recognition.face_locations(self.img))
        if(len(self.locations)==0):
            return False
        return True
    
    """检测iface对象中是否存在嘴唇部分
       并且取得嘴唇部分对应的矩形
    :return <BOOL>
    完成人：耿茂荣
    """
    def findLips(self):
        self.face_landmarks_list = face_recognition.face_landmarks(self.img)
        if(len(self.face_landmarks_list)>0):
            self.marks=self.face_landmarks_list[0]
            if "top_lip" in list(self.marks.keys()):
                 if "bottom_lip"  in list(self.marks.keys()):           
                     self.lipTop=self.marks['top_lip']
                     self.lipBottom=self.marks['bottom_lip']
                     return True
                 else:
                     return False
            else:
                return False
        else:
            return False
        
    """截取iface中的嘴唇矩形图片，并保存
    完成人：耿茂荣
    """
    def getAndCutLipsRECT(self):
        topPoints=[i[1] for i in self.lipTop]
        #Y坐标的数组
        bottomPoints=[i[1] for i in self.lipBottom]
        leftPoints=[i[0] for i in self.lipTop]+[i[0] for i in self.lipBottom]
        topPoints.sort()
        bottomPoints.sort()
        leftPoints.sort()
        top=topPoints[0]
        #取得最顶边坐标
        bottom=bottomPoints[-1]
        #取得最底边坐标
        left=leftPoints[0]
        #取得最左边坐标
        right=leftPoints[-1]
        #取得最右边坐标
        img=Image.open(self.path)
        imglips=img.crop((left,top,right,bottom))
        #裁剪图片
        imglips.save(self.path+"_.jpg")
        return self.path+"_.jpg"
        

#debug:

