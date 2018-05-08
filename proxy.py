import requests
from bs4 import BeautifulSoup
import re
import pymongo
import json
import time
# web = requests.get('https://www.taobao.com',proxies={'http':'121.232.147.64:9000'})
# print(web.status_code)
class proxy():
    status_ok = 'ok'
    status_error = 'error'
    status_ready = 'ready_check'
    def __init__(self,db,collection):

        self.client = pymongo.MongoClient(host='localhost',port = 27017)
        self.Client = self.client.test
        self.db = self.Client[collection]

    def get_ip_port(self,url):
        '''获取快代理页面上的ip地址放入数据库,状态为ready_check'''#
        self.web = requests.get(url)
        self.soup = BeautifulSoup(self.web.text,'lxml')
        self.getIP = self.soup.find_all('td',{'data-title':'IP'})
        self.getPORT = self.soup.find_all('td',{'data-title':'PORT'})
        print(url)
        for self.ip,self.port in zip(self.getIP,self.getPORT):
            # self.get_ip = self.ip.text
            # self.get_port = self.port.text
            self.ip_port = self.ip.text+':'+self.port.text
            # self.ip_port = self.get_ip+':'+self.get_port
            print(self.ip_port)
            try:
                self.db.insert_one({'_id':self.ip_port,'Status':self.status_ready})
            except pymongo.errors.DuplicateKeyError:
                print('重复ip，不添加')
                continue

    def pop_ip(self):
        '''读取'ready_check'的ip地址，生成列表'''
        # query = {}
        # query['Status'] = 'ready_check'
        cursor = self.db.find({'Status':'ready_check'})
        result = []
        for i in cursor:
            result.append(i['_id'])
        return result

    def ok_ip_pool(self):
        cursor = self.db.find({'Status':self.status_ok})
        result_ok = []
        for i_ok in cursor_ok:
            result.append(i_ok['_id'])
        return result_ok

    def check_ip(self,list):
        '''检测ip将状态200的ip地址更新为ok，其余删除'''
        for ip_address in list:
            try:
                self.req = requests.session()
                test_url = 'https://www.baidu.com'
                web_1 = self.req.get(test_url,proxies={'http':list},timeout=3)
                if web_1.status_code == 200:
                    self.db.update({'_id':ip_address},{'$set':{'Status':self.status_ok}})
                    print(ip_address+'        IP地址正常')
            except:
                self.db.update({'_id':ip_address},{'$set':{'Status':self.status_error}})
                print(ip_address+'        无法连接')

    def ok_count(self):
        '''获取可用和失效的数量'''
        ok = self.db.find({'Status':self.status_ok}).count()
        err = self.db.find({'Status':self.status_error}).count()
        return ok,err

    def reset(self):
        '''每次启动检测都重置所有状态为ready_check,multi=Ture为多条数据更新'''
        self.db.update({'Status':self.status_ok},{'$set':{'Status':self.status_ready}},multi=True)
        # self.db.find_and_modify({query={'Status':self.status_ok}})
    def closeDB(self):
        self.db.close()
    def clear(self):
        '''删库'''
        self.db.drop()
    def get_xs_proxy(self,url):
        '''获取快代理页面上的ip地址放入数据库,状态为ready_check'''
        base_url = 'http://www.xsdaili.com'#
        now = '%s年%s月%s日'%(time.strftime('%Y'),time.strftime('%m'),time.strftime('%d'))
        self.web = requests.get(url)
        self.web.encoding = 'utf-8'
        today = re.compile(r'<a href="(.*)">%s.*?</a>'%now)
        find_today = today.findall(self.web.text)
        for i in find_today:
            full = base_url + i
            ipweb =requests.get(full)
            ipweb.encoding = 'utf-8'
            re_ip = re.compile(r'\d{3}.\d{3}.\d{3}.\d{3}:')
            get_ipadress = re_ip.findall(ipweb.text)
            print(get_ipadress)


        # self.getIP = self.soup.find('cont')
        # print(self.getIP)
        # for self.ip,self.port in zip(self.getIP,self.getPORT):
        #
        #     self.ip_port = self.ip.text+':'+self.port.text
        #
        #     print(self.ip_port)
        #     try:
        #         self.db.insert_one({'_id':self.ip_port,'Status':self.status_ready})
        #     except errors.DuplicateKeyError:
        #         print('重复ip，不添加')
        #         continue
# if __name__ == '__main__':
#     proxy_go = proxy('test','ip_pool')
#
#     proxy_go.get_ip_port('https://www.kuaidaili.com/free/inha/1/')
#     time.sleep(5)
#     proxy_go.get_ip_port('https://www.kuaidaili.com/free/intr/1/')
#
#     list = proxy_go.pop_ip()
#     proxy_go.check_ip(list)
