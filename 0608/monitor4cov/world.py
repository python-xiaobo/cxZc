import random, requests
from pyecharts.charts import *
from pyecharts import options as opts
import json


def get_json():
    url = 'https://lab.isaaclin.cn/nCoV/api/area'
    data = requests.get(url).json()
    with open('data.json', 'w') as file:
        json.dump(data, file)


def read_json():
    filename = 'data.json'
    with open(filename) as f:
        json_ = json.load(f)
        return json_


def world_maps():
    data = read_json()
    # url = 'https://lab.isaaclin.cn/nCoV/api/area'
    # data = requests.get(url).json()
    oversea_confirm = []
    for item in data['results']:
        if item['countryEnglishName']:
            oversea_confirm.append((item['countryEnglishName']
                                    .replace('United States of America', 'United States')
                                    .replace('United Kiongdom', 'United Kingdom'),
                                    item['deadCount']))
    world_map = (
        Map(init_opts=opts.InitOpts(theme='dark'))
            .add('累计死亡人数', oversea_confirm, 'world', is_map_symbol_show=False, is_roam=False)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False, color='#fff'))
            .set_global_opts(
            title_opts=opts.TitleOpts(title='全球疫情累计死亡人数地图'),
            legend_opts=opts.LegendOpts(is_show=False),
            visualmap_opts=opts.VisualMapOpts(max_=2700,
                                              is_piecewise=True,
                                              pieces=[
                                                  {"max": 99999, "min": 10000, "label": "10000人及以上",
                                                   "color": "#8A0808"},
                                                  {"max": 9999, "min": 1000, "label": "1000-9999人", "color": "#B40404"},
                                                  {"max": 999, "min": 500, "label": "500-999人", "color": "#DF0101"},
                                                  {"max": 499, "min": 100, "label": "100-499人", "color": "#F78181"},
                                                  {"max": 99, "min": 10, "label": "10-99人", "color": "#F5A9A9"},
                                                  {"max": 9, "min": 0, "label": "1-9人", "color": "#FFFFCC"},
                                              ])
        )
    )
    return world_map


# return world_map.render(path='../templates/worldmap.html')

def randomcolor(kind):
    colors = []
    for i in range(kind):
        colArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        color = ""
        for i in range(6):
            color += colArr[random.randint(0, 14)]
        colors.append("#" + color)
    return colors


def rose():
    # url = 'https://lab.isaaclin.cn/nCoV/api/area'
    # data_json = requests.get(url).json()
    data_json = read_json()
    country_list = []
    count_list = []
    ds = {}
    for item in data_json['results']:
        if item['countryEnglishName']:
            if item['deadCount'] is not None and item['countryName'] is not None:
                if int(item['deadCount']) > 2000:
                    d = {item['countryName']: item['deadCount']}
                    ds.update(d)
    ds = dict(sorted(ds.items(), key=lambda k: k[1]))
    # 名称有重复的，把国家名作为 key 吧
    country_list = ds.keys()
    count_list = ds.values()
    # 随机颜色生成
    color_series = randomcolor(len(count_list))
    rose = (
        # width='800px', height='900px',
        Pie(init_opts=opts.InitOpts(theme='dark'))
            # 添加数据
            .add("", [list(z) for z in zip(country_list, count_list)],
                 radius=['20%', '100%'],
                 center=['60%', '65%'],
                 rosetype='area')
            # 设置全局配置
            # pie.set_global_opts(title_opts=opts.TitleOpts(title='南丁格尔玫瑰图'),
            #                     legend_opts=opts.LegendOpts(is_show=False))
            # 设置全局配置项
            .set_global_opts(title_opts=opts.TitleOpts(title='全球新冠疫情', subtitle='死亡人数超过\n2000 的国家',
                                                       title_textstyle_opts=opts.TextStyleOpts(font_size=15,
                                                                                               color='#0085c3'),
                                                       subtitle_textstyle_opts=opts.TextStyleOpts(font_size=15,
                                                                                                  color='#003399'),
                                                       pos_right='center', pos_left='53%', pos_top='62%',
                                                       pos_bottom='center'
                                                       ),
                             legend_opts=opts.LegendOpts(is_show=False))
            # 设置系列配置和颜色
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True, position='inside', font_size=12,
                                                       formatter='{b}：{c}', font_style='italic',
                                                       font_family='Microsoft YaHei'))
            .set_colors(color_series))
    # return rose.render(path='../templates/rose.html')
    return rose


def page_simple():
    page = Page()
    page.add(
        world_maps(),
        rose(),
    )
    page.render("nans.html")


def get_world():
    url = 'http://aiiyx.cn:81/llw'
    req = requests.get(url).text
    dic = eval(req)
    return dic


def get_rose():
    url = 'http://aiiyx.cn:81/rrw'
    req = requests.get(url).text
    dic = eval(req)
    return dic
