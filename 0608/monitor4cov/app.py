#!/usr/bin/python
# encoding:utf-8

from flask import Flask as _Flask, jsonify
from flask_cors import CORS
from flask import render_template
from flask.json import JSONEncoder as _JSONEncoder
from jieba.analyse import extract_tags
import decimal
import database
import string
from datetime import datetime
from spider import update_history, update_details, update_hotsearch
import requests
import random
from world import get_world, get_rose


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(_JSONEncoder, self).default(o)


class Flask(_Flask):
    json_encoder = JSONEncoder


# 添加跨域支持，解决因为同源导致的无非访问等问题
app = Flask(__name__)
CORS(app, supports_credentials=True)


# 主页路由，当前访问主页面
@app.route('/')
def hello_word3():
    return render_template("main.html")


# 添加获取当前时间的接口，供前端调取展示当前日期
@app.route('/time')
def get_time():
    return database.get_time()


# 添加获取可视化展示区位的中间上半部分，展示全国疫情的当前主要数据包括确诊、死亡、治愈以及尚存等
@app.route('/c1')
def get_c1_data():
    data = database.get_c1_data()
    return jsonify({"confirm": data[0], "suspect": data[1], "heal": data[2], "dead": data[3]})


# 添加获取可视化展示区位的中间下半部分，展示全国疫情动态地图，地图通过echarts渲染到js前端展示
@app.route('/c2')
def get_c2_data():
    res = []
    for tup in database.get_c2_data():
        res.append({"name": tup[0], "value": int(tup[1])})
    return jsonify({"data": res})


# 添加获取可视化展示区位的左侧上半部分，展示全国当前监控状态下的累计趋势变化图
@app.route('/l1')
def get_l1_data():
    data = database.get_l1_data()
    day, confirm, suspect, heal, dead = [], [], [], [], []
    for a, b, c, d, e in data[7:]:
        try:
            day.append(datetime.strptime(a, '%Y-%m-%d').strftime("%m-%d"))
        except:
            day.append(a.strftime("%m-%d"))
        confirm.append(b)
        suspect.append(c)
        heal.append(d)
        dead.append(e)
    return jsonify({"day": day, "confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead})


# 添加获取可视化展示区位的左侧上半部分，展示全国当前监控状态下的新增趋势变化图
@app.route('/l2')
def get_l2_data():
    data = database.get_l2_data()
    day, confirm_add, suspect_add = [], [], []
    for a, b, c in data[7:]:
        try:
            day.append(datetime.strptime(a, '%Y-%m-%d').strftime("%m-%d"))
        except:
            day.append(a.strftime("%m-%d"))
        confirm_add.append(b)
        suspect_add.append(c)
    return jsonify({"day": day, "confirm_add": confirm_add, "suspect_add": suspect_add})


# 添加获取可视化展示区位的右侧上半部分，展示全国非武汉地区的TOP5确认城市地区信息
@app.route('/r1')
def get_r1_data():
    data = database.get_r1_data()
    city = []
    confirm = []
    for k, v in data:
        city.append(k)
        confirm.append(int(v))
    return jsonify({"city": city, "confirm": confirm})


# 添加获取可视化展示区位的右侧下半部分，展示当前疫情节点下微博的每日热搜新闻等构建词云图
@app.route('/r2')
def get_r2_data():
    data = database.get_r2_data()
    d = []
    for i in data:
        k = i[0].rstrip(string.digits)
        v = i[0][len(k):]
        ks = extract_tags(k)
        for j in ks:
            if not j.isdigit():
                d.append({"name": j, "value": v})
    return jsonify({"kws": d})


# 添加非主页路由，更新数据库信息
@app.route('/update4data')
def get_r3_data():
    update_history()
    update_details()
    update_hotsearch()
    return "数据更新完毕！"


@app.route('/worldmap')
def world():
    worldmap = world_maps()
    # return render_template("worldmap.html")
    return worldmap.dump_options_with_quotes()


@app.route('/world')
def ww():
    # get_json()
    return render_template("worlds.html")


@app.route('/rosemap')
def nan():
    rosemap = rose()
    # return render_template("rose.html")
    return rosemap.dump_options_with_quotes()


@app.route('/w')
def get_w():
    j = get_world()
    return jsonify(j)


@app.route('/r')
def get_r():
    j = get_rose()
    return jsonify(j)


if __name__ == '__main__':
    # 整个项目的启动位置，项目启动后请在浏览器端直接访问5000端口
    # （此处port可修改，访问时即变更端口即可）
    app.run(host="0.0.0.0", port=5000)
