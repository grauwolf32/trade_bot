import csv
import requests
import json
import MySQLdb
import string
import time
import os
from flask import Flask, render_template

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'template')
application = Flask(__name__, template_folder=template_path)

db = MySQLdb.connect(host="localhost", user="tradebot", passwd="tradeb0t", db="trade_data", charset='utf8')
cursor = db.cursor()

@application.route("/")
def hello():
    return render_template("index.html",title="Yahoo!",paragraph=["How cool!"])

@application.route('/info')
def aboutpage():
    try:
        sql = "SHOW TABLES;"
        cursor.execute(sql)
        tables =  cursor.fetchall()
        instruments = [str(i[0]) for i in tables]
        dates = dict()

        sql = "SELECT table_name,data_length,index_length FROM information_schema.tables WHERE table_schema='trade_data';"
        cursor.execute(sql)
        mem_size = dict()
        result =  cursor.fetchall()
        for i in result:
            mem_size[str(i[0])] = dict()
            mem_size[str(i[0])] = float(int(i[1]) + int(i[2])) / 1024/1024

        for inst in instruments:
            sql = "SELECT DISTINCT(date) from %s;" % (inst)
            cursor.execute(sql)
            result =  cursor.fetchall()
            dates[inst] = [str(i[0]) for i in result]

        info = dict()
        for inst in instruments:
            info[inst] = dict()
            for date in dates[inst]:
                info[inst][date] = dict()
                sql = "SELECT MIN(time),MAX(time) from %s WHERE date='%s';"% (inst,date)
                cursor.execute(sql)
                daily_time = cursor.fetchall()
                info[inst][date]['mintime'] = str(daily_time[0][0])
                info[inst][date]['maxtime'] = str(daily_time[0][1])
                sql = "SELECT MIN(bid),AVG(bid),MAX(bid),MIN(ask),AVG(ask),MAX(ask) from %s where date = '%s'"%(inst,date)
                cursor.execute(sql)
                statistics = cursor.fetchall()
                info[inst][date]['minbid'] = float(statistics[0][0])
                info[inst][date]['avgbid'] = float(statistics[0][1])
                info[inst][date]['maxbid'] = float(statistics[0][2])
                info[inst][date]['minask'] = float(statistics[0][3])
                info[inst][date]['avgask'] = float(statistics[0][4])
                info[inst][date]['maxask'] = float(statistics[0][5])
                sql = "SELECT COUNT(id) from %s where date='%s';"%(inst,date)
                cursor.execute(sql)
                n_records =  cursor.fetchall()
                info[inst][date]['n_records'] = int(n_records[0][0])
       
        for inst in instruments:
            info[inst]['size'] = mem_size[inst]
    
        return render_template("info.html", instruments=instruments,dates=dates,info=info)
    except Exception,e:
        return str(e)


@application.route('/about/contact')
def contactPage():

    title = "About this site"
    paragraph = ["blah blah blah memememememmeme blah blah memememe"]

    pageType = 'about'

    return render_template("index.html", title=title, paragraph=paragraph, pageType=pageType)

def db_size():
    sql = """SELECT table_schema "database_name", sum( data_length + index_length )/1024/1024 
          "Data Base Size in MB" FROM information_schema.TABLES GROUP BY table_schema;"""

    cursor.execute(sql)
    data =  cursor.fetchall()
    return data

if __name__ == "__main__":
    application.run()
