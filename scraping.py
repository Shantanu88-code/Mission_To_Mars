#!/usr/bin/env python
# coding: utf-8

import datetime as dt
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():

# Initialize headless driver for deployment

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

# Run all scraping functions and store results in dictionary

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

# Stop the webdriver and return data

    browser.quit()
    return data

# Visit the mars nasa news site

# When we add the word "browser" to our function, we're telling Python that we'll be using the browser variable we defined outside
# the function. All of our scraping code utilizes an automated browser, and without this section, our function wouldn't work.

def mars_news(browser):

    url = 'https://redplanetscience.com'
    browser.visit(url)

# Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

# One is that we're searching for elements with a specific combination of tag (div) and attribute (list_text). 
# As an example, ul.item_list would be found in HTML as <ul class="item_list">.

# Setup HTML Parser

    html = browser.html

    news_soup = soup(html, 'html.parser')

# Add try and except for error handling

    try:

        slide_elem = news_soup.select_one('div.list_text')

        slide_elem.find('div', class_='content_title')

# # Use the parent element to find the first 'a' tag and save it as 'news_title'

        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_title

# Use the parent element to find the paragraph text

        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# ### Featured Images

# Visit URL

# Declare a function

def featured_image(browser):

    url = 'https://spaceimages-mars.com'
    browser.visit(url)

# Find and click full image button

    full_image_elem = browser.find_by_tag('button')[1]

    full_image_elem.click()

# Parse reulting html with soup

    html = browser.html

    img_soup = soup(html, 'html.parser')

# Find the relative image url
# Add try and except error handling

    try:

# Find the relative image url

        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None
    

# .get('src') pulls the link to the image.
# What we've done here is tell BeautifulSoup to look inside the <img /> tag for an image with a class of fancybox-image. 
# "This is where the image we want lives—use the link that's inside these tags."

# Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():

# Add try and except error handling

    try:

#  # Use 'read_html' to scrape the facts table into a dataframe

        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:

        return None

# Assign columns and set index of dataframe

    df.columns=['description', 'Mars', 'Earth']

    df.set_index('description', inplace=True)


# By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list

# By using the .set_index() function, we're turning the Description column into the DataFrame's index. 
# inplace=True means that the updated index will remain in place

# Convert DataFrame into HTML format

    return df.to_html(classes="table table-striped")

# Now that we've gathered everything on Robin's list, we can end the automated browsing session. 
# This is an important line to add to our web app also. Without it, the automated browser won't know to shut down


def mars_hemispheres(browser):

   

    hemisphere_image_urls = []

    for hemis in range(4):

        url = 'https://marshemispheres.com/'

        browser.visit(url)

        html = browser.html

        mrs_img = soup(html, 'html.parser')

    # Scraping
        title = mrs_img.find_all('h3')[hemis].text
    
        img_url = mrs_img.find_all('img', class_='thumb')[hemis]['src']
    
    # Store findings into a dictionary and append to list
        hemispheres = {}
    
        hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
    
        hemispheres['title'] = title
    
        hemisphere_image_urls.append(hemispheres)
    
    # Browse back to repeat
        browser.back()

    return hemisphere_image_urls


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())






