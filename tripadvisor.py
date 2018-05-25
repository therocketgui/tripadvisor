from env import _path_to_mozilla

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from bs4 import BeautifulSoup

from urllib.parse import quote_plus

import requests
import re
import json

import time
import random
import os
import sys

class TripAdvisor():


    def __init__(self):
      time.sleep(1)
      options = Options()
      options.add_argument("--headless")

      self.driver = webdriver.Firefox(firefox_options=options, executable_path=_path_to_mozilla)

      self.driver.implicitly_wait(10)

      self.clever_print("Starting Firefox Browser")

      self.prospects = []
      return

    def clever_print(self, message):
      # Print and Log
      print(self.curtime()+"~ "+str(message))
      # self.log+= self.curtime()+"~ "+str(message)
      return

    def launch(self):
      options = Options()
      options.add_argument("--headless")
      self.driver = webdriver.Firefox(firefox_options=options, executable_path=_path_to_mozilla)
      # self.driver = webdriver.Firefox(executable_path=_path_to_mozilla)
      self.driver.implicitly_wait(10)

      self.clever_print("Firefox Headless Browser Invoked")

      return

    def quit(self):
      self.clever_print('Quit Driver')
      self.driver.quit()
      time.sleep(1)
      return

    def curtime(self):
      return '[' + time.strftime("%d/%m/%Y")+ ' - ' + time.strftime("%H:%M:%S") + '] '

    def get(self, url):
      self.clever_print('Getting: '+str(url))
      self.driver.get(url)
      time.sleep(2)
      return

    def extra_short_sleep(self):
      r = random.uniform(0.22, 0.33)
      time.sleep(r) # pause for 0.3 seconds
      return
    def very_short_sleep(self):
      r = random.uniform(0.4, 0.7)
      time.sleep(r) # pause for 0.3 seconds
      return
    def short_sleep(self):
      r = random.uniform(0.7, 1.0)
      time.sleep(r) # pause for 0.3 seconds
      return
    def medium_sleep(self):
      r = random.uniform(4, 5)
      time.sleep(r) # pause for 0.3 seconds
      return
    def large_sleep(self):
      r = random.uniform(10, 16)
      time.sleep(r) # pause for 0.3 seconds
      return

    def type(self, driver, text):
      for character in text:
          driver.send_keys(character)
          r = random.uniform(0.06, 0.15)
          time.sleep(r) # pause for 0.3 seconds
      return

    def get_infos(self, source):
      prospects = []
      soup = BeautifulSoup(source, "html.parser")
      # soup = BeautifulSoup(open("test.html"), "html.parser")

      for listing in soup.select('div.listing.rebrand'):
        try:
          company = listing.find('a', {'class':'property_title'}).text.strip()
          link = 'https://www.tripadvisor.co.uk'+listing.find('a', {'class':'property_title'})['href']
          prospect = {'company':company, 'link':link}
          prospects.append(prospect)
        except:
          pass

      return prospects

    def get_infos_pages(self, link):
      self.get(link)
      source = self.driver.page_source
      prospects = self.get_infos(source)

      for i in range(0, 22):
        self.driver.find_element_by_class_name('next').click()
        time.sleep(3)
        source = self.driver.page_source
        prospects = prospects + self.get_infos(source)

      return prospects

    def clean_link(self, link):
      # link = link.replace('http://', '').replace('https://', '').replace('http://www.', '').replace('https://www.', '')
      # return link.split('/')[0]
      return link

    def get_data(self):
      with open('data.json') as data_file:
          data = json.load(data_file)
      return data

    def get_company_list(self):
      with open('data.json') as data_file:
          data = json.load(data_file)

      companies = []

      for d in data:
        companies.append(d['company'])

      return companies

    def store(self, jobs):

        # retrieive the data stored and the local_id list
        data = self.get_data()

        # Insert
        for job in jobs:
            data.append(job)

        # Write and store the data in the json
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)

        return

    def get_info(self, prospect):

      self.get(prospect['link'])
      source = self.driver.page_source

      soup = BeautifulSoup(source, "html.parser")
      phone = soup.select_one('div.blEntry.phone').text.strip()
      address = soup.select_one('div.blEntry.address').text.strip()

      website_link = self.driver.find_element_by_xpath("//span[contains(text(),'Website')]")
      website_link.click()
      window_before = self.driver.window_handles[0]
      window_after = self.driver.window_handles[1]
      self.driver.switch_to_window(window_after)

      time.sleep(2)
      url = self.clean_link(self.driver.current_url.split('?utm_source')[0])
      if url == 'about:blank' or url == 'https:' or url == 'http:':
        # try again
        time.sleep(5)
        url = self.clean_link(self.driver.current_url.split('?utm_source')[0])

      info = {'phone':phone, 'address':address, 'url': url}
      prospect['info'] = info


      # self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
      self.driver.close()
      self.driver.switch_to_window(window_before)
      #
      return prospect

    def run_get_info_all(self, prospects):
      _prospects = []
      companies = self.get_company_list()
      # print('~ Banlist: '+str(companies))
      self.launch()

      for prospect in prospects:
        if prospect['company'] not in companies:
          # self.launch()

          try:
            _prospect = self.get_info(prospect)
            if 'url' in prospect['info']:
              print(_prospect)
              _prospects.append(_prospect)
              self.prospects.append(_prospect)
          except Exception as e:
            print(e)

          # self.quit()
      self.quit()
      return _prospects

    def go(self, link):
      self.launch()
      # get all prospects
      # self.get('https://www.tripadvisor.com/Restaurants-g186338-c6-London_England.html')
      # source = self.driver.page_source
      # prospects = self.get_infos(source)
      # self.get('https://www.tripadvisor.co.uk/Restaurant_Review-g186338-d12116313-Reviews-Shahi_Pakwaan-London_England.html')
      # source = self.driver.page_source
      # i = self.get_info(source)
      # print(i)
      # print(self.get_info(open('testindiv.html')))

      prospects = self.get_infos_pages(link)

      try:
        _prospects = self.run_get_info_all(prospects)
        print('\n')
        print(json.dumps(_prospects, indent=4))
        self.store(_prospects)
      except Exception as e:
        print(e)
        print('Process Stopped.')
      finally:
        print('Storing Prospects...')
        self.store(self.prospects)


      return

def main():
  try:
    tripadv = TripAdvisor()
    tripadv.go(sys.argv[1])
  except Exception as e:
    print(e)
  finally:
    tripadv.quit()
  return

def count():
  count=0
  with open('data.json') as data_file:
      data = json.load(data_file)

  for prospect in data:
    if 'printed' not in prospect:
      # print(prospect['company'])
      count += 1

  return count

if __name__ == "__main__":
  print(count())

  if len(sys.argv) > 1:
    main()

