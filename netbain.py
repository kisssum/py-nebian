from requests_html import HTMLSession
import os
import time

# 网站URL
baseUrl = 'http://pic.netbian.com/'
headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
    }

# 分栏链接
columnUrls = [
    ['风景', baseUrl+'4kfengjing'],
    ['美女', baseUrl+'4kmeinv'],
    ['游戏', baseUrl+'4kyouxi'],
    ['动漫', baseUrl+'4kdongman'],
    ['影视', baseUrl+'4kyingshi'],
    ['明星', baseUrl+'4kmingxing'],
    ['汽车', baseUrl+'4kqiche'],
    ['动物', baseUrl+'4kdongwu'],
    ['人物', baseUrl+'4krenwu'],
    ['美食', baseUrl+'4kmeishi'],
    ['宗教', baseUrl+'4kzongjiao'],
    ['背景', baseUrl+'4kbeijing']
]

# 选择的栏目编号
columnIndex = 0

# 起始页
startPage = 1

# 爬取总页数
countPage = 1

# 文件保存目录
saveDir = os.getcwd()+'/pua/'

# 整页的下一级网页链接
nextUrls = []

# 整页的图片链接
imgsUrls = []


def UI():
    print('彼岸图网')
    for i in range(len(columnUrls)):
        print(str(i)+":"+columnUrls[i][0])


def ChoiceColumn():
    # 选择栏目
    print('选择栏目编号:', end='')
    try:
        index = int(input())
        if index < 0 or index >= len(columnUrls):
            print('栏目选择错误!')
            exit(0)
        else:
            return index
    except:
        print('栏目选择错误!')
        exit(0)


def ChoiceStartPage():
    # 起始页
    print('爬取起始页:', end='')
    try:
        index = int(input())
        if index < 1:
            print('起始页错误!')
            exit(0)
        else:
            return index
    except:
        print('起始页错误!')
        exit(0)


def ChoiceCountPage():
    # 爬取页数
    print('爬取页数:', end='')
    try:
        index = int(input())
        if index < 1:
            print('爬取页数错误!')
            exit(0)
        else:
            return index
    except:
        print('爬取页数错误!')
        exit(0)


def mkDir(path: str):
    try:
        # 创建目录
        if os.path.exists(path):
            print(path+' 目录已存在!')
        elif not os.path.exists(path):
            os.mkdir(path)
            print(path+' 目录创建成功！')
    except:
        print('创建目录失败！')
        exit(0)


def getNextUrlS(url):
    nextUrls = []

    # 解析网页并提取所有a节点
    r = HTMLSession().get(url,headers=headers).html.find('.slist a')

    # 获取完整链接
    for i in r:
        nextUrls.append(baseUrl+''.join(i.links)[1:])
        print(baseUrl+''.join(i.links)[1:])

    return nextUrls


def getImgUrls(urls):
    imgs = []

    for url in urls:
        r = HTMLSession().get(url,headers=headers).html.find('#img img')[0].attrs['src']
        imgs.append(baseUrl+r[1:])
        print(baseUrl+r[1:])

    return imgs


def downImg(url, savePath, interval):
    count = 0

    try:
        for i in range(len(url)):
            r = HTMLSession().get(url[i],headers=headers)
            path = savePath+str(i+1)+'.jpg'

            if not os.path.exists(path):
                with open(path, 'wb') as f:
                    f.write(r.content)
                print(path+' Ok！')
                count += 1
            else:
                print(path+' 已存在！')

            time.sleep(interval)
    except:
        print('保存失败!')
        exit(0)

    return count


def main():
    # UI
    UI()

    # 选择
    columnIndex = ChoiceColumn()
    startPage = ChoiceStartPage()
    countPage = ChoiceCountPage()

    # 创建主目录和栏目页
    print('创建主目录和栏目页')
    mkDir(saveDir)
    mkDir(saveDir+columnUrls[columnIndex][0])

    # 取链
    pageUrl = ''
    pageDir = ''
    interval = 100  # 爬取间隔
    imgCount = 0
    for page in range(startPage, startPage+countPage):
        # 页地址
        if page == 1:
            pageUrl = columnUrls[columnIndex][1]
        else:
            pageUrl = columnUrls[columnIndex][1]+'/index_'+str(page)+'.html'
        # 创建分页目录
        pageDir = saveDir+columnUrls[columnIndex][0]+'/'+str(page)+'/'
        mkDir(pageDir)
        # 获取下一级网页链接
        nextUrls = getNextUrlS(pageUrl)
        # 获取图片链接
        imgsUrls = getImgUrls(nextUrls)
        # 下载图片
        print('开始下载')
        imgCount += downImg(imgsUrls, pageDir, interval)

    print('爬取结束,共爬取'+str(imgCount)+'张')


if __name__ == '__main__':
    main()
