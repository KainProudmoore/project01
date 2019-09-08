from lxml import html
def parse():
    """使用xpath语法解析本地html页面"""
    with open('index.html','r',encoding='utf-8') as f:
        html_data = f.read()
        selector = html.fromstring(html_data)
        h1 = selector.xpath('//div[@class="dl_sum"]/dl/dd/span/a')
        print(len(h1))
        for i in h1:
            mubiao = i.xpath('text()')
            print(mubiao)
parse()
