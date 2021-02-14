 
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time
import face
import data
import image
import json
from datetime import timedelta
 
#设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app = Flask(__name__, static_url_path="/static")
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)

"""Flask路由至主页
完成人：于惠松
"""
@app.route('/')
def hello_world():
    return render_template('index.html')

"""Flask上传图片接口
:param <POST>:file 上传图片的文件对象
:return:
    <json>
    state:状态，1代表成功，0代表失败
    path:上传后图片的路径
完成人：于惠松
"""
@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))
        f.save(upload_path)
        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)
        width=img.shape[1]
        height=(400/width)*img.shape[0]
        width=400
        img= cv2.resize(img,(int(width), int(height)))
        filenamesave=str(time.time())+".jpg"
        cv2.imwrite(os.path.join(basepath, 'static/images', filenamesave), img)
        dict1={"state":1,"path":filenamesave}
        return jsonify(dict1)
    return "Please use Post"

"""Flask分析图片接口
:param <POST>:path 上传图片的路径
:return:
    <json>
    state:状态，1代表成功，0代表失败
    fcolor:识别出来的嘴唇部分颜色
    list:识别出来颜色对应口红的字典
完成人：于惠松
"""


@app.route('/getLip',methods=['POST','GET'])
def getLipstickByImage():
    if request.method == 'POST':
        formImagePath=r'static\images\\'
        formImagePath=formImagePath+request.form['path']
        myface=face.iface(formImagePath)
        if(myface.hasFace() and myface.findLips()):
            lipspath=myface.getAndCutLipsRECT()
            lipcolor=image.getLipsColor(lipspath)
            lipsticks=data.matchSimlarLipstick(lipcolor)
            lipslist=[]
            for i in lipsticks:
                lipstick=data.getLipstickByID(i)[0]
                lipslist.append({"brand":lipstick[0],"series":lipstick[1],"colorname":lipstick[2],"color":lipstick[3],"id":lipstick[4],"price":lipstick[5],"link":lipstick[6]})
            dictreturn={"state":1,"fcolor":lipcolor,"list":lipslist}
            return jsonify(dictreturn)
        else:
            dictreturn={"state":0}
            return jsonify(dictreturn)
    return 'Please Use Post'


"""Flask匹配颜色接口
:param <POST>:color 颜色值
:return:
    <json>
    state:状态，1代表成功，0代表失败
    list:与该颜色接近的口红的列表
完成人：于惠松
"""

@app.route('/matchColor',methods=['POST','GET'])
def getLipstickByColor():
    if request.method == 'POST':
        color=request.form['color'].replace("#","")
        color=image.hexTo10(color)
        lipsticks=data.matchSameColor(color)
        lipslist=[]
        for i in lipsticks:
            lipstick=data.getLipstickByID(i)[0]
            lipslist.append({"brand":lipstick[0],"series":lipstick[1],"colorname":lipstick[2],"color":lipstick[3],"id":lipstick[4],"price":lipstick[5],"link":lipstick[6]})
        dictreturn={"state":1,"list":lipslist}
        return jsonify(dictreturn)
    return 'Please Use Post'

"""Flask品牌匹配接口
:param <POST>:brand 品牌名称
:return:
    <json>
    state:状态，1代表成功，0代表失败
    list:与该品牌相同的口红颜色列表
完成人：于惠松
"""

@app.route('/matchBrand',methods=['POST','GET'])
def getLipstickByBrand():
    if request.method == 'POST':
        lipsticks=data.matchSameBrand(request.form['brand'])
        lipslist=[]
        for i in lipsticks:
            lipstick=data.getLipstickByID(i)[0]
            lipslist.append({"brand":lipstick[0],"series":lipstick[1],"colorname":lipstick[2],"color":lipstick[3],"id":lipstick[4],"price":lipstick[5],"link":lipstick[6]})
        dictreturn={"state":1,"list":lipslist}
        return jsonify(dictreturn)
    return 'Please Use Post'




if __name__ == '__main__':
    data.parseJSON()
    app.run(host='0.0.0.0', port=8987, debug=True)
    