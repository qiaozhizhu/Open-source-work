import pandas as pd
from pyecharts import Bar
from pyecharts import Pie
import pymongo
import numpy as np
#把数据库中的数据读取出来,转换成dataframe格式
myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['lab1']
mycol = mydb['information']
data = pd.DataFrame(list(mycol.find()))
#提取行和列,这是把所有的的行中的name,project.... 提取了出来（去除mongoDB中的id项）
data = data.loc[:,['project','name','star','fork','request','issue','license','describe']]
#查询各种不同的license在项目中的占比,提取出不同许可证的数量转换成字典模式
agg_find_license = data.groupby('license').agg({'license':'count'})
license_dict = agg_find_license.to_dict('dict')
license_data = license_dict['license']
#删除null项目
del license_data['null']
#提取出license_data中的键和值
license_list = list(license_data.keys())
count = []
for item in license_data:
    count.append(license_data[item])
#绘制饼图
pie = Pie('项目中许可证占比',height=1000,width=1200)
pie.add('',license_list,count,is_label_show=True)
pie.render('饼图.html')
#pandas 对star。。。。类型转换
data[['star']] = data[['star']].apply(pd.to_numeric)
data[['fork']] = data[['fork']].apply(pd.to_numeric)
data[['request']] = data[['request']].apply(pd.to_numeric)
data[['issue']] = data[['issue']].apply(pd.to_numeric)
#找出star数值排在前十的作者
agg_find_name = data.groupby('name').agg({'star':'sum','fork':'sum','request':'sum','issue':'sum'})
agg_find_name = agg_find_name.sort_values(by=['star'],ascending=False)
dict1  = agg_find_name.to_dict('dict')
star_list = []
fork_list = []
request_list =[]
issue_list = []
star_dict = dict1['star']
for item in star_dict:
    star_list.append(star_dict[item])
fork_dict = dict1['fork']
for item in fork_dict:
    fork_list.append(fork_dict[item])
request_dict = dict1['request']
for item in request_dict:
    request_list.append(request_dict[item])
issue_dict = dict1['issue']
for item in issue_dict:
    issue_list.append(issue_dict[item])
name0 = list(star_dict.keys())
name_list = []
count = 0
for i in name0:
    if 'mirror' in i:
        i = i.split(' / ')[1]
    name_list.append(i)
    count = count+1
#数据分析完成，图表可视化，1.柱状图显示排行前十的项目的项目名，star,fork,的数值   2.饼状图显示各个许可证在项目总数中的占比
#pyecharts,columns中的值是array2
bar = Bar('gitcode上各类数据总计排行前十大佬',title_pos='left',height=1000,width=1200)
bar.add("star", name_list[0:10], star_list[0:10], mark_line=["average"], mark_point=["max", "min"])
bar.add("fork", name_list[0:10], fork_list[0:10], mark_line=["average"], mark_point=["max", "min"])
#bar.add("合并请求", columns, data3, mark_line=["average"], mark_point=["max", "min"])
#bar.add("issue", columns, data4, mark_line=["average"], mark_point=["max", "min"])
bar.render('柱状图.html')

