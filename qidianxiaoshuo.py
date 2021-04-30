import requests,os
import re
from lxml import etree
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5383.400 QQBrowser/10.0.1313.400'}


#获取章节目录和链接
def getbookurls(url):
    charpters = requests.get(url, headers=headers)
    objects = etree.HTML(charpters.text)
    bookname = objects.xpath('/html/body/div/div[6]/div[1]/div[2]/h1/em/text()')[0]
    objs=objects.xpath("//ul[@class='cf']/li")
    tinybox=[]
    for obj in objs:
        try:
            charpnames=obj.xpath('a/text()')[0]
            charpurls=obj.xpath('a/@href')[0]
            info={
                'bookname':bookname,
                'charpnames':charpnames,
                'charpurls':'https:'+charpurls
            }
            tinybox.append(info)
            # print(charpnames,charpurls)
        except:
            pass
    return tinybox

#获取小说内容
def getcontent(url):
    content = requests.get(url, headers=headers)
    objects = etree.HTML(content.text)
    objs=objects.xpath("//div[@class='read-content j_readContent']/p/text()")
    neirong=[]
    for obj in objs:
        #obj=obj.replace('\u3000\u3000','')
        obj = re.sub( '\s+', '\r\n\t', obj)
        #print(obj,end='')
        neirong.append(obj)
    return neirong


def main(url):

    get=getbookurls(url)

    for g in get:
        charptername= g['charpnames'].strip()
        bookname = g['bookname'].strip()
        print(g['charpnames'],'下载完成')
        # 如果目录不存在就创建
        if not os.path.exists(bookname):
            os.makedirs(bookname)
        bs=getcontent(g['charpurls'])
        with open('%s/%s.txt' % (bookname, charptername), 'a',encoding='utf-8') as f:
            for b in bs:
                f.write(b)
    print("全部下载完成!!!")

if __name__ == '__main__':
    url = input('请输入小说链接：')
    main(url)