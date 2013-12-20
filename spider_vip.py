#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
from spider import BaseSpider, Request
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


if __name__ == '__main__':
    keyword = '%28Keyword_C%3D%28%E6%98%8E%E7%9F%BE%29%2BTitle_C%3D%28%E6%98%8E%E7%9F%BE%29%29'
    sp = VipPaperUrlSpider(company_id=1, keyword=keyword)
    sp.crawl([Request(url=sp.SUB_URL % (sp.keyword, 1, sp.keyword), parser=sp.seed_parser)])
