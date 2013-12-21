#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
from spider import BaseSpider, Request
from pyquery import PyQuery as pq
import helpers


class VipPaperUrlSpider(BaseSpider):
    """docstring for VipSpider"""
    def __init__(self, company_id, keyword):
        super(VipPaperUrlSpider, self).__init__()
        self.PAPER_PATH_RE = re.compile('href="(/qk/.+?.html)"')
        self.PAPER_ID_RE = re.compile('/(\d+)\.html')
        self.NUM_RE = re.compile('search_jg2">(\d+)')
        self.SUB_SQL = 'insert into PaperUrl(Id, Path) values(%d, %s)'
        self.SUB_URL = ('http://lib.cqvip.com/zk/search.aspx?E=%s&M=&P=%d'
                        '&CP=&CC=&LC=&H=%s&Entry=M&S=1&SJ=&ZJ=&GC=&Type=')
        self.keyword = keyword
        self.company_id = company_id

    def page_parser(self, url, page_content):
        """docstring for page_parser"""
        con = helpers.mssqlconn()
        paths = self.PAPER_PATH_RE.findall(page_content)
        for i in paths:
            try:
                #con.execute_non_query(self.SUB_SQL, (int(self.PAPER_ID_RE.search(i).group(1)), i))
                print self.PAPER_ID_RE.search(i).group(1), i
            except Exception:
                pass
        con.close()

    def seed_parser(self, url, page_content):
        """docstring for seed_parser"""
        page_count = int(self.NUM_RE.search(page_content).group(1)) / 20 + 2
        print page_count
        for i in xrange(1, page_count):
            yield Request(url=self.SUB_URL % (self.keyword, i, self.keyword),
                          parser=self.page_parser)


class VipPaperSpider(BaseSpider):
    """fetch paper content"""
    def __init__(self):
        super(VipPaperSpider, self).__init__()
        self.PAPER_ID_RE = re.compile('/(\d+)\.html')
        self.INSERT_SQL = ('insert into PaperContent(id, Title, Author,'
                           'Abstract, Keywords, Class, DownloadUrl)'
                           'values(%d, %s, %s, %s, %s, %s, %s)')

    def content_parser(self, url, page_content):
        """docstring for content_parser"""
        con = helpers.mssqlconn()
        p = pq(page_content)
        paper_id = int(self.PAPER_ID_RE.search(url).group(1))
        title = p('h1').text() or '-----'
        author = p('.author a').text() or '-----'
        abstract = p('.abstrack').text() or '-----'
        keywords = p('.keywords a').text() or '-----'
        paper_class = p('#wxClass').attr.value or '-----'
        download_url = '-----'
        try:
            con.execute_non_query(self.INSERT_SQL,
                                  (paper_id, title, author, abstract,
                                   keywords, paper_class, download_url))
            print paper_id
        except Exception:
            print 'not', paper_id


if __name__ == '__main__':
    #keyword = '%28Keyword_C%3D%28%E6%98%8E%E7%9F%BE%29%2BTitle_C%3D%28%E6%98%8E%E7%9F%BE%29%29'
    #sp = VipPaperUrlSpider(company_id=1, keyword=keyword)
    #sp.crawl([Request(url=sp.SUB_URL % (sp.keyword, 1, sp.keyword), parser=sp.seed_parser)])
    vps = VipPaperSpider()
    con = helpers.pymssqlconn()
    cur = con.cursor()
    cur.execute(('select Path from PaperUrl where not exists'
                 '(select 1  from PaperContent where id=PaperUrl.id)'))
    reqs = []
    for row in cur:
        url = 'http://lib.cqvip.com%s' % row[0]
        reqs.append(Request(url=url, parser=vps.content_parser))
    vps.crawl(reqs)
