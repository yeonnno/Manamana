from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep, time
from dotenv import load_dotenv
from datetime import datetime
from webtoonUtil import *
import os
import sys
import webtoon

# 로그인하기
def login(driver):
    # .env 로드
    load_dotenv()

    id = os.environ.get('ID')
    pw = os.environ.get('PW')

    # 로그인 페이지로 이동
    driver.get('https://webtoon.kakao.com/more')
    sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, '#root > main > div > div > div.absolute.top-0.left-0.w-full.z-navigationBar > div.px-18.m-auto.items-center.flex.h-header-height.fixed.top-0.left-0.right-0.z-navigationBar > div.ml-auto.flex.flex-none > a').click()
    sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, 'body > div:nth-child(20) > div > div > div > div.overflow-x-hidden.overflow-y-auto.\!overflow-hidden.flex.flex-col > div.text-center.pb-\[117px\].overflow-y-auto > div > div > button').click()
    sleep(0.5)
    # 아이디, 비밀번호 입력
    driver.find_element(By.CSS_SELECTOR, '#loginKey--1').send_keys(id)
    driver.find_element(By.CSS_SELECTOR, '#password--2').send_keys(pw)
    sleep(0.5)
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

def crawling(driver, day_string, f):
    

    count = 0 # 성공한 웹툰 개수

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
        cnt = 0
        if count and count % 10 == 0:
            print("count-10! WAIT 10sec!!")
            sleep(10)

        webtoon_info = webtoon.Webtoon() # 웬툰 클래스 생성

        webtoon_url = kakao_base_url + url # 웹툰 주소 생성
        while cnt <= 2:
            try:
                driver.get(webtoon_url) # 이동
                
                idx = url.find("/", -5)
                webtoon_info.webtoon_id = url[idx+1:]
                
                sleep(0.5)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                genre = soup.select('#root > main > div > div.page.bg-background-02.activePage > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.w-full.left-0.top-0.relative > div.content-main-wrapper.opacity-0.invisible.relative.current-content-main.opacity-100.\!visible.z-1 > div.pb-20.pt-96.relative.z-1 > div.relative.mx-auto.my-0.w-full.lg\:w-default-max-width > div.mx-20.flex.justify-between.relative.z-1.pointer-events-auto.pt-12 > div > div > div:nth-child(1) > p')
                genre = genre[0].string.strip()
                if genre[-2:] == "무료":
                    genre = soup.select('#root > main > div > div.page.bg-background-02.activePage > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.w-full.left-0.top-0.relative > div.content-main-wrapper.opacity-0.invisible.relative.current-content-main.opacity-100.\!visible.z-1 > div.pb-20.pt-96.relative.z-1 > div.relative.mx-auto.my-0.w-full.lg\:w-default-max-width > div.mx-20.flex.justify-between.relative.z-1.pointer-events-auto.pt-12 > div > div > div:nth-child(2) > p')
                    genre = genre[0].string.strip()
                webtoon_info.genre_arr = genre.split()
                try:
                    driver.find_element(By.CSS_SELECTOR, '#root > main > div > div.page.bg-background-02.activePage > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.w-full.left-0.top-0.relative > div.content-main-wrapper.opacity-0.invisible.relative.current-content-main.opacity-100.\!visible.z-1 > div.pb-20.pt-96.relative.z-1 > div.relative.mx-auto.my-0.w-full.lg\:w-default-max-width > div.mx-20.flex.justify-between.relative.z-1.pointer-events-auto.pt-12 > div').click()
                except Exception as err:
                    print("False")
                    print(webtoon_url)

                    print(err)
                    miss.add(url)
                    continue

                sleep(1)

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
                    grade = "전체이용가"
                else:
                    grade = "성인"
                webtoon_info.grade = grade

                # 웹툰 이름 저장
                webtoon_info.name = soup.select_one('#root > main > div > div.page.bg-background-02.activePage > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.relative.z-1.h-full > div > div > div.swiper-slide.swiper-no-swiping.swiper-slide-active > div > div.relative.h-full > div > div > div.swiper-slide.swiper-slide-active > div > div > div > div > p').string.strip()

                # 웹툰 작가 리스트 저장
                webtoon_info.authors_arr = [
                    soup.select_one('#root > main > div > div.page.bg-background-02.activePage > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.relative.z-1.h-full > div > div > div.swiper-slide.swiper-no-swiping.swiper-slide-active > div > div.relative.h-full > div > div > div.swiper-slide.swiper-slide-active > div > div > div > div > dl > div:nth-child(1) > dd').string.strip(),
                    soup.select_one('#root > main > div > div.page.bg-background-02.activePage > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.relative.z-1.h-full > div > div > div.swiper-slide.swiper-no-swiping.swiper-slide-active > div > div.relative.h-full > div > div > div.swiper-slide.swiper-slide-active > div > div > div > div > dl > div:nth-child(2) > dd').string.strip()
                    ]
                
                # 웹툰 줄거리 저장
                plot = soup.select_one('#root > main > div > div.page.bg-background-02.activePage > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.relative.z-1.h-full > div > div > div.swiper-slide.swiper-no-swiping.swiper-slide-active > div > div.relative.h-full > div > div > div.swiper-slide.swiper-slide-active > div > div > div > div > div:nth-child(4) > div:nth-child(2) > p').string.strip()
                webtoon_info.plot = plot[:100]
                
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
                if total_ep:
                    total_ep = total_ep.string.strip()
                    if "화" in total_ep:
                        idx = total_ep.index("화")
                        total_ep = total_ep[:idx]
                    if not total_ep.isdigit():
                        total_ep = len(driver.find_elements(By.CSS_SELECTOR, '#root > main > div > div > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.relative.z-1.h-full > div > div > div.swiper-slide.swiper-slide-active > div > div.relative.h-full > div > div > div.swiper-slide.swiper-slide-active > div > div > div > div > ul > li'))
                webtoon_info.total_ep = total_ep
                driver.find_element(By.CSS_SELECTOR, '#root > main > div > div > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.relative.z-1.h-full > div > div > div.swiper-slide.swiper-no-swiping.swiper-slide-active > div > div.bottom-73.z-5.relative.flex-center.pointer-events-none > button').click()
                sleep(0.5)

                # 시작날짜 저장
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                start_date = soup.select_one('#root > main > div > div > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.relative.z-1.h-full > div > div > div.swiper-slide.swiper-no-swiping.swiper-slide-active > div > div.relative.h-full > div > div > div.swiper-slide.swiper-slide-active > div > div > div > div > ul > li:nth-child(1) > a > div.px-8.pt-9.pb-8.h-46 > div > p')
                webtoon_info.start_date = start_date.string.strip()

                # 색 저장
                webtoon_info.colorHsl = image_main_color_hsl(webtoon_info.image)

                # dict 형태로 변환
                webtoon_info.done()
                
                # 수행 여부를 확인하기위한 카운터
                count += 1
                print(count)

                sleep(1)
            except Exception as e:
                print(e)
                miss.add(url)
            cnt += 1
            if not webtoon_info.check_none():
                break
        else:
            print(f'name: {webtoon_info.name}')
            print(f'image: {webtoon_info.image}')
            print(f'plot: {webtoon_info.plot}')
            print(f'grade: {webtoon_info.grade}')
            print(f'status: {webtoon_info.status}')
            print(f'webtoon_url: {webtoon_info.webtoon_url}')
            print(f'webtoon_id: {webtoon_info.webtoon_id}')
            print(f'start_date: {webtoon_info.start_date}')
            print(f'total_ep: {webtoon_info.total_ep}')
            print(f'genre_arr: {webtoon_info.genre_arr}')
            print(f'day_arr: {webtoon_info.day_arr}')
            print(f'authors_arr: {webtoon_info.authors_arr}')
            print(f'colorHsl: {webtoon_info.colorHsl}')

    print("done:",count)
    print("fail:", len(miss))
    print("miss:",miss)
    

