from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
from time import sleep
from random import randint
from constants import REDDIT_BASE_URL, SCROLL_DISTANCE, SLEEP_MAX_SECONDS, SLEEP_MIN_SECONDS
class Scrapper(object):
    def __init__(self, browser):
        self.browser = browser
        self.driver = None
        
    def start(self):
        if self.browser.lower() == 'chrome':
            self.driver = webdriver.Chrome()
        elif self.browser.lower() == 'firefox':
            self.driver = webdriver.Firefox()
        elif self.browser.lower() == "edge":
            self.driver = webdriver.Edge()
        else:
            raise ValueError("Unsupported browser. Use 'chrome' or 'firefox'")
        sleep(1)
        
    def stop(self):
        if self.driver:
            self.driver.quit()
    
    def sleep(self):
        sleep(randint(SLEEP_MIN_SECONDS, SLEEP_MAX_SECONDS))

class RedditScraper(Scrapper):
    def __init__(self, browser):
        super().__init__(browser)
        self.posts = []
        self.comments = []
        self.activeIn = []
        self.username = None
        
    def start(self, username):
        super().start()
        self.username = username
        self.scrapePosts()
        self.scrapeComments()
        

    def scrapePosts(self):
        if not self.driver or not self.username:
            raise ValueError("Driver not initialized or username not set")
            
        url = f"https://www.reddit.com/user/{self.username}/submitted"
        self.driver.get(url)
        self.sleep()
        self.driver.execute_script(f"window.scrollBy(0,{SCROLL_DISTANCE})")
        self.sleep()
        self.driver.execute_script(f"window.scrollBy(0,{SCROLL_DISTANCE})")
        self.sleep()
        
        html = self.driver.page_source.encode('utf-8').strip()
        soup = bs(html, 'html.parser')
        posts = soup.find_all("a", attrs={"slot":"title"})
        
        data = []
        for post in posts:
            postLink = post.get("href")
            title = post.get_text().strip()
            
            textLink = soup.find("a", attrs={'href':postLink, "slot":"text-body"})
            desc = ""
            if textLink:
                texts = textLink.find_all("p")
                for text in texts:
                    descChunk = text.get_text().strip()
                    if descChunk:
                        desc += descChunk
                        
                if not desc:
                    desc = textLink.get_text()
                    
            data.append({
                "title": title,
                "description": desc,
                "link": postLink
            })
            
        self.posts = data
        
    def scrapeComments(self):
        if not self.driver or not self.username:
            raise ValueError("Driver not initialized or username not set")
            
        url = f"{REDDIT_BASE_URL}/user/{self.username}/comments"
        self.driver.get(url)
        self.sleep()
        self.driver.execute_script(f"window.scrollBy(0,{SCROLL_DISTANCE})")
        self.sleep()
        self.driver.execute_script(f"window.scrollBy(0,{SCROLL_DISTANCE})")
        self.sleep()
        
        html = self.driver.page_source.encode('utf-8').strip()
        soup = bs(html, 'html.parser')
        comments = soup.find_all("shreddit-profile-comment")
        
        data = []
        for comment in comments:
            try:
                page = comment.find("a", 
                                  attrs={"rpl":True}, 
                                  class_="hover:underline").get('href')
                
                subReddit = comment.find("a", 
                                  attrs={"rpl":True, "target":"_blank"}, 
                                  class_="hover:underline").get_text().strip()
                
                cmnt = comment.find("div", id="-post-rtjson-content").get_text().strip()
                
                data.append({
                    "page": page,
                    "subReddit": subReddit,
                    "comment": cmnt
                })
            except AttributeError:
                continue
                
        self.comments = data
        
    def getPosts(self):
        return self.posts
        
    def getComments(self):
        return self.comments
        
    def data(self):
        return self.posts, self.comments
