#!/usr/bin/python
# encoding:utf-8

import time
from DBtools import OPMysql


# 获取时间
def get_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年", "月", "日")


# 测试数据表是否写入信息（主要用作测试使用）
def test():
    mysqlDB = OPMysql()
    sql = "select * from details"
    res = mysqlDB.query(sql)
    return res[0]


# 获取全国疫情的关键信息，按照更新的时间节点的最新日期从表中查取数据包括累计确诊、治愈、死亡等相关数据
def get_c1_data():
    mysqlDB = OPMysql()
    sql = "select sum(confirm)," \
          "(select suspect from history order by ds desc limit 1)," \
          "sum(heal),sum(dead) from details " \
          "where update_time=(select update_time from details order by update_time desc limit 1) "
    res = mysqlDB.query(sql)
    return res[0]


# 获取各省份以及各省份对应的累计确诊人数，做可视化疫情地图做数据支撑
def get_c2_data():
    mysqlDB = OPMysql()
    sql = "select province,sum(confirm) from details " \
          "where update_time=(select update_time from details " \
          "order by update_time desc limit 1) " \
          "group by province"
    res = mysqlDB.query(sql)
    return res


# 通过查找history库获取累计确认折线图的数据支撑
def get_l1_data():
    mysqlDB = OPMysql()
    sql = "select ds,confirm,suspect,heal,dead from history"
    res = mysqlDB.query(sql)
    return res


# 通过查找history库获取累计确诊折线图的数据支撑
def get_l2_data():
    mysqlDB = OPMysql()
    sql = "select ds,confirm_add,suspect_add from history"
    res = mysqlDB.query(sql)
    return res


# 通过查库获取非武汉地区的全国top5城市地区的确诊数据
def get_r1_data():
    mysqlDB = OPMysql()
    sql = 'select city,confirm from ' \
          '(select city,confirm from details ' \
          'where update_time=(select update_time from details order by update_time desc limit 1) ' \
          'and province not in ("湖北","北京","上海","天津","重庆","香港") ' \
          'union all ' \
          'select province as city,sum(confirm) as confirm from details ' \
          'where update_time=(select update_time from details order by update_time desc limit 1) ' \
          'and province in ("北京","上海","天津","重庆","香港") group by province) as a ' \
          'order by confirm desc limit 5'
    res = mysqlDB.query(sql)
    return res


# 通过查找hotsearch表获取经过统计的词频和热搜词为构建词云图做数据支撑
def get_r2_data():
    mysqlDB = OPMysql()
    sql = "select content from hotsearch order by id desc limit 20"
    res = mysqlDB.query(sql)
    return res

