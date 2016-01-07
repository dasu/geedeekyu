#This is a proof of concept and BAD
import requests
import datetime
from bs4 import BeautifulSoup
import pymysql

def mysql(dt=None, total=None, action=None):
    connection = pymysql.connect(host='',user='', passwd='',db='', charset='utf8')
    cursor = connection.cursor()
    if action == 'select':
        sql = "select * FROM gdq2016 order by dt"
        cursor.execute(sql)
        res = cursor.fetchall()
        connection.close()
        return res
    if action == 'test':
        sql = "INSERT INTO gdq2016 (dt, total) VALUES (%s, %s) ON DUPLICATE KEY UPDATE total = total+%s"
        cursor.execute(sql, (dt, total, total))
        connection.commit()
    if action == 'test2':
        sql = "INSERT INTO Tgdq2016 (dt, total) VALUES (%s, %s) ON DUPLICATE KEY UPDATE total = %s"
        cursor.execute(sql, (dt, total, total))
        connection.commit()
    if action == 'truncate1':
        sql = "TRUNCATE gdq2016"
        cursor.execute(sql)
        connection.commit()
    if action == 'truncate2':
        sql = "TRUNCATE Tgdq2016"
        cursor.execute(sql)
        connection.commit
    if action == "delete":
        sql = "DELETE from Tgdq2016 where id < 5"
        cursor.execute(sql)
        connection.commit
    connection.close()
    
mysql(action="truncate1")
dt = ''
total = 0
i = 1
url = "https://gamesdonequick.com/tracker/donations/agdq2016?page={}".format(i)
x = requests.get(url)
while x.text.strip() != 'Server done blowed up':
    print("Page {}".format(i))
    bs = BeautifulSoup(x.content)
    for b in bs.body.findAll("table")[0].findAll("tr")[1:]:
        dt =  datetime.datetime.strptime(b.findAll("td")[1].text.strip(), "%m/%d/%Y %H:%M:%S %z")
        total = float(b.findAll("td")[2].text.strip().replace('$','').replace(',',''))
        mysql(dt, total, 'test')
    i+=1
    url = "https://gamesdonequick.com/tracker/donations/agdq2016?page={}".format(i)
    x = requests.get(url)
dt = ''
total = 0
mysql(action="truncate2")
res = mysql(action='select')
for don in res:
    dt = don[1]
    total += float(don[2])
    print ("{} {}".format(dt, total))
    mysql(dt,total,'test2')

mysql(action="delete")
