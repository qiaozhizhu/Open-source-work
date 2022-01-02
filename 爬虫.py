# @Time    : 2021/12/28 19:32
# @Author  : 软测1905 朱金龙 201992291
# @FileName: main.py
# @Software: PyCharm
import requests
import re
import pandas as pd
import pymongo
def Gethtml(url):
     headers = {
          "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43"
     }
     html = requests.get(url, headers=headers)
     return html.text


def issue_count(content):
     list = []
     issue_count = re.compile(r'<a class="d-none d-xl-flex align-items-center icon-wrapper issues has-tooltip".*?Issue.*?</use></svg>\n(?P<issue>.*?)\n</a>',re.S)
     result = issue_count.finditer(content)
     for item in result:
          list.append(item.group("issue"))
     return list


def lisence_kind(content):
     list = []
     lisence = re.compile(r'<a class="d-none d-xl-flex align-items-center icon-wrapper issues has-tooltip".*?许可证.*?</use></svg>\n(?P<lisence>.*?)\n</a>',re.S)
     result = lisence.finditer(content)
     for item in result:
          list.append(item.group("lisence"))
     return list


def request_count(content):
     list = []
     request_count = re.compile(r'<a class="d-none d-xl-flex align-items-center icon-wrapper merge-requests has-tooltip".*?</use></svg>\n(?P<request>.*?)\n</a>',re.S)
     result = request_count.finditer(content)
     for item in result:
          list.append(item.group("request"))
     return list


def fork_count(content):
     list = []
     fork_count = re.compile(r'<a class="align-items-center icon-wrapper forks has-tooltip".*?</use></svg>\n(?P<fork>.*?)\n</a>',re.S)
     result = fork_count.finditer(content)
     for item in result:
          list.append(item.group("fork"))
     return list


def star_count(content):
     list = []
     re_count = re.compile(r'<span class=".*?-star-count">\n(?P<count>.*?)\n</span>')
     result = re_count.finditer(content)
     for item in result:
          list.append(item.group("count"))
     return list


def Name(content):
     list = []
     re_name = re.compile(r'<span class="namespace-name">\n(?P<name>.*?)\n')
     result = re_name.finditer(content)
     for item in result:
          list.append(item.group("name"))
     return list


def Project(content):
     list = []
     re_project = re.compile(r'<span class="project-name">(?P<project>.*?)</span>')
     result = re_project.finditer(content)
     for item in result:
          list.append(item.group("project"))
     return list


def Describe(content):
     list = []
     re_describe = re.compile(r'<p data-sourcepos="1..*?" dir="auto">(?P<describe>.*?)</p>')
     result = re_describe.finditer(content)
     for item in result:
          list.append(item.group("describe"))
     return list


def  Unit(html):
     list = []
     li = re.compile(r'<li class="d-flex .*?project-row">(?P<unit>.*?)</li>',re.S)
     result = li.finditer(html)
     for item in result:
          list.append(item.group("unit"))
     return list


if __name__ == '__main__':
     myclient = pymongo.MongoClient('mongodb://localhost:27017/')
     mydb = myclient['lab1']
     mycol = mydb['information']
     k = 0
     list = []
     lists = [[]for i in range(750)]
     #第一步获取一个页面的html,第二步获取一个页面中的每个项目所在的函数<li class="d-flex project-row">的代码段，在代码段中进行匹配，若没有则记为空
     #建立循环，获取50页html的内容
     for i in range(37):
          #每一页的url,以i为变化
          url = f'https://gitcode.net/explore/topics/java?page={i+1}'
          #获取html
          text = Gethtml(url)
          #获取每个html中的项目的信息盒子
          unit = Unit(text)
          #输出项目数量
          #建立循环，将每个页面中的每个项目的信息进行提取
          for j in unit:
               #对各项信息进行提取，共724个项目的信息。
               project = Project(j)
               name = Name(j)
               star = star_count(j)
               #去除数据中的其他符号
               star[0] = star[0].replace(',','')
               fork = fork_count(j)
               request = request_count(j)
               issue = issue_count(j)
               lisence = lisence_kind(j)
               if len(lisence) == 0:
                    lisence.append('null')
               describe = Describe(j)
               if len(describe) == 0:
                    describe.append('null')
               star[0] = int(star[0] )
               mycol.insert_one({"project":project[0],"name":name[0],"star":star[0],"fork":fork[0],"request":request[0],"issue":issue[0],"license":lisence[0],"describe":describe[0]})



