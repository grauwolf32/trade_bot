import requests
import json
import MySQLdb
import string
from optparse import OptionParser

db = MySQLdb.connect(host="localhost", user="tradebot", passwd="tradeb0t", db="trade_data", charset='utf8')
cursor = db.cursor()

def main():
    sql = "select table_name,data_length,index_length from information_schema.tables where table_schema='trade_data';"
    cursor.execute(sql)
    mem_size = dict()
    result =  cursor.fetchall()
    for i in result:
        mem_size[str(i[0])] = dict()
        mem_size[str(i[0])] = float(int(i[1]) + int(i[2])) / 1024/1024
        print mem_size[str(i[0])]
if __name__ == "__main__":
    main()
