'''
          cloudminingstatus.py 

@summary: Show selected API data from cloudhasher and miningpool.

@author:  Andreas Krueger
@since:   12 Feb 2017
@contact: https://github.com/drandreaskrueger
@copyright: @author @since @license
  
@license: Donationware, see README.md. Plus see LICENSE.
@version: v0.1.0
@status:  It is working well.
@todo:    Make it into webservice?
 
'''
from __future__ import print_function
import time
import sys
import pprint
import requests  # pip install requests

SLEEP_SECONDS= 5*60
SHOW_COMPOSITE_RESULTS = True

try:
    from credentials_ME import POOL_API_USERNAME, HASHER_API_ID, HASHER_API_KEY
except:
    from credentials import POOL_API_USERNAME, HASHER_API_ID, HASHER_API_KEY

POOL_API_URL="http://soil.miners-zone.net/apisoil/accounts/%s"

HASHER_ORDERS_API_URL="https://www.nicehash.com/api?method=orders.get&my&algo=20&location=0&id=%s&key=%s"
HASHER_BALANCE_API_URL="https://www.nicehash.com/api?method=balance&id=%s&key=%s" # unused

def humanTime(epoch):
    return time.strftime("GMT %H:%M:%S %a %d %b %Y", time.gmtime(epoch))

POOL_JSON=[('currentHashrate', (lambda x: "%6.2f MHash/s 30m average" % (x/1000000.0))),
           ('hashrate'       , (lambda x: "%6.2f MHash/s  3h average" % (x/1000000.0))),
           ('paymentsTotal'  , (lambda x:x)),
           ('stats'   , (lambda x: "%10.4f SOIL paid" % (float(x['paid'])/1000000000))),
           ('stats'   , (lambda x: "%10.4f SOIL balance" % (float(x['balance'])/1000000000))),
           ('24hreward',(lambda x: "%10.4f SOIL" % (float(x)/1000000000))),
           ('stats'   , (lambda x: "%d blocksFound" % (x['blocksFound']))),
           ('stats'   , (lambda x: "%s lastShare" % (humanTime(x['lastShare'])))),
           ('workers' , (lambda x: "%s last beat" % (humanTime(x['0']['lastBeat'])))),
           ('workers' , (lambda x: "%s Online" % (not bool(x['0']['offline'])))),
           ('workersTotal', (lambda x:x)),
           ]

HASHER_JSON_PATH=('result', 'orders', 0)
HASHER_JSON=[             
             ('alive',     (lambda x: x)),
             ('workers',   (lambda x: x)),
             ('id',        (lambda x: x)),
             ('pool_host', (lambda x: x)),
             ('pool_user', (lambda x: x)),
             ('limit_speed',    (lambda x: "%6.2f MHash/s" % (float(x)*1000))),
             ('accepted_speed', (lambda x: "%6.2f MHash/s" % (float(x)*1000))),
             ('btc_paid',  (lambda x: x)),
             ('btc_avail', (lambda x: x)),
             ('price',     (lambda x: "%s BTC/GH/Day" % x)),
             ('end',       (lambda x: "%4.2f days order lifetime" % (x/1000.0/60/60/24))),
             ]


def getJsonData(url):
    """
    get url, check for status_code==200, return as json
    """
    try:
        r=requests.get(url)
    except Exception as e:
        print ("no connection: ", e)
        return False
    if r.status_code != 200:
        print ("not answered OK==200, but ", r.status_code)
        return False
    try:
        j=r.json()
    except Exception as e:
        print ("no json, text:")
        print (r.text)
        # raise e
        return False
    return j

def showPoolData(url):
    """
    gets all json data from pool, but shows only what is in POOL_JSON 
    """
    print ("Pool:")
    j=getJsonData(url)
    if not j: 
        return False
    # pprint.pprint (j)
    for Jkey, Jfn in POOL_JSON:
        print (Jfn(j[Jkey]), "(%s)" % Jkey)
    return j
    
def showHasherData(url):
    """
    gets all json data from cloudhasher, but shows only what is in HASHER_JSON
    """
    
    print ("CloudHasher:")
    j=getJsonData(url)
    if not j: 
        return False
    # pprint.pprint (j)
    
    # climb down into the one branch with all the interesting data:
    j=j [HASHER_JSON_PATH[0]] [HASHER_JSON_PATH[1]] [HASHER_JSON_PATH[2]]
    
    # pprint.pprint (j)
    for Jkey, Jfn in HASHER_JSON:
        print (Jfn(j[Jkey]), "(%s)" % Jkey)
        
    estimate = (float(j['btc_avail']) / ( float(j['price'])*float(j['accepted_speed'])) )
    print ("%.2f days" % estimate, end='')
    print ("(remaining btc / order price / hashrate)")
    return j


def showCompositeResults(pooldata, hasherdata):
    """
    Estimates a coin prices by money spent versus money mined.
    N.B.: In this form probably only be roughly correct 
    during first buy order? We'll see.
    """
    coinsMined = float(pooldata['stats']['paid'])
    coinsMined += float(pooldata['stats']['balance'])
    coinsMined /= 1000000000
    hashingCostsBtc = float(hasherdata['btc_paid'])
    satoshiPrice = hashingCostsBtc / coinsMined * 100000000
    print ("%.1f Satoshi/SOIL (mining price approx)" % satoshiPrice)
    return satoshiPrice

def loop(sleepseconds):
    """
    Shows both, then sleeps, the repeats.
    """
    
    while True:
        print ()
        pooldata=showPoolData(url=POOL_API_URL%POOL_API_USERNAME)
        print ()
        hasherdata=showHasherData(url=HASHER_ORDERS_API_URL%(HASHER_API_ID, HASHER_API_KEY))
        print ()
        if SHOW_COMPOSITE_RESULTS and pooldata and hasherdata:
            showCompositeResults(pooldata, hasherdata)
            print ()
        print (humanTime(time.time()), end='') 
        print ("... sleep %s seconds ..." % sleepseconds)
        time.sleep(sleepseconds)
    
def checkCredentials():
    """
    See credentials.py
    """
    yourCredentials=(POOL_API_USERNAME, HASHER_API_ID, HASHER_API_KEY)
    if "" in yourCredentials: 
        print ("You must fill in credentials.py first.")
        print (yourCredentials)
        return False
    else:
        return True

if __name__ == '__main__':
    if not checkCredentials():
        sys.exit()
    try:
        loop(sleepseconds=SLEEP_SECONDS)
    except KeyboardInterrupt:
        print ("Bye.")
        sys.exit()
    
    
    