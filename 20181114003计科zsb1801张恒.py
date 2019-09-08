import requests
import time #时间类库，这里我用来做爬虫休眠
import jieba #jieba库做字符分词
from wordcloud import WordCloud #词云分析库，用于生成词云
from lxml import html #解析HTML文件时需要使用
from matplotlib import pyplot as plt #调用数学类库，用于生成柱状图
import pandas as pd
import imageio
mask = imageio.imread('new1.jpg') #词云的形状图
movie_list = []
# 做网页解析提交网页源码函数
def link_info(url):
    resp = requests.get(url)
    html_data = resp.text
    return html_data  #返回网页源码
#具体的爬虫程序
def spider(isbn):#传入的网站参数
    url = 'https://movie.douban.com/cinema/later/{}/'.format(isbn)
    print(url)
    # 使用requests进行http请求然后获取网页的源代码

    selector = html.fromstring(link_info(url))
    ul_list = selector.xpath('//div[@id="showing-soon"]/div')
    print('即将上映的电影有:',len(ul_list),'部')  #输出爬出了多少倍电影，计算列表长度
    for li in ul_list:
        # 电影名称
        title = li.xpath('div[@class="intro"]/h3/a/text()')[0]
        # print(title)

        #上映日期
        date = li.xpath('div[@class="intro"]/ul/li[1]/text()')[0]
        # print(date)
        # 地区
        space = li.xpath('div[@class="intro"]/ul/li[3]/text()')[0]
        # print(space)

        # 想看人数
        numbers = li.xpath('div[@class="intro"]/ul/li[4]/span/text()')
        numbers = '0' if len(numbers) == 0 else numbers[0]
        numbers = numbers.replace('人想看','') #将标签里面的数据修改，不需要“人想看”这段数据
        #电影的详细介绍页面
        to_link = li.xpath('a[@class="thumb"]/@href')[0]

        # 存储形式[{},{},{}]
        movie_list.append({
            "title": title,
            "date": date,
            "space": space,
            "numbers": numbers,
            "link":to_link
        })

    # 按照想看人数进行排序 [{},{}]
    movie_list.sort(reverse=True,key=lambda x : float(x['numbers']))
    #输出元组中的每一个元素，每一个元素里都存放一个具体的电影信息，for循环遍历输出
    for movie in movie_list:
        print(movie)

    print("---------------------------------------------------")
    df = pd.DataFrame(movie_list)
    df.to_excel('movie.xls')  #存入excel表格中

    # x ，y 轴
    price_x = [float(i['numbers']) for i in movie_list[:5]]   #排序前5的想看人数
    print(price_x)
    store_y = [i['title'] for i in movie_list[:5]]   #排序前5的电影名称
    print(store_y)
    newlink = [i['link'] for i in movie_list[:5]]   #排序前5电影的具体页面链接
    # print(newlink)

    temp=1
    add = 'comments?status=F'   #详细短评页面链接的同一后缀
    for x in newlink:     #遍历前5电影的具体信息页面网址
        x = x+add           #将详细短评的统一后缀加上去，那么网址就会链向详细短评
        newread = html.fromstring(link_info(x))        #对目标网站做请求和返回源码
        review_list = newread.xpath('//div[@id="comments"]/div[@class="comment-item"]')  #将每个短评的真个标签存入列表当中
        DuanPs = ''  #定义一个字符串
        for tag in review_list:  #tag遍历一个电影的每个短评，然后将每个短评拼接起来
            DuanP = tag.xpath('div[@class="comment"]/p/span/text()')[0]
            DuanPs = DuanPs+DuanP    #拼接
        words = jieba.lcut(DuanPs)   #jieba分词，将拼接后的字符串分成单个的词汇
        cloud_word = []     #定义一个列表

        for word in words:     #筛选符合长度的词语，并存入列表当中
            if len(word) == 1:
                continue
            else:
                cloud_word.append(word)
        cloud_text = " ".join(cloud_word)   #用空格链接列表当中的每一个元素，并赋给字符串cloude_text
        print(cloud_text)
        wc = WordCloud(
            width=800,
            height=600,
            background_color='white',
            font_path='msyh.ttc',
            mask=mask
        ).generate(cloud_text)    #词云的属性配置，以及生成词云
        file = 'movie_wordcloud'+str(temp)+'.png'   #将词云结果存入文件movie_wordcloud$.png当中，$随变量变化
        wc.to_file(file)
        temp = temp+1               #变量数值加1
        time.sleep(0.5)              #爬虫程序休眠0.5秒
        print("--------------------------------------------------------------")

    # 绘制
    plt.rcParams["font.sans-serif"] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.barh(store_y,price_x )
    plt.show()

isbn  = input('请输入查询电影的所在城市：')
spider(isbn)
