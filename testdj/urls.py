'''
@Description:
@Autor: YangZeMiao
@Date: 2019-12-05 08:33:24
@LastEditors: YangZeMiao
@LastEditTime: 2019-12-17 17:48:17
'''
"""testdj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""




from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.shortcuts import render
import time
import uuid
import random
import string
import pandas as pd
import numpy as np
from pyecharts.charts import Page, Line ,Bar ,Pie ,Map ,WordCloud, Tab
from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.globals import SymbolType
from pyecharts.globals import ThemeType
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
import os
def index(request):
    return render(request, 'index.html')

def upload(request):
   if request.method == 'POST':
       fe = request.FILES.get('file', None)
       filesname = ''.join(random.sample(string.ascii_letters + string.digits, 8))+fe.name     
       filespath = 'excel//' +filesname
       if fe:
           with open(filespath, 'wb') as f:
               for chunk in fe.chunks():
                    f.write(chunk)
                    f.close()
                    pd.set_option('display.max_columns', None)
                    # 显示所有行
                    pd.set_option('display.max_rows', None)
                    # 设置数据的显示长度，默认为50
                    pd.set_option('max_colwidth', 200)
                    # 禁止自动换行(设置为Flase不自动换行，True反之)
                    pd.set_option('expand_frame_repr', False)


                    # excel I/O设置
                    # io = filespath
                    # io = 'excel/lk7xKJp5exportx_UR.xlsx'
                    io = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/excel/'+filesname
                    # io = io.strip()
                    # return HttpResponse(temp_io)
                    # 生成pandas DataForm
                    # io = r''+io
                    # return HttpResponse(io)
                    data = pd.read_excel(io=io, sheet_name=0)
                    # 删除某列包含特殊字符的行
                    read_data = data[~ data['客户名称'].str.contains('多次上门')]
                    # 删除某列包含特殊字符的行
                    read_data = read_data[~ read_data['客户名称'].str.contains('售后支持')]
                    # 删除某列包含特殊字符的行
                    read_data = read_data[~ read_data['客户名称'].str.contains('实施支持')]


                    name_data = read_data
                    name_data.dropna(axis=0, how='any', inplace=True, subset=["实施工程师"])
                    name_sheet = name_data.实施工程师.drop_duplicates()
                    more_name_sheets = name_sheet[name_sheet.str.contains(',')]
                    name_sheet = name_sheet[~name_sheet.str.contains(',')]
                    # name_data = name_data[name_data['实施工程师'].str.contains('陈中华')]

                    # print(type(name_sheet))
                    # exit()
                    temp_list = []
                    for name in more_name_sheets:
                        temp_list.append(name[0:name.rfind(',')])
                        temp_list.append(name[name.rfind(',')+1:])
                    # final_name_sheet = name_sheet.append(temp_list)
                    # name_sheet.drop_duplicates()
                    temp_serise = pd.Series(temp_list)
                    final_name_sheet = name_sheet.append(temp_serise, ignore_index=True)
                    final_name_sheet = final_name_sheet.drop_duplicates()

                    # ["姓名", "参与工程", "完成项目数", "推迟项目数","进行中项目数","员工工作量占比（%）"]
                    final_data_pyecharts = []

                    for name in final_name_sheet:
                        final_one_pyechart = []
                        final_one_pyechart.append(name)
                        final_one_pyechart.append(
                            name_data[name_data['实施工程师'].str.contains(name)]['实施工程师'].count())

                        tttt = name_data[name_data['实施工程师'].str.contains(name)]
                        tttt.dropna(axis=0, how='any', inplace=True, subset=["项目状态"])

                        ffff = tttt[tttt['项目状态'].str.contains('finished')]['实施工程师'].count()
                        final_one_pyechart.append(ffff)

                        eeee = tttt[tttt['项目状态'].str.contains('suspended')]['实施工程师'].count()
                        final_one_pyechart.append(eeee)

                        gggg = tttt[tttt['项目状态'].str.contains('processing')]['实施工程师'].count()
                        final_one_pyechart.append(gggg)

                        final_one_pyechart.append(ffff/name_data['实施工程师'].count()*100)

                        final_data_pyecharts.append(final_one_pyechart)


                    # txt = open(r'out.txt','w',encoding='utf-8')
                    # print(final_name_sheet,file=txt)
                    # txt.close()


                    # 获取产品次数
                    # 去重 获取所有产品名称
                    productNames = read_data["产品名称"].drop_duplicates()
                    # 去除NaN
                    productNames.dropna(axis=0, how='any', inplace=True)
                    resList = []
                    for name in productNames:
                        resList.append([name, list(data.产品名称).count(name)])


                    # 获取所有省列表
                    provinceNames = data['省'].drop_duplicates()
                    # 去除NaN
                    provinceNames.dropna(axis=0, how='any', inplace=True)
                    # 最终结果集
                    mapResList = []
                    # 最大销量值
                    maxNum = list(data.省).count(provinceNames[0])
                    # 最终结果集添加和清洗
                    for name in provinceNames:
                        num = list(data.省).count(name)
                        name = name[:-1]
                        if(name == '新疆维吾尔自治'): name = '新疆'
                        if(name == '广西壮族自治'): name = '广西'
                        if(name == '宁夏回族自治'): name = '宁夏'
                        if(name == '内蒙古自治'): name = '内蒙古'
                        mapResList.append([name, num])
                        if(maxNum < num):
                            maxNum = num


                    # 最大耗时，最小耗时
                    minTimeList = []
                    maxTimeList = []
                    barData = read_data
                    barData.dropna(axis=0, how='any', inplace=True, subset=["产品名称"])
                    for name in productNames:
                        minTimeList.append(barData[barData['产品名称'].str.contains(name)].实施天数.min())
                        maxTimeList.append(barData[barData['产品名称'].str.contains(name)].实施天数.max())


                    table = Table()
                    headers = ["姓名", "参与工程", "完成项目数", "推迟项目数", "进行中项目数", "员工工作量占比（%）"]
                    table.add(headers, final_data_pyecharts).set_global_opts(
                            title_opts=ComponentTitleOpts(title="工作量表",)
                        )


                    # 一个产品最大项目耗时
                    timeBar = (
                            Bar(init_opts=opts.InitOpts(
                                theme=ThemeType.LIGHT, width='1800px', height='900px'))
                            .add_xaxis(list(productNames))
                            .add_yaxis("最大时间", list(maxTimeList), category_gap="50%", gap='100%',)
                            .add_yaxis("最小时间", list(minTimeList), category_gap="50%", gap='-100%')
                            .set_global_opts(
                                xaxis_opts=opts.AxisOpts(
                                    axislabel_opts=opts.LabelOpts(rotate=-45)),
                            )
                        )
                    # 词汇图
                    c = (
                            WordCloud(init_opts=opts.InitOpts(width='1800px', height='900px'))
                            .add("", resList, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
                            .set_global_opts(title_opts=opts.TitleOpts(title="所有产品销量图"))
                        )
                    # 产品销量饼状图
                    pie = (
                        Pie(init_opts=opts.InitOpts(width='1800px', height='900px'))
                        .add("", resList)
                        .set_global_opts(
                                title_opts=opts.TitleOpts(title="所有产品销量图"),
                                legend_opts=opts.LegendOpts(
                                    type_="scroll", pos_left="80%", orient="vertical",
                                ),
                            )
                        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}",))
                    )
                    sailMap = (
                            Map(init_opts=opts.InitOpts(width='1800px', height='1000px'))
                            .add("", mapResList, "china", is_map_symbol_show=False, zoom=1)
                            .set_global_opts(
                                title_opts=opts.TitleOpts(title="所有产品销量分布"),
                                visualmap_opts=opts.VisualMapOpts(max_=maxNum),
                            )
                            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}"))
                        )
                    tab = Tab(page_title='分析报告')
                    tab.add(c, "文字图")
                    tab.add(pie, "饼状图")
                    tab.add(sailMap, "地图销量")
                    tab.add(timeBar, "消耗时间")
                    tab.add(table, "工作量表")
                    tab.render('templates/html/'+filesname+'.html')
           return render(request, 'html/'+filesname+'.html')
   return render(request,'index.html')
    
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('show/', upload),
]
