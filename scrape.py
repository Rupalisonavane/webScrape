import requests
from bs4 import BeautifulSoup
import time
import csv
import send_mail
from datetime import date

urls = ["https://finance.yahoo.com/quote/AMZN?p=AMZN&.tsrc=fin-srch","https://finance.yahoo.com/quote/GOOG?p=GOOG&.tsrc=fin-srch","https://finance.yahoo.com/quote/MSFT?p=MSFT&.tsrc=fin-srch"]
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}

Todays=str(date.today())+".csv"
csv_file=open(Todays,"w")
csv_writer=csv.writer(csv_file)
csv_writer.writerow(['Stock Name','currency price','Previous Close','Open','Bid','Ask','Days Range','52 Week Range','volume','Avg.Volume'])
 
for url in urls:
    stock=[]
    html_page = requests.get(url,headers=headers)
    soup = BeautifulSoup(html_page.content,'lxml')
    
    headers_info= soup.find_all("div",id="quote-header-info")[0]
    stock_title=headers_info.find("h1").get_text()
    current_value = headers_info.find("div",class_="My(6px) Pos(r) smartphone_Mt(6px)").find("span").get_text()
 
    stock.append(stock_title)
    stock.append(current_value)

    table_info = soup.find_all("div",class_="D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)")[0].find_all("tr")
    
    for i in range(0,8):
       
        value=table_info[i].find_all("td")[1].get_text()
        stock.append(value)
    csv_writer.writerow(stock)
    time.sleep(5)
send_mail.send(filename=Todays)
csv_file.close()
