from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
from colorthief import ColorThief
import urllib.request
import os
from HSL.hsl import rgb_to_hsl, hsl_to_rgb
import webtoon

def image_main_color_hsl(url,tmp_file='tmp.jpg'):
    """
    이미지의 메인 컬러를 추출하는 함수
        Args:
            url (str): 이미지 주소
            tmp_file (str): 임시로 이미지를 저장할 이름
        Returns:
            hsl (str): 이미지의 메인 컬러(HSL)
    """

    img=urllib.request.urlopen(url).read()
    with open(tmp_file, mode="wb") as f:
        f.write(img)
    color_thief = ColorThief(tmp_file)
    dominant_color = color_thief.get_color(quality=1)
    # os.remove("test.png")
    r, g, b = dominant_color
    print(r,g,b)
    ONE_255 = 1.0 / 255.0

    h, s, l = map(lambda x: int(round(x*100, 0)), rgb_to_hsl(r * ONE_255, g * ONE_255, b * ONE_255))
    
    return f'{int(round(h*3.6,0))},{s},{l}'



def scroll_bottom(driver):
    """
    맨 아래까지 스크롤하하는 함수
        Args:
            driver (selenium): webdriver
    """
    SCROLL_PAUSE_SEC = 1

    # 스크롤 높이 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 1초 대기
        sleep(SCROLL_PAUSE_SEC)

        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


