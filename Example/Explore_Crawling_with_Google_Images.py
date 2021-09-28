from urllib.request import urlretrieve # image를 저장할 때 사용하기 위함
from urllib.parse import quote_plus    # 한글 검색 자동 변환
from bs4 import BeautifulSoup as bs   
from selenium import webdriver
import time as t
from typing import List
import os

def main():
    downloadImagesFileName = input("현재 폴더에서 다운로드할 이미지를 저장할 폴더 이름 : ")
    keyword: List[str] = input("Image Name : ").split()
    
    for word in keyword:
        # i_URL 설명 링크 : https://ssung85.tistory.com/81
        i_URL = f'https://www.google.com/search?q={quote_plus(word)}&sxsrf=ALeKk00OQamJ34t56QSInnMzwcC5gC344w:1594968011157&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjXs-7t1tPqAhVF7GEKHfM4DqsQ_AUoAXoECBoQAw&biw=1536&bih=754'

        # 크럼 드라이버 설치 설명 링크 : https://m.blog.naver.com/jsk6824/221763151860 
        driver_path = 'C:\\Users\\pksmb\\Desktop\\Project\\chromedriver.exe'
        # 크롬 드라이버로 크롬 실행
        driver = webdriver.Chrome(driver_path) 

        # ------------ webdriver로 여러가지 옵션을 설정할 때 사용한다.
        # options = webdriver.ChromeOptions()
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # -------------------------------------------

        # 저장한 url 주소로 이동
        driver.get(i_URL) 

        # 자동 스크롤
        # 참고 링크 : https://cottonwood-moa.tistory.com/34
        # Get scrool height
        # execute_script method의 내부 명령어는 Javascript 명령어이다.
        print('Scrolling automatically')
        last_height = driver.execute_script('return document.body.scrollHeight')
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            t.sleep(1.5)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                try:
                    driver.find_element_by_css_selector(".mye4qd").click()
                except:
                    break
            last_height = new_height

        # Create some code for saving the images
        html = driver.page_source
        soup = bs(html, features="html.parser")

        images = soup.select('img')

        images_list = []

        print(f"Searching {word} Images")
        for image in images:
            try:
                images_list.append(image.attrs["src"])
            except KeyError:
                images_list.append(image.attrs["data-src"])
        print('Searching... Done')

        print(f"Downloading {word} Images")
        os.makedirs(name=downloadImagesFileName, exist_ok=True)
        for num, image in enumerate(images_list): # 개수 조절 images_list[:100]
            os.makedirs(name=f'{downloadImagesFileName}/{word}', exist_ok=True)
            urlretrieve(url=image, filename=f'{downloadImagesFileName}/{word}/{word}_{str(num)}' + '.jpg')
        print('Downloading... Done')

        # 크롬 드라이버로 열었던 Window를 닫는다.
        driver.close()
    print("Finish")

if __name__ == '__main__':
    main()