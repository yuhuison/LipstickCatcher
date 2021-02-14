# -*- coding: utf-8 -*-
import json
import image


"""将json数据转换为python的数据类型
完成人：赵君夫
"""
datalist=[]
def parseJSON():
    count=0
    f=open("lipstick.json",encoding='UTF-8')
    text=f.read()
    data=json.loads(text)
    data=data['brands']
    for brand in data:
        brandname=brand["name"]
        series=brand["series"]
        for aseries in series:
             seriesname=(aseries["name"])
             for lipstick in aseries["lipsticks"]:
                 count+=1
                 alist=[brandname,seriesname,lipstick['name'],lipstick["color"],str(count),aseries['price'],aseries['link']]
                 datalist.append(tuple(alist))

"""依靠ID获取对应的口红
:param  <str>id
:return <tuple>
完成人：赵君夫
"""
def getLipstickByID(n):
    ineed=[]
    for lipstick in datalist:
        if lipstick[4]==n:
            ineed.append(lipstick)            
    return ineed

"""依靠颜色获取与该颜色接近的5个口红
:param  <int>color
:return <tuple>
完成人：赵君夫
"""
def matchSimlarLipstick(color):
    ndatalist=[]
    for lipstick in datalist:
        lipcolor=lipstick[3].replace("#","")
        lipcolor=image.hexTo10(lipcolor)
        distance=image.getColorDistance(color,lipcolor)
        ndatalist.append(lipstick+(distance,0))
    ndatalist.sort(key=lambda x:x[7])
    print(ndatalist)
    return(ndatalist[0][4],ndatalist[1][4],ndatalist[2][4],ndatalist[3][4],ndatalist[4][4])

"""依靠颜色获取与该颜色接近的10个同色系口红
:param  <int>color
:return <tuple>
完成人：赵君夫
"""
def matchSameColor(color):
    ndatalist=[]
    for lipstick in datalist:
        lipcolor=lipstick[3].replace("#","")
        lipcolor=image.hexTo10(lipcolor)
        distance=image.getColorDistance(color,lipcolor)
        ndatalist.append(lipstick+(distance,0))
    ndatalist.sort(key=lambda x:x[7])
    returnlist=[i[4] for i in ndatalist]
    returnlist=returnlist[0:10]
    return(tuple(returnlist))

"""获取一个品牌的所有口红
:param  <str>brand
:return <tuple>
完成人：赵君夫
"""
def matchSameBrand(brand):
    ndatalist=[]
    for lipstick in datalist:
        if lipstick[0]==brand:
            ndatalist.append(lipstick[4])
    return tuple(ndatalist)

