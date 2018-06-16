#coding=utf-8
import requests
from lxml import etree
import xlsxwriter
import json
import os
import xlsxwriter
import gevent
from gevent import monkey,pool   #导入协程库
monkey.patch_socket()   #猴子补丁

class Sina_gk():

    def __init__(self):
        self.header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
        self.i=0
        self.k=0

    def college_id_name(self):
        ar=[]
        url='http://kaoshi.edu.sina.com.cn/?p=college&s=api2015&a=getAllCollege'  #json格式所有大学id & name
        res=requests.get(url,self.header)
        res.encoding='utf-8'
        data=res.json()
        res.close()
        for i in range(1,33):  #共32个省级
            dic=data['data'][str(i)]['college']
            for k in dic.items():
                ar.append(k)   #大学id & name
        return ar

    def paser(self,college_id):
        gevent.sleep(2)
        url='http://college.edu.sina.cn/aj/collegegrade?&province=9&college={}&dep=2'.format(college_id[0])  #文科 dep=1,理科dep=2  province=9对应安徽
        ur='http://kaoshi.edu.sina.com.cn/college/c/{}.shtml'.format(college_id[0])
        print ur
        res=requests.get(url,self.header)
        data=res.json()
        for x in data['data']:
            for y in data['data'][x]:
                value=[ur,college_id[0],college_id[1],x,y['lowest'],y['average'],y['highest'],y['num'],y['batch']]
                for kk in range(0,9):
                    sheet.write(self.k,kk,value[kk])
                self.k+=1
        res.close()

if __name__=='__main__':
    gk=Sina_gk()
    lists=gk.college_id_name()
    xls=xlsxwriter.Workbook('gk_anhui.xlsx')
    sheet=xls.add_worksheet('sheet')
    th=[]
    p=pool.Pool(20)    #协程并发数20
    for l in lists:
        th.append(p.spawn(gk.paser,l))
    gevent.joinall(th,timeout=15)
    xls.close()