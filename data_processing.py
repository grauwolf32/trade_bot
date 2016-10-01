import requests
import json
import MySQLdb
import string
import csv
import numpy as np

db = MySQLdb.connect(host="localhost", user="tradebot", passwd="tradeb0t", db="trade_data", charset='utf8')
cursor = db.cursor()

def main():
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
