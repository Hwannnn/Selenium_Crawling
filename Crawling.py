from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import requests
import time
import copy

class NaverCafeCrawing :
    
    def __init__(self, URL):
        self.URL = URL
        self.page = []
        self.board = []
        self.board_temp = []
        self.content = {}

    def error(self, driver, boardNo) :
        self.content[boardNo] = "can't search"
        driver.back()
        time.sleep(3)
        
    def getData(self) :
        url = self.URL
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "lxml")
        
        pageNumber = soup.select("table[class='Nnavi'] > tr > td > a")
        for n in pageNumber :
            self.page.append(n.text)
        
        res.close()
        
        for pageNo in self.page:
            url = "http://cafe.naver.com/ArticleList.nhn?search.clubid=11133417&search.menuid=560&search.boardtype=L&search.questionTab=A&search.totalCount=115&search.page=" + pageNo
            res = requests.get(url)
            soup = BeautifulSoup(res.text, "lxml")
            
            boardNumber = soup.select("form[name='ArticleList'] .list-count")
            for n in boardNumber :
                self.board.append(n.text)
            
            res.close()
        
        print(self.page)
        print(self.board)
        return self.page, self.board
        
        
    def crawling(self) :
        try :
            #selenium webdriver chrome을 월하는 위치에 설치한후 아래에 주소입력
            driver = webdriver.Chrome('C:/Users/DS/chromedriver_win32/chromedriver.exe')
            driver.get("http://toors.cafe24.com/cafe-link/")        
            window_before = driver.window_handles[0]

            self.board_temp = copy.copy(self.board)
            print(self.board)
            for boardNo in self.board_temp :
                if boardNo == "" :
                    continue
                url = "http://cafe.naver.com/assarabia/" + boardNo
                elem = driver.find_element_by_id("searchbar")
                elem.clear()
                elem.send_keys(url)
                elem = driver.find_element_by_id("submit")
                elem.click()
                
                if(driver.current_url == "http://toors.cafe24.com/cafe-link/error.html") : 
                    self.error(driver, boardNo)
                    continue
                time.sleep(2)
                
                if(len(driver.find_element_by_css_selector("._cafeBase > .section_head").text) == 3) :
                    self.error(driver, boardNo)
                    continue
                
                elem = driver.find_element_by_id("nx_query").get_attribute('value')                
                elem2 = driver.find_elements_by_class_name("sh_cafe_title");
                
                for temp in elem2 :
                    if(elem == temp.text) :
                        elem2 = temp.text
                        break

                if(elem != elem2) :
                    self.error(driver, boardNo)
                    continue
                
                elem = driver.find_element_by_link_text(elem)
                elem.click()
                time.sleep(2)
                
                window_after = driver.window_handles[1]
                driver.switch_to_window(window_after)
                elem = driver.find_element_by_id("cafe_main")
                driver.switch_to_frame(elem)
                time.sleep(2)
                
                con = driver.find_element_by_css_selector("#tbody").text
                driver.close()
                
                driver.switch_to_window(window_before)
                time.sleep(2)
                
                driver.back()
                time.sleep(2)
                
                print(boardNo)
                self.content[boardNo] = con
                del self.board[0]

        except :
            print("error!!!!!!!!!")
            print(self.board)
            driver.quit()
            time.sleep(2)
            self.crawling()
        
        finally :
            return self.content


    def writeCsv(self, con) :
        writeData = pd.DataFrame(list(con.items()), columns=['boardNo', 'boardContent'])
        writeData.to_csv("crawling_result.csv")
