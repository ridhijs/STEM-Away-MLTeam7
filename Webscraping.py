#!/usr/bin/env python
# coding: utf-8

# In[425]:


# imports
from selenium import webdriver
import pandas as pd
import numpy as np
import time
from bs4 import BeautifulSoup


# In[426]:


# webdriver
browser = webdriver.Chrome()
browser.set_page_load_timeout(10)
URL = "https://sellercentral.amazon.com/forums/c/fulfillment-by-amazon"
browser.get(URL)


# In[427]:


# variables
scroll_pause_time = 3
cats = []
subcats = []
titles = []
post_texts = []
urls = []
replies = []
start = 0
reloads = 0


# In[430]:


# webscraping
while reloads < 30:
    
    # find all posts on page
    elem = browser.find_element_by_tag_name("span")
    post_elem = browser.find_elements_by_class_name("link-top-line")
    
    for i in range(start, len(post_elem)):
        
        # find link to each post
        time.sleep(2.5) # increase the sleep time if there's an error at runtime
        elem = browser.find_element_by_tag_name("span")
        post_elem = browser.find_elements_by_class_name("link-top-line")
        link = browser.find_element_by_link_text(post_elem[i].text)
        link.click()

        # switch URL of browser
        time.sleep(2) # increase the sleep time if there's an error at runtime
        window_after = browser.window_handles[0]
        browser.switch_to.window(window_after)

        soup = BeautifulSoup(browser.page_source, 'html.parser')
        post = soup.find("section")
        # title
        title = post.find('a', attrs={'class': 'fancy-title'})
        titles.append(title.text.replace('\n', '').strip())
        # category
        categories = post.find_all('span', attrs={'class': 'category-name'})
        cat = categories[0]
        cats.append(cat.text.replace('\n', '').strip())
        # subcategory
        if len(categories) > 1 :
            subcat = categories[1]
        else :
            subcat = categories[0]
        subcats.append(subcat.text.replace('\n', '').strip())
        # post text
        post_text = post.find('div', attrs={'class': 'cooked'})
        post_texts.append(post_text.text.replace('\n', '').strip())
        # urls
        url = browser.current_url
        urls.append(url)
        # replies
        comments = post.find_all('div', attrs={'class': 'regular contents'})
        post_comments = []
        for i in range (1, len(comments)) :
            post_comments.append(comments[i].find('div', attrs={'class': "cooked"}).text.replace('\n', '').strip())
        replies.append(post_comments)

        browser.back()
    
    # scroll down once
    start = len(post_elem)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    reloads = reloads + 1
    time.sleep(scroll_pause_time)

browser.close()


# In[ ]:


# dataframe 1
all = list(zip(titles, cats, subcats, post_texts, urls))
DF1 = pd.DataFrame(all, columns = ["Title", "Category", "Sub-category", "Post Text", "URL"])
DF1.head(800)


# In[ ]:


# dataframe 2
responses = []
for i in range (0, len(urls)) :
    for j in range (0, len(replies[i])) :
        responses.append((urls[i], replies[i][j]))
DF2 = pd.DataFrame(responses, columns = ["URL", "Response Text"])
DF2.head(800)


# In[ ]:


# csv files
DF1.to_csv(DF1.csv', index = False)
DF2.to_csv(DF2.csv', index = False)


# In[ ]:




