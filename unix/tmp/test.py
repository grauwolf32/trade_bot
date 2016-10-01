import requests
import json
import MySQLdb
import string
from optparse import OptionParser

db = MySQLdb.connect(host="localhost", user="tradebot", passwd="tradeb0t", db="trade_data", charset='utf8')
cursor = db.cursor()

def main():
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
    
    body = ""
    for inst in instruments:
        body += "instrument: %s  size: %f\n"%(inst,info[inst]['size'])
        for date in dates[inst]:
            body += """date: %s start time: %s stop time: %s bid: %f ask: %f number of records: %d\n""" % \
                  (date,info[inst][date]['mintime'],info[inst][date]['maxtime'],info[inst][date]['avgbid'],\
                  info[inst][date]['avgask'],info[inst][date]['n_records']) 

    html = "<html><head><title>%s</title><head><body>\n%s\n</body></html>" % ("Info",body)
    print html

if __name__ == "__main__":
    main()
