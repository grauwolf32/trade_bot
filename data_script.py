"""
Demonstrates streaming feature in OANDA open api
To execute, run the following command:
python streaming.py [options]
To show heartbeat, replace [options] by -b or --displayHeartBeat
"""

import requests
import json
import MySQLdb
import string

from optparse import OptionParser

db = MySQLdb.connect(host="localhost", user="tradebot", passwd="tradeb0t", db="trade_data", charset='utf8')
cursor = db.cursor()

def connect_to_stream():
    """
    Environment           <Domain>
    fxTrade               stream-fxtrade.oanda.com
    fxTrade Practice      stream-fxpractice.oanda.com
    sandbox               stream-sandbox.oanda.com
    """

    # Replace the following variables with your personal ones
    domain = 'stream-fxpractice.oanda.com'
    access_token = '8613c60f8e33893978070805176f817d-694984dc25b3ff9087605fe364be7df3'
    account_id = '9924627'
    instruments = "AUD_JPY,AUD_USD,EUR_AUD,EUR_CHF,EUR_GBP,EUR_JPY,EUR_USD,GBP_CHF,GBP_JPY,GBP_USD,NZD_USD,USD_CAD,USD_CHF,USD_JPY"

    try:
        s = requests.Session()
        url = "https://" + domain + "/v1/prices"
        headers = {'Authorization' : 'Bearer ' + access_token,
                   # 'X-Accept-Datetime-Format' : 'unix'
                  }
        params = {'instruments' : instruments, 'accountId' : account_id}
        req = requests.Request('GET', url, headers = headers, params = params)
        pre = req.prepare()
        resp = s.send(pre, stream = True, verify = False)
        return resp
    except Exception as e:
        s.close()
        print "Caught exception when connecting to stream\n" + str(e) 

def demo(displayHeartbeat):
    response = connect_to_stream()
    if response.status_code != 200:
        print response.text
        return
    for line in response.iter_lines(1):
        if line:
            try:
                msg = json.loads(line)
            except Exception as e:
                print "Caught exception when converting message into json\n" + str(e)
                return

            if msg.has_key("tick"):
                instrument = msg["tick"]["instrument"]
                time = msg["tick"]["time"]
                bid = msg["tick"]["bid"]
                ask = msg["tick"]["ask"]
                #print "instr : %(instrument)s time : %(time)s \n bid : %(bid)f ask : %(ask)"%{"instrument":instrument,"time":time,"bid":bid,"ask":ask}
                date = time[0:10]
                clock = time[11:19]
                milsec = float(time[19:-1])
                sql = """INSERT INTO %(instrument)s(instrument,date,time,milsec,bid,ask)
                VALUES ('%(instrument)s','%(date)s','%(time)s','%(milsec)f','%(bid)f','%(ask)f')
                """%{"instrument":instrument,"date":date,"time":clock,"milsec":milsec,"bid":bid,"ask":ask}
                print sql
                cursor.execute(sql)
                db.commit()
                
def main():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-b", "--displayHeartBeat", dest = "verbose", action = "store_true", 
                        help = "Display HeartBeat in streaming data")
    displayHeartbeat = False

    (options, args) = parser.parse_args()
    if len(args) > 1:
        parser.error("incorrect number of arguments")
    if options.verbose:
        displayHeartbeat = True
    demo(displayHeartbeat)


if __name__ == "__main__":
    main()
