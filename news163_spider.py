import requests
import json
import pandas
import re
import MySQLdb

# url = 'http://c.m.163.com/nc/article/headline/T1348647853363/0-100.html'

header = {
    'User-Agent': 'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)',
    'Connection': 'keep - alive',
}
conn = MySQLdb.connect('localhost', 'root', '123456', '163_news', charset="utf8", use_unicode=True)
cursor = conn.cursor()
news_total = []


# table_name = "1_domestic_news"
# catagory = "BA10TA81wangning"


def news163_connect(catagory, table_name):
    for n in range(0, 1):
        url_0 = 'https://3g.163.com/touch/reconstruct/article/list/{0}/{1}-10.html'.format(catagory, n)
        # url_1 = url_0
        mydata = requests.get(url_0, headers=header).text
        mydata1 = re.findall(r'[(](.*?)[)]', mydata)
        # print(len(mydata1))
        # print(mydata1[0])
        # wbdata = requests.get(url, headers=header).text
        # data = json.loads(wbdata)
        data = json.loads(str(mydata1[0]))
        news = data[catagory]

        for item in news:
            docid = item['docid']
            source = item['source']
            title = item['title']
            priority = item['priority']
            digest = item['digest']
            time = item['ptime']

            try:
                url = item['url']
            except:
                url = ''
            newes_data = {
                'title': title,  # '标题'
                'time': time,  # '时间'
                'source': source,  # '来源'
                'digest': digest,  # '内容'
                'url': url  # 链接'
            }
            # news_total.append(newes_data)

            # print(type(df))
            insert_sql = """ 
                        insert into {}(title, time, source, digest,url) VALUES (%s, %s, %s, %s, %s)
                        """.format(table_name)

            cursor.execute(insert_sql, (
                item['title'], item["ptime"], item["source"], item["digest"], item["url"]))

        print("第" + str(n) + "页爬取完毕\n")
    # df = pandas.DataFrame(news_total, columns=['title', 'time', 'source', 'digest', 'url'])
    # df.to_excel("news_net_all.xlsx")
    conn.commit()


kinds = [("BD29LPUBwangning", "01_domestic_news"),
         ("BD29MJTVwangning", "02_foreign_news"),
         ("BD2A86BEwangning", "03_tv_entertainment"),
         ("BD2A9LEIwangning", "04_movie_entertainment"),
         ("BD2AB5L9wangning", "05_star_entertainment"),
         ("BD2AC4LMwangning", "06_music_entertainment"),
         ("C2769L6Ewangning", "07_moviesongs_entertainment"),
         ("BA8E6OEOwangning", "08_sports"),
         ("BD2C01CQwangning", "09_stock_financing"),
         ("BD2C1904wangning", "10_fund_financing"),
         ("BD2C24VCwangning", "11_commerce_financing"),
         ("DE0E57UJwangning", "12_observing_car"),
         ("BA8DOPCSwangning", "13_news_car"),
         ("DE0CGUSJwangning", "14_military_situation"),
         ("DE0CE1U2wangning", "15_military_products"),
         ("D90S2KJMwangning", "16_science_technology"),
         ("D90S5T8Qwangning", "17_science_intelligence"),
         ("BV5U6ON6wangning", "18_iphone"),
         ("BV5U5EOVwangning", "19_android"),
         ("BAI6JOD9wangning", "20_digital"),
         ("BAI6RHDKwangning", "21_games"),
         ("E8UDIQP2lizhenzhen", "22_new_era")]

for (catagory, table_name) in kinds:
    news163_connect(catagory, table_name)
