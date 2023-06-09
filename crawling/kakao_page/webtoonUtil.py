import urllib.request
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from colorthief import ColorThief
# from HSL.hsl import rgb_to_hsl, hsl_to_rgb
from selenium import webdriver
from dotenv import load_dotenv
import colorsys
import time
import os
import requests

def image_main_color_hsl(url, tmp_file='tmp.jpg'):
    """
    이미지의 메인 컬러를 추출하는 함수
        Args:
            url (str): 이미지 주소
            tmp_file (str): 임시로 이미지를 저장할 이름
        Returns:
            hsl (str): 이미지의 메인 컬러(HSL)
    """
    req = urllib.request.Request(
        url=url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )

    img = urllib.request.urlopen(req).read()

    with open(tmp_file, mode="wb") as f:
        f.write(img)

    color_thief = ColorThief(tmp_file)
    dominant_color = color_thief.get_color(quality=1)

    r, g, b = dominant_color
    ONE_255 = 1.0 / 255.0
    h, l, s = map(lambda x: int(round(x*100, 0)), colorsys.rgb_to_hls(r * ONE_255, g * ONE_255, b * ONE_255))
    # h, s, l = map(lambda x: int(round(x*100, 0)),
    #               rgb_to_hsl(r * ONE_255, g * ONE_255, b * ONE_255))

    return f'{int(round(h*3.6,0))},{s},{l}'


def login(driver):
    load_dotenv()

    id = os.environ.get('ID')
    pw = os.environ.get('PW')

    login_url = "https://accounts.kakao.com/login/?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3Fis_popup%3Dfalse%26ka%3Dsdk%252F2.1.0%2520os%252Fjavascript%2520sdk_type%252Fjavascript%2520lang%252Fko-KR%2520device%252FWin32%2520origin%252Fhttps%25253A%25252F%25252Fpage.kakao.com%26auth_tran_id%3DMIACm4jYE0AY885ULiKw2u.40fC_jumaSraRJbVQ_AMQoQ~WU9ZaKnLuu6Ba%26response_type%3Dcode%26state%3Dhttps%25253A%25252F%25252Fpage.kakao.com%25252F%26redirect_uri%3Dhttps%253A%252F%252Fpage.kakao.com%252Frelay%252Flogin%26through_account%3Dtrue%26client_id%3D49bbb48c5fdb0199e5da1b89de359484&talk_login=hidden#login"
    driver.get(login_url)

    time.sleep(1)

    html = driver.page_source
    soup = bs(html, 'html.parser')

    driver.find_element(By.NAME, 'loginKey').send_keys(id)
    driver.find_element(By.NAME, 'password').send_keys(pw)
    driver.find_element(
        By.XPATH, '//*[@id="mainContent"]/div/div/form/div[4]/button[1]').click()
    
# post
def post_request(data, url="http://localhost:8080"):
    """
    JSON 데이터를 POST 요청
        ARGS:
            data: JSON
            url: "http://localhost:8080"(default)
    """
    headers = { 'content-type': 'application/json' }
    http_post_request = requests.post(url, headers=headers, data=data.encode('utf-8'))
    print("HTTP POST REQUEST!")
    print(http_post_request.text)
    print(http_post_request.status_code)

