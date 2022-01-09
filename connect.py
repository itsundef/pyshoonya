import requests
import time
import pandas as pd
import hashlib
import json 

class pyShoonya(object):
    login_quick_auth = "https://shoonya.finvasia.com/NorenWClientWeb/QuickAuth"
    u_limits="https://shoonya.finvasia.com/NorenWClientWeb/Limits"
    u_positionbook="https://shoonya.finvasia.com/NorenWClientWeb/PositionBook"
    u_orderbook="https://shoonya.finvasia.com/NorenWClientWeb/OrderBook"
    u_holdings="https://shoonya.finvasia.com/NorenWClientWeb/Holdings"
    u_search="https://shoonya.finvasia.com/NorenWClientWeb/SearchScrip"
    u_scripinfo="https://shoonya.finvasia.com/NorenWClientWeb/GetSecurityInfo"
    u_placeorder="https://shoonya.finvasia.com/NorenWClientWeb/PlaceOrder"
    u_cancelorder="https://shoonya.finvasia.com/NorenWClientWeb/CancelOrder"
    u_headers = {
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
    
    def __init__(self,uid=None,pwd=None,factor2=None,sutok=None):
        self.uid=uid
        self.pwd=str(hashlib.sha256(pwd.encode()).hexdigest())
        self.factor2=factor2
        self.actid=None
        self.uname=None
        self.susertoken=None
        self.email=None
        
        
    def login(self):
        data='jData={"uid":"'+self.uid+'","pwd":"'+self.pwd+'","factor2":"'+self.factor2+'","apkversion":"1.2.0","imei":"e4aa28b6eefb872fbeb34e70943a578d","vc":"NOREN_WEB","appkey":"fe1447bd9e67d02e381dce43e1e79b5df44959dd325743316d6ae0d6fa23ca37","source":"WEB","addldivinf":"Chrome-96.0.4664.110"}'
        response = requests.post(self.login_quick_auth, headers=self.u_headers, data=data)
        x=json.loads(response.text)
        print(data)
        print(x)
        self.actid=x['actid']
        self.uname=x['uname']
        self.susertoken=x['susertoken']
        self.email=x['email']
        print("Logged In as {}({})".format(self.uname,self.email))
    
    def limits(self):
        data = 'jData={"uid":"'+self.uid+'","actid":"'+self.uid+'"}&jKey='+self.susertoken+''
        response = requests.post(self.u_limits, headers=self.u_headers, data=data)
        print(response.text)
    
    def searchscrip(self,s):
        data='jData={"uid":"'+self.uid+'","stext":"'+s+'"}&jKey='+self.susertoken
        response = requests.post(self.u_search, headers=self.u_headers, data=data)
        print(response.text)
        x=json.loads(response.text)
        return x['values'][0]['exch'],x['values'][0]['token'],x['values'][0]['tsym']
            
    def scripinfo(self,s):
        exch,token,tsym=self.searchscrip(s)
        data='jData={"uid":"'+self.uid+'","exch":"'+exch+'","token":"'+token+'"}&jKey='+self.susertoken
        response = requests.post(self.u_scripinfo, headers=self.u_headers, data=data)
        print(response.text)
        x=json.loads(response.text)
        return x['exch'],x['token'],x['values'][0]['tsym']
       
        
    def placeorder(self,s,t,q,p,prct,a,pr):
        exch,token,tsym=self.searchscrip(s)
        qty=q    
        prc=p    #acceptablevalues 0 for market orders 
        prctyp=prct
        prd=pr   #MARGIN OR CASH acceptablevalues M,C 
        typ=t     #acceptablevalues B,S 
        ret="DAY" #acceptablevalues DAY,IOC 
        amo=a or "True" #acceptablevalues Yes,No 
        data='jData={"uid":"'+self.uid+'","actid":"'+self.uid+'","exch":"'+exch+'","tsym":"'+tsym+'","qty":"'+qty+'","prc":"'+prc+'","prd":"'+prd+'","trantype":"'+typ+'","prctyp":"'+prctyp+'","ret":"'+ret+'","amo":"'+amo+'","ordersource":"WEB"}&jKey='+self.susertoken
        response = requests.post(self.u_placeorder, headers=headers, data=data)
        print(response.text)
        
             
    def orderbook(self):
        data='jData={"uid":"'+self.uid+'"}&jKey='+self.susertoken
        response = requests.post(self.u_orderbook, headers=self.u_headers, data=data)
        x=json.loads(response.text)
        df=pd.DataFrame.from_dict(x)
        return df

    def positions(self):
        data='jData={"uid":"'+self.uid+'","actid":"'+self.uid+'"}&jKey='+self.susertoken
        response = requests.post(self.u_positionbook, headers=self.u_headers, data=data)
        x=json.loads(response.text)
        print(x)
        df=pd.DataFrame(x, index=[0])
        return df
    
    def cancel(self,ordno):
        data='jData={"uid":"'+self.uid+'","norenordno":"'+ordno+'","ordersource":"WEB"}&jKey='+self.susertoken
        response = requests.post(self.u_cancelorder, headers=self.u_headers, data=data)
        print(response.text)
        
    def cancelAll(self):
        df=self.orderbook()
        for x in df.iloc[:,1]:
            self.cancel(x)
        return self.orderbook()
        
        
        
        
        
tes=pyShoonya('#UID','#PASSWORD','#DOB_PAN')
tes.login()
tes.limits()
tes.placeorder("BANKNIFTY27JAN22F","B","25","37900","LMT","No","M")
tes.placeorder("RELIANCE","B","1","0","MKT","Yes","M")
tes.orderbook()
tes.positions()
tes.cancelAll()





