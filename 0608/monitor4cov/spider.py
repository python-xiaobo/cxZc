#!/usr/bin/python
# encoding:utf-8

from random import randint
import time
import json
import traceback
import requests
from selenium.webdriver import Chrome
from DBtools import OPMysql
from selenium.webdriver.chrome.options import Options
# 配置信息：
# 1.chrome浏览器的驱动路径（driver_path）
# 2.需要爬取的3个链接的具体url地址（urlConf，json格式方便通过key找到对应value）
driver_path = r"E:\a\chromedriver.exe"
urlConf = {
           "disease_h5": "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5",
           "disease_other": "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other",
           "sina_hot": "https://s.weibo.com/top/summary?cate=realtimehot"
           }


# 利用伪随机的思路，随机获取一个UAgent一次构建hearder，模拟浏览器行为并随时变更浏览器配置
# 保证爬虫的伪装性，高端防止长时间爬取造成的ip被封等问题（基础反爬策略）
def random4agent():
    # 获取一个随机产生的UAgent代理
    USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    ]
    random_agent = USER_AGENTS[randint(0, len(USER_AGENTS) - 1)]
    return random_agent


# 获取疫情期间内的新浪热搜新闻数据
# 该网站利用js做了渲染，因此数据爬取需要模拟网页端自动化分析页面并爬取数据，与request爬取静态页面思路不用
# 这里要先通过解析网页找到我们要爬取的数据信息的区块并通过selenium辅助爬取再对爬取数据做解析保存
def get_sina_hot():
    # chrome_options = Options()
    # chrome_options.add_argument('headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # browser = Chrome(chrome_options=chrome_options)
    # browser.get(urlConf["sina_hot"])
    # c = browser.find_elements_by_xpath('//*[@id="pl_top_realtimehot"]/table/tbody/tr/td[2]')
    # context = [i.text for i in c]
    # browser.close()
    # return context[1:]
    browser = Chrome(driver_path)
    browser.get(urlConf["sina_hot"])
    c = browser.find_elements_by_xpath('//*[@id="pl_top_realtimehot"]/table/tbody/tr/td[2]')
    context = [i.text for i in c]
    browser.close()
    return context[1:]


# 爬取url中的数据，该爬取是针对静态页面的爬取，直接利用request并伪装UAgent即可
# 再对爬取的数据做相关保存
def get_tencent_data():
    url1 = urlConf["disease_h5"]
    url2 = urlConf["disease_other"]
    headers = {
        "user-agent": random4agent()
    }
    r1 = requests.get(url1, headers)
    r2 = requests.get(url2, headers)

    res1 = json.loads(r1.text)
    res2 = json.loads(r2.text)

    data_all1 = json.loads(res1["data"])
    data_all2 = json.loads(res2["data"])

    history = {}
    for i in data_all2["chinaDayList"]:
        ds = "2020." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")  # 匹配时间
        ds = time.strftime("%Y-%m-%d", tup)  # 改变时间格式
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds] = {"confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead}
    for i in data_all2["chinaDayAddList"]:
        ds = "2020." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")  # 匹配时间
        ds = time.strftime("%Y-%m-%d", tup)  # 改变时间格式
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds].update({"confirm_add": confirm, "suspect_add": suspect, "heal_add": heal, "dead_add": dead})

    details = []
    update_time = data_all1["lastUpdateTime"]
    data_country = data_all1["areaTree"]
    data_province = data_country[0]["children"]
    for pro_infos in data_province:
        province = pro_infos["name"]
        for city_infos in pro_infos["children"]:
            city = city_infos["name"]
            confirm = city_infos["total"]["confirm"]
            confirm_add = city_infos["today"]["confirm"]
            heal = city_infos["total"]["heal"]
            dead = city_infos["total"]["dead"]
            details.append([update_time, province, city, confirm, confirm_add, heal, dead])
    return history, details


# details表格更新操作，通过对比当前最新的时间戳更新数据表
# 如果时间戳最新，即显示数据已是最新数据无须在更新等
def update_details():
    try:
        mysqlDB = OPMysql()
        li = get_tencent_data()[1]  # 1代表最新数据
        conn, cursor = mysqlDB.get_conn()
        sql = "insert into details(update_time,province,city,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s,%s,%s)"
        sql_query = 'select %s=(select update_time from details order by id desc limit 1)'
        # 对比当前最大时间戳
        cursor.execute(sql_query, li[0][0])
        if not cursor.fetchone()[0]:
            # print(f"{time.asctime()}开始更新数据")
            for item in li:
                cursor.execute(sql, item)
            conn.commit()
            # print(f"{time.asctime()}更新到最新数据")
        else:
            # print(f"{time.asctime()}已是最新数据！")
            print("已是最新数据！")
    except:
        traceback.print_exc()
    finally:
        mysqlDB.dispose()


# 通过爬虫爬取的数据信息要不断的保存在我们的数据库表中
# 插入字段包括确诊数、治愈数、死亡人数等
def insert_history():
    try:
        mysqlDB = OPMysql()
        dic = get_tencent_data()[0]  # 0代表历史数据字典
        # print(f"{time.asctime()}开始插入历史数据")
        conn, cursor = mysqlDB.get_conn()
        sql = "insert into history values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for k, v in dic.items():
            cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
                                 v.get("suspect_add"), v.get("heal"), v.get("heal_add"),
                                 v.get("dead"), v.get("dead_add")])
        conn.commit()
        # print(f"{time.asctime()}插入历史数据完毕")
    except:
        traceback.print_exc()
    finally:
        mysqlDB.dispose()


# 更新历史数据，将数据存入history数据表中
def update_history():
    try:
        mysqlDB = OPMysql()
        dic = get_tencent_data()[0]  # 0代表历史数据字典
        # print(f"{time.asctime()}开始更新历史数据")
        conn, cursor = mysqlDB.get_conn()
        sql = "insert into history values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select confirm from history where ds=%s"
        for k, v in dic.items():
            if not cursor.execute(sql_query, k):
                cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
                                     v.get("suspect_add"), v.get("heal"), v.get("heal_add"),
                                     v.get("dead"), v.get("dead_add")])
        conn.commit()
        # print(f"{time.asctime()}历史数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        mysqlDB.dispose()


# 更新热搜数据，将数据存入hotsearch数据表中
def update_hotsearch():
    try:
        mysqlDB = OPMysql()
        context = get_sina_hot()
        # print(f"{time.asctime()}开始更新数据")
        conn, cursor = mysqlDB.get_conn()
        sql = "insert into hotsearch(dt,content) values(%s,%s)"
        ts = time.strftime("%Y-%m-%d %X")
        for i in context:
            cursor.execute(sql, (ts, i))
        conn.commit()
        # print(f"{time.asctime()}数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        mysqlDB.dispose()
