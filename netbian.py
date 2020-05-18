import requests
from lxml import etree
import os


class netbian(object):
    root = '/home/rull/Pictures'
    # 站点链接
    siteUrl = 'http://pic.netbian.com'
    # 分栏链接
    columnUrls = {
        'fengjing': 'http://pic.netbian.com/4kfengjing',
        'meinv': 'http://pic.netbian.com/4kmeinv',
        'youxi': 'http://pic.netbian.com/4kyouxi',
        'dongman': 'http://pic.netbian.com/4kdongman',
        'yingshi': 'http://pic.netbian.com/4kyingshi',
        'mingxing': 'http://pic.netbian.com/4kmingxing',
        'qiche': 'http://pic.netbian.com/4kqiche',
        'dongwu': 'http://pic.netbian.com/4kdongwu',
        'renwu': 'http://pic.netbian.com/4krenwu',
        'meishi': 'http://pic.netbian.com/4kmeishi',
        'zongjiao': 'http://pic.netbian.com/4kzongjiao',
        'beijing': 'http://pic.netbian.com/4kbeijing'
    }
    # 爬取图片总数
    imgCounts = 0
    # 开始页数
    startPage = 0
    # 爬取页数
    page = 0
    # 爬取栏目
    column = ''

    def __init__(self):
        print('栏目\n')
        for i in self.columnUrls:
            print(i)

        try:
            startpage = int(input("输入起始页:"))
            page = int(input("输入爬的页数:"))
            column = input('输入栏目:')
            self.sets(startpage, page, column)
            self.main()
        except:
            print('错误!')
            exit(0)

    def sets(self, startPage: int, page: int, column: str):
        self.startPage = startPage
        self.page = page
        self.column = column

    def main(self):
        # 爬取几页
        for i in range(self.startPage, self.startPage+self.page):
            # 下一级网页链接
            nextUrls = []
            # 图片链接
            imgUrls = []
            # 第几页网址
            pageUrl = self.columnUrls[self.column]

            if(i != 1):
                pageUrl = self.columnUrls[self.column]+'/index_'+str(i)+'.html'

            # 获取该页图片所有下级链接
            nextUrls = netbian.getThisPageAllUrls(self.siteUrl, pageUrl)

            # 获取该页面所有图片链接
            for nextUrl in nextUrls:
                imgUrls.append(netbian.getImgLink(self.siteUrl, nextUrl))

            # 下载图片
            self.imgCounts += netbian.downLoad(self.root + '/' +
                                               self.column+'/', imgUrls, i)

        print('爬取图片数:'+str(self.imgCounts))

    def getThisPageAllUrls(siteUrl: str, columnUrl: str):
        # 网页源代码
        r = requests.get(columnUrl)
        if(r.raise_for_status()):
            r.encoding = r.apparent_encoding

        # 提取链接
        html = etree.HTML(r.text)
        cUrls = html.xpath('/html/body/div[2]/div/div[3]/ul/li/a/@href')

        # 完善链接
        for i in range(len(cUrls)):
            cUrls[i] = siteUrl+cUrls[i]

        # 返回链接列表
        return cUrls

    def getImgLink(mainUrl: str, url: str):
        # 网页源代码
        r = requests.get(url)
        if(r.raise_for_status()):
            r.encoding = r.apparent_encoding

        # 提取链接
        html = etree.HTML(r.text)
        imgLink = html.xpath(
            '/html/body/div[2]/div[1]/div[2]/div[1]/div[2]/a/img/@src')

        # 返回图片链接
        return mainUrl+imgLink[0]

    def downLoad(root: str, imgLinks: list, page):
        # 判断root目录存在
        try:
            if not os.path.exists(root):
                os.mkdir(root)

            root += str(page)+'/'
            if not os.path.exists(root):
                os.mkdir(root)
        except:
            print('目录创建失败')
            exit(0)

        # 爬取
        # 爬取图片数
        count = 0
        try:
            for i in range(len(imgLinks)):
                r = requests.get(imgLinks[i])
                path = root+str(i+1)+'.jpg'
                if not os.path.exists(path):
                    with open(path, 'wb') as f:
                        f.write(r.content)
                    print(root+str(i+1)+'.jpg')
                    count = count+1
                else:
                    print(root+str(i+1)+'.jpg,已存在!')
        except:
            print('保存失败')
        finally:
            return count


if __name__ == '__main__':
    pua = netbian()
