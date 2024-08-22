import re
import sys
import logging
import requests
from selenium import webdriver
from flask import Flask
from flask import Response, stream_with_context
from selenium.webdriver.common.by import By

current_stream = None
app = Flask(__name__)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def bypass_shortener(endpoint):
  logger.info('[!] Bypassing shortener with url ' + endpoint)

  driver.get(endpoint)
  driver.execute_script("document.querySelector('#landing').submit()")
  pattern = r"https://tech\.unblockedgames\.world/\?go=pepe-[\w\-]+"
  matches = re.findall(pattern, driver.page_source)

  if len(matches) == 0:
    raise Exception("Error while finding valid 'driveleech' url")
  
  logger.info("[+] Succesfully bypassed, found url: " + matches[0])

  return matches[0]

def fetch_stream_infos(driveleech_url):
  logger.info('[!] Looking for stream key')

  driver.get(driveleech_url)
  a_href = driver.find_element(By.XPATH, '//*[@id="cf_captcha"]/div[2]/div[2]/a[1]')

  key_url = a_href.get_attribute('href')
  key_value = key_url.split("url=")[1]

  logger.info('[+] Found key value ' + key_value)

  r = requests.post(f"https://video-leech.xyz/api", headers={
    'x-token': "https://video-leech.xyz/",
  }, data={
    "keys": key_value
  })

  if r.status_code != 200:
    raise Exception(f"Failed with status code {r.status_code}")

  logger.info('[+] Found stream url: ' + r.json()['url'])

  return r.json()

@app.get("/stream")
def stream():
  logger.info('[!] Started streaming of url ' + current_stream)
  res = requests.get(current_stream, stream=True)
  return Response(stream_with_context(res.iter_content(4096)), content_type=res.headers['content-type'])

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("[x] You should provide a valid url")
    exit(-1)
  
  driveleech_url = bypass_shortener(sys.argv[1])
  stream_infos = fetch_stream_infos(driveleech_url)
  current_stream = stream_infos['url']

  app.run('0.0.0.0', port=3000, debug=True, use_reloader=False)
  exit(0)