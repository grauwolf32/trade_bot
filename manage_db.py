import requests
import argparse
import json
import MySQLdb
import string
import csv
import numpy as np

db = MySQLdb.connect(host="localhost", user="tradebot", passwd="tradeb0t", db="trade_data", charset='utf8')
cursor = db.cursor()

def show_instruments(db):
    cursor = db.cursor()
    sql = "SHOW TABLES"
    cursor.execute(sql)
    data =  cursor.fetchall()
    for i in data:
        print data

    return

def show_info(db,instruments):
    for inst in instruments:
    try:
        sql = "SELECT DISTINCT(date) from %s;" % (inst)
        cursor.execute(sql)
        dates =  cursor.fetchall()
	dates = [str(i[0]) for i in dates] #
        times = [] 
    
        for date in data:
	    sql = "SELECT MIN(time),MAX(time) from EUR_USD WHERE date=%s;"%(str(date[0]))
            cursor.execute(sql)
            daily_time = cursor.fetchall()
            
	    
            
     

def main():
    #parser = argparse.ArgumentParser(description='Database management instrument.')
    #parser.add_argument('--instruments', dest='accumulate', action='store_const', const=sum, default=max, help='sum the integers (default: find the max)')
    #parser.add_argument('--info', dest='accumulate', action='store_const', const=sum, default=max, help='sum the integers (default: find the max)')
    parser = argparse.ArgumentParser(description='Database management instrument.')
    subparsers = parser.add_subparsers()
    parser_info = subparsers.add_parser('info', help='Info about choosen currency')
    parser_info.add_argument('instrument',help='Currency name')
    parser_info.set_defaults(func=show_info)

    instruments = input("Instruments (['EUR_USD','GBP_USD']: ")
    date_start  = input("Date of start(yyyy-mm-dd): ")
    time_start  = input("Time start (hh:mm:ss): ")

    date_end    = input("Date of end(yyyy-mm-dd): ")
    time_end    = input("Time end (hh:mm:ss): ")
    
    for instrument in instruments:
        sql = """SELECT * FROM %(instrument)s WHERE time >= '%(time_start)s' AND time <= '%(time_end)s'
              AND date >= '%(date_start)s' AND date <= '%(date_end)s' 
              """%{"instrument":instrument,"time_start":time_start,"time_end":time_end,"date_start":date_start,"date_end":date_end}
        print sql
        cursor.execute(sql)
        data =  cursor.fetchall()
        
        csvfile = open(str(instrument)+".csv","wb") 
        csvfile.write("date,time,millsec,bid,ask,time_space, \n")
        time_space  = 0.0
        millsec_last = 0.0
        time_last   = ""

        for record in data:
            record_id,instrument,date,time,millsec,bid,ask = record

            if time_last == "":
                time_space = 0.0
            else:
               time_space += time.seconds - time_last.seconds + millsec - millsec_last

            csvfile.write("%(date)s,%(time)s,%(millsec)f,%(bid)f,%(ask)f,%(time_space)f, \n"%{"date":date,"time":time,"millsec":millsec,"bid":bid,"ask":ask,"time_space":time_space})
            time_last = time
            millsec_last = millsec    

if __name__ == "__main__":
    main()
