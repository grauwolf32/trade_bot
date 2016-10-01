import requests
import json
import MySQLdb
import string
from optparse import OptionParser

def main():
    db = MySQLdb.connect(host="localhost", user="tradebot", passwd="tradeb0t", db="trade_data", charset='utf8')
    cursor = db.cursor()
    instruments = ['AUD_JPY','AUD_USD','EUR_AUD','EUR_CHF','EUR_GBP','EUR_JPY','EUR_USD','GBP_CHF','GBP_JPY','GBP_USD','NZD_USD','USD_CAD','USD_CHF','USD_JPY']
    values = ['instrument','date,time','milsec','bid','ask']
    params = '(id int NOT NULL  AUTO_INCREMENT,instrument VARCHAR(16), date DATE, time TIME, milsec FLOAT ZEROFILL, bid FLOAT ZEROFILL, ask FLOAT ZEROFILL, PRIMARY KEY (id))'

    for i in instruments:
        sql = "create table " + str(i) + " " + params + ";"
	print sql
	try:
            cursor.execute(sql)
            db.commit()
        except:
	    print "[SQL ERROR]"
            continue

	sql = "create index creation_date ON %s (date);" % (str(i))
	print sql
	try:
            cursor.execute(sql)
            db.commit()
        except:
	    print "[SQL ERROR]"
            pass
        print "\n"
	

if __name__ == '__main__':
    main()


