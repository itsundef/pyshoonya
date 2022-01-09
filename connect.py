import requests
import time

class pyShoonya(object):
    login_quick_auth = "https://shoonya.finvasia.com/NorenWClientWeb/QuickAuth"
    u_limits="https://shoonya.finvasia.com/NorenWClientWeb/Limits"
    u_positionbook="https://shoonya.finvasia.com/NorenWClientWeb/PositionBook"
    u_orderbook="https://shoonya.finvasia.com/NorenWClientWeb/OrderBook"
    u_holdings="https://shoonya.finvasia.com/NorenWClientWeb/Holdings"
    u_search="https://shoonya.finvasia.com/NorenWClientWeb/SearchScrip"
    u_scripinfo="https://shoonya.finvasia.com/NorenWClientWeb/GetSecurityInfo"
    u_placeorder="https://shoonya.finvasia.com/NorenWClientWeb/PlaceOrder"
    
    
    def __init__(self,uid=None,pwd=None,factor2=None,sutok=None):
        self.uid=uid
        self.pwd=pwd
        self.factor2=factor2
        self.actid=None
        self.uname=None
        self.susertoken=None
        self.email=None
        
    def login(self):
        headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'sec-ch-ua-platform': '"macOS"',
    'content-type': 'text/plain; charset=utf-8',
    'Accept': '*/*',
    'Origin': 'https://shoonya.finvasia.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://shoonya.finvasia.com/',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',}
        data='jData={"uid":"'+self.uid+'","pwd":"'+self.pwd+'","factor2":"'+self.factor2+'","apkversion":"1.2.0","imei":"e4aa28b6eefb872fbeb34e70943a578d","vc":"NOREN_WEB","appkey":"fe1447bd9e67d02e381dce43e1e79b5df44959dd325743316d6ae0d6fa23ca37","source":"WEB","addldivinf":"Chrome-96.0.4664.110"}'
        response = requests.post(self.login_quick_auth, headers=headers, data=data)
        x=json.loads(response.text)
        self.actid=x['actid']
        self.uname=x['uname']
        self.susertoken=x['susertoken']
        self.email=x['email']
        print("Logged In as {}({})".format(self.uname,self.email))
    
    def limits(self):
        data = 'jData={"uid":"'+self.uid+'","actid":"'+self.uid+'"}&jKey='+self.susertoken+''
        response = requests.post(self.u_limits, headers=headers, data=data)
        print(response.text)
    
    def searchscrip(self,s):
        data='jData={"uid":"'+self.uid+'","stext":"'+s+'"}&jKey='+self.susertoken
        response = requests.post(self.u_search, headers=headers, data=data)
        print(response.text)
        x=json.loads(response.text)
        return x['values'][0]['exch'],x['values'][0]['token'],x['values'][0]['tsym']
            
    def scripinfo(self,s):
        exch,token,tsym=self.searchscrip(s)
        data='jData={"uid":"'+self.uid+'","exch":"'+exch+'","token":"'+token+'"}&jKey='+self.susertoken
        response = requests.post(self.u_scripinfo, headers=headers, data=data)
        print(response.text)
        
    def placeorder(self,s,typ,qty,amo):
        #WIP
        exch,token,tsym=self.searchscrip(s)
        data='jData={"uid":"'+self.uid+'","actid":"'+self.uid+'","exch":"'+exch+'","tsym":"'+tsym+'","qty":"'+qty+'","prc":"'++'","prd":"M","trantype":"'+typ+'","prctyp":"'++'","ret":"'++'","amo":"'+amo+'","ordersource":"WEB"}&jKey='+self.susertoken
        
tes=pyShoonya('#UID','#HASHEDPWD','#DOB_PAN')
tes.login()
tes.limits()
tes.scripinfo("NIFTY13JAN22C17850")





