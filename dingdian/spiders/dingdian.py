import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from dingdian.items import DingdianItem
from dingdian.items import DcontentItem
from dingdian.mysqlpipelines.sql import Sql


class Myspider(scrapy.Spider):
    name = 'dingdian'
    allowed_domains = ['23wx.cc']
    bash_url = 'http://www.23wx.cc/class/'
    bashurl = '.html'
    base_domain = 'http://www.23wx.cc'

    def start_requests(self):
        for i in range(1, 5):
            url = self.bash_url + str(i) + '_1' + self.bashurl
            yield Request(url, self.parse)
        for i in range(6, 9):
            url = self.bash_url + str(i) + '_1' + self.bashurl
            yield Request(url, self.parse)

    def parse(self, response):
        max_num = BeautifulSoup(response.text, 'lxml').find(
            'div', class_='pagelink').find_all('a')[-1].get_text()
        bashurl = str(response.url)[:-7]
        categorys = BeautifulSoup(response.text, 'lxml').find(
            'div', class_='nav').find_all('a')
        cat = ''
        for category in categorys:
            if category['href'].find(str(bashurl)[-8:]) != -1:
                cat = category.get_text()
                break

        for num in range(1, int(max_num) + 1):
            url = bashurl + '_' + str(num) + self.bashurl
            yield Request(url, callback=self.get_name, meta={'cat': cat})

    def get_name(self, response):
        items = BeautifulSoup(response.text, 'lxml').find_all(
            'div', class_='image')
        for item in items:
            novelname = item.find('img')['alt']
            novelurl = item.find('a')['href']
            if str(novelurl).find(self.base_domain) == -1:
                novelurl = self.base_domain + novelurl
            yield Request(novelurl, callback=self.get_chapterurl, meta={'name': novelname, 'url': novelurl, 'cat': response.meta['cat']})

    def get_chapterurl(self, response):
        item = DingdianItem()
        item['name'] = str(response.meta['name']).replace('\xa0', '')
        item['novelurl'] = response.meta['url']
        item['category'] = response.meta['cat']
        author = BeautifulSoup(response.text, 'lxml').find(
            id='info').find('p')
        author = str(author.get_text()).split('：')[1]
        item['author'] = author
        name_id = str(response.url)[-6:-1].replace('/', '')
        item['name_id'] = name_id
        yield item
        dds = BeautifulSoup(response.text, 'lxml').find_all('dd')
        num = 0
        for novel in dds:
            num = num + 1
            url = response.url + novel.find('a')['href']
            chapter_title = novel.find('a').get_text()
            rets = Sql.select_chapter(url)
            if rets[0] == 1:
                print('the chapter is exsits!')
                pass
            else:
                yield Request(url, callback=self.get_chapter, meta={'num': num, 'name_id': name_id, 'chaptername': chapter_title, 'chapterurl': url})

    def get_chapter(self, response):
        item = DcontentItem()
        item['num'] = response.meta['num']
        item['id_name'] = response.meta['name_id']
        item['chaptername'] = str(
            response.meta['chaptername']).replace('\xa0', '')
        item['chapterurl'] = response.meta['chapterurl']
        content = BeautifulSoup(response.text, 'lxml').find(
            id='content').get_text()
        item['chaptercontent'] = str(content).replace('\xa0', '')
        return item