miss = set() # 크롤링에 필패한 웹툰을 기록할 리스트
week = ["mon", "tue", "wed", "thu", "fri", "sat", "sun", "complete"]
today = week[datetime.today().weekday()]


if __name__ == "__main__":
    arguments = sys.argv

    print("====================")
    if len(arguments) == 2:
        if arguments[1] == "all":
            week_arr = week
            print("Crawling All")
        else:
            if arguments[1] in week:
                week_arr = arguments[1].split()
                print(f'Crawling {arguments[1]}')
    else:
        week_arr = today.split()
        print(f'Crawling {today}')
    print("====================")
    
    start = time()

    f = open("webtoon.json", 'w', encoding="UTF-8") # json을 저장할 파일 지정

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")

    # linux 환경에서 필요한 option
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome("chromedriver", options=chrome_options) # 크롬 브라우저를 사용
    driver.implicitly_wait(10)

    try:
        print("-----Login-----")
        login(driver) # 카카오 웹툰 로그인
    except Exception:
        print("-----Fail-----")
        print("-----retry-----")
        sleep(5)
        print("-----Login-----")
        login(driver) # 카카오 웹툰 로그인
    print("-----succes-----")
    for week_string in week_arr:
        print(f"-----{week_string}-----")
        crawling(driver, week_string, f)

    total_webtoon = webtoon.Webtoon()
    webtoon_json = total_webtoon.make_json()


    f.write(webtoon_json)
    f.close()
    post_request(webtoon_json, url="http://crawling-spring-boot:8080/crawling")

    end = time()
    print(miss)
    print(f"{end - start:.5f} sec")


