# -*- coding: utf-8 -*-
import Crawling as caw

URL = "http://cafe.naver.com/ArticleList.nhn?search.clubid=11133417&search.menuid=560&search.boardtype=L&search.questionTab=A&search.totalCount=115&search.page=1"

crawler = caw.NaverCafeCrawing(URL)
pageNo, boardNo = crawler.getData()
content = crawler.crawling()
crawler.writeCsv(content)