# 천천히 스크롤하며 모든 이미지 불러오기
def scroll_slow(driver):
    SCROLL_PAUSE_SEC = 1

    # 스크롤 높이 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # 끝까지 스크롤 다운
        for h in range(0,last_height,last_height//10):
            driver.execute_script(f'window.scrollTo(0, {h});')
            sleep(0.5)

        # 1초 대기
        sleep(SCROLL_PAUSE_SEC)

        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# 로그인하기
def login(driver):
    id = "oth5447@naver.com"
    pw= "261834oO@@"
    # 로그인 페이지로 이동
    driver.get('https://webtoon.kakao.com/more')
    driver.find_element(By.CSS_SELECTOR, '#root > main > div > div > div.absolute.top-0.left-0.w-full.z-navigationBar > div.px-18.m-auto.items-center.flex.h-header-height.fixed.top-0.left-0.right-0.z-navigationBar > div.ml-auto.flex.flex-none > a').click()
    driver.find_element(By.CSS_SELECTOR, 'body > div:nth-child(20) > div > div > div > div.overflow-x-hidden.overflow-y-auto.\!overflow-hidden.flex.flex-col > div.text-center.pb-\[117px\].overflow-y-auto > div > div > button').click()
    
    # 아이디, 비밀번호 입력
    driver.find_element(By.CSS_SELECTOR, '#loginKey--1').send_keys(id)
    driver.find_element(By.CSS_SELECTOR, '#password--2').send_keys(pw)
    
    # 로그인버튼 클릭
    driver.find_element(By.CSS_SELECTOR, '#mainContent > div > div > form > div.confirm_btn > button.btn_g.highlight.submit').click()
    sleep(1)

    # 중복로그인 알람 뜨는 경우 확인 눌러주기
    try:
        yes_click = driver.find_element(By.CSS_SELECTOR, 'body > div:nth-child(24) > div > div > div > div.absolute.w-full.px-18.bottom-0.pb-30.flex.left-0.z-1.bg-grey-01.light\:bg-white.Alert_buttonsWrap__2fPaV.pt-10 > button.relative.px-10.py-0.btn-white.light\:btn-black.button-active')
        yes_click.click()
    except Exception:
        pass
    sleep(1)

def crawling(day_string):
    f = open("./webtoon-json.txt", 'a', encoding="UTF-8") # json을 저장할 파일 지정

    count = 0 # 성공한 웹툰 개수

    driver = webdriver.Chrome("./chromedriver") # 크롬 브라우저를 사용
    driver.implicitly_wait(10)

    login(driver) # 카카오 웹툰 로그인

    driver.get(f'https://webtoon.kakao.com/original-webtoon?tab={day_string}')
    kakao_base_url = 'https://webtoon.kakao.com'

    scroll_slow(driver) # 맨 아래로 스크롤 하기

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    urls = soup.select('#root > main > div > div > div.px-11.mx-auto.my-0.w-full.lg\:w-default-max-width.md\:w-\[490px\] > div.flex.flex-col.gap-4 > div.flex.flex-wrap.gap-4.content-start > div > div > div > a')
    # 인물만 뽑기
    images = soup.select('#root > main > div > div.page.bg-background.activePage > div.px-11.mx-auto.my-0.w-full.lg\:w-default-max-width.md\:w-\[490px\] > div.flex.flex-col.gap-4 > div.flex.flex-wrap.gap-4.content-start > div > div > div > a > picture:nth-child(2) > img')
    # 배경, 인물 같이 뽑기
    # images = soup.select('#root > main > div > div.page.bg-background.activePage > div.px-11.mx-auto.my-0.w-full.lg\:w-default-max-width.md\:w-\[490px\] > div.flex.flex-col.gap-4 > div.flex.flex-wrap.gap-4.content-start > div > div > div > a > picture > img')
    # sleep(3)

    # 웹툰 주소, 썸네일 주소
    url_arr = list(map(lambda x: x["href"], urls))
    images_arr = list(map(lambda x: x["src"], images))
    urls_and_images = tuple(zip(url_arr, images_arr))
    print("전체 웹툰 개수:", len(urls_and_images))

    for url, image in urls_and_images:
        if count and count % 10 == 0:
            print("count-10! WAIT 10sec!!")
            sleep(10)

        webtoon_info = webtoon.Webtoon() # 웬툰 클래스 생성

        webtoon_url = kakao_base_url + url # 웹툰 주소 생성
        
        driver.get(webtoon_url) # 이동
        
        idx = url.find("/", -5)
        webtoon_info.webtoon_id = url[idx+1:]
        
        sleep(0.5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        try:
            driver.find_element(By.CSS_SELECTOR, '#root > main > div > div.page.bg-background-02.activePage > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.w-full.left-0.top-0.relative > div.content-main-wrapper.opacity-0.invisible.relative.current-content-main.opacity-100.\!visible.z-1 > div.pb-20.pt-96.relative.z-1 > div.relative.mx-auto.my-0.w-full.lg\:w-default-max-width > div.mx-20.flex.justify-between.relative.z-1.pointer-events-auto.pt-12 > div').click()
        except Exception as err:
            print("False")
            print(webtoon_url)

            print(err)
            miss.append(url)
            continue

        sleep(1)

        # try:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # 연재 정보
        '''
        연재 정보가의 태그 종류가 두가지임       
        하나를 먼저 확인하고, 없으면 다음 태그 종류를 확인 
        '''
        try:
            webtoon_info.status = soup.select_one('#root > main > div > div > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.relative.z-1.h-full > div > div > div.swiper-slide.swiper-no-swiping.swiper-slide-active > div > div.relative.h-full > div > div > div.swiper-slide.swiper-slide-active > div > div > div > div > div.flex.flex-wrap > div > p.whitespace-pre-wrap.break-all.break-words.support-break-word.font-badge.\!whitespace-nowrap.rounded-5.s10-bold-white.bg-dark-red.px-4').string.strip()
        except Exception:
            webtoon_info.status = soup.select_one('#root > main > div > div.page.bg-background-02.activePage > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.relative.z-1.h-full > div > div > div.swiper-slide.swiper-no-swiping.swiper-slide-active > div > div.relative.h-full > div > div > div.swiper-slide.swiper-slide-active > div > div > div > div > div.flex.flex-wrap > div > p.whitespace-pre-wrap.break-all.break-words.support-break-word.font-badge.\!whitespace-nowrap.rounded-5.s10-bold-white.bg-dark-grey-09.px-4').string.strip()

        # 연재 요일 정보 저장
        days = soup.select('#root > main > div > div.page.bg-background-02.activePage > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.relative.z-1.h-full > div > div > div.swiper-slide.swiper-no-swiping.swiper-slide-active > div > div.relative.h-full > div > div > div.swiper-slide.swiper-slide-active > div > div > div > div > div.flex.flex-wrap > div > p.whitespace-pre-wrap.break-all.break-words.support-break-word.font-badge.\!whitespace-nowrap.rounded-5.s10-bold-black.bg-white.px-4')
        webtoon_info.day_arr = [day.string.strip() for day in days]
        
        # 연재 등급 정보 저장
        # 성인 여부 태그
        grade = soup.select_one('#root > main > div > div.page.bg-background-02.activePage > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.relative.z-1.h-full > div > div > div.swiper-slide.swiper-no-swiping.swiper-slide-active > div > div.relative.h-full > div > div > div.swiper-slide.swiper-slide-active > div > div > div > div > div.flex.flex-wrap > div > img')
        if not grade:
            # 등급 태그
            grade = soup.select_one('#root > main > div > div.page.bg-background-02.activePage > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.relative.z-1.h-full > div > div > div.swiper-slide.swiper-no-swiping.swiper-slide-active > div > div.relative.h-full > div > div > div.swiper-slide.swiper-slide-active > div > div > div > div > div.flex.flex-wrap > div > p.whitespace-pre-wrap.break-all.break-words.support-break-word.font-badge.\!whitespace-nowrap.rounded-5.s10-bold-white.bg-dark-blue.px-4')
            # 전체 이용가는 표시가 안되어있음
            if not grade:
                webtoon_info.grade = "전체이용가"
        webtoon_info.grade

        # 웹툰 이름 저장
        webtoon_info.name = soup.select_one('#root > main > div > div.page.bg-background-02.activePage > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.relative.z-1.h-full > div > div > div.swiper-slide.swiper-no-swiping.swiper-slide-active > div > div.relative.h-full > div > div > div.swiper-slide.swiper-slide-active > div > div > div > div > p').string.strip()

        # 웹툰 작가 리스트 저장
        webtoon_info.authors_arr = [
            soup.select_one('#root > main > div > div.page.bg-background-02.activePage > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.relative.z-1.h-full > div > div > div.swiper-slide.swiper-no-swiping.swiper-slide-active > div > div.relative.h-full > div > div > div.swiper-slide.swiper-slide-active > div > div > div > div > dl > div:nth-child(1) > dd').string.strip(),
            soup.select_one('#root > main > div > div.page.bg-background-02.activePage > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.relative.z-1.h-full > div > div > div.swiper-slide.swiper-no-swiping.swiper-slide-active > div > div.relative.h-full > div > div > div.swiper-slide.swiper-slide-active > div > div > div > div > dl > div:nth-child(2) > dd').string.strip()
            ]
        
        # 웹툰 줄거리 저장
        webtoon_info.plot = soup.select_one('#root > main > div > div.page.bg-background-02.activePage > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.relative.z-1.h-full > div > div > div.swiper-slide.swiper-no-swiping.swiper-slide-active > div > div.relative.h-full > div > div > div.swiper-slide.swiper-slide-active > div > div > div > div > div:nth-child(4) > div:nth-child(2) > p').string.strip()

        # 웹툰 장르 리스트 저장
        genres = soup.select('#root > main > div > div.page.bg-background-02.activePage > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.relative.z-1.h-full > div > div > div.swiper-slide.swiper-no-swiping.swiper-slide-active > div > div.relative.h-full > div > div > div.swiper-slide.swiper-slide-active > div > div > div > div > div:nth-child(5) > div.flex.flex-wrap.-mt-12 > a > p')
        webtoon_info.genre_arr = [genre.string.strip() for genre in genres]
        
        # 웹툰 썸네일 저장
        webtoon_info.image = image

        # 웹툰 주소 저장
        webtoon_info.webtoon_url = url

        # 회차 정보 클릭
        driver.find_element(By.CSS_SELECTOR, '#root > main > div > div.page.bg-background-02.activePage > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.relative.z-1.h-full > div > div > div.swiper-slide.swiper-no-swiping.swiper-slide-active > div > div.menu-wrapper.-mt-1.left-0.absolute.top-0.w-full.z-3.flex-center > div.w-full.mx-52 > div > div.w-full.h-full.relative > ul > li.cursor-pointer.relative.whitespace-nowrap.flex-center.flex-1.flex-shrink-0.HorizontalTab_firstItem__1ar2M').click()
        sleep(0.5)

        # 전체 회차 저장
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        total_ep = soup.select_one('#root > main > div > div.page.bg-background-02.activePage > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.relative.z-1.h-full > div > div > div.swiper-slide.swiper-no-swiping.swiper-slide-active > div > div.relative.h-full > div > div > div.swiper-slide.swiper-slide-active > div > div > div > div > ul > li:nth-child(1) > a > div.px-8.pt-9.pb-8.h-46 > p')
        webtoon_info.total_ep = total_ep.string.strip()[:-1]
        driver.find_element(By.CSS_SELECTOR, '#root > main > div > div > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.relative.z-1.h-full > div > div > div.swiper-slide.swiper-no-swiping.swiper-slide-active > div > div.bottom-73.z-5.relative.flex-center.pointer-events-none > button').click()
        sleep(0.5)

        # 시작날짜 저장
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        start_date = soup.select_one('#root > main > div > div > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.relative.z-1.h-full > div > div > div.swiper-slide.swiper-no-swiping.swiper-slide-active > div > div.relative.h-full > div > div > div.swiper-slide.swiper-slide-active > div > div > div > div > ul > li:nth-child(1) > a > div.px-8.pt-9.pb-8.h-46 > div > p')
        webtoon_info.start_date = start_date.string.strip()

        # dict 형태로 변환
        webtoon_info.done()
        
        # 수행 여부를 확인하기위한 카운터
        count += 1
        print(count)

        sleep(1)

    webtoon_json = webtoon_info.make_json()
    print("done:",count)
    print("fail:", len(miss))
    print("miss:",miss)
    f.write(webtoon_json)
    f.write("\n")
    f.close()

miss = [] # 크롤링에 필패한 웹툰을 기록할 리스트
week = ["mon", "tue", "wed", "thu", "fri", "sat", "sun", "complete"]

if __name__ == "__main__":
    crawling("mon")