from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import os

# Naver 블로그 URL
url = "https://blog.naver.com/ranto28"

# Chrome WebDriver 초기화
driver = webdriver.Chrome()
driver.get(url)

try:
    # 현재 실행 파일의 경로를 가져옴
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_dir, '메르경제관련글.txt')
    
    # iframe 로딩 대기 및 전환
    time.sleep(2)
    iframe = driver.find_element(By.ID, 'mainFrame')
    driver.switch_to.frame(iframe)
    
    results = []
    page_num = 1
    
    while True:
        print(f"\n=== {page_num}페이지 처리 중 ===")
        
        # 게시물 링크 찾기
        posts = driver.find_elements(By.CSS_SELECTOR, 'a.pcol2._setTop._setTopListUrl')
        
        # 현재 페이지의 게시물 처리
        for post in posts:
            try:
                title = post.text.strip()
                link = post.get_attribute('href')
                if title and link:
                    results.append({'title': title, 'url': link})
                    print(f"제목: {title}")
                    print(f"링크: {link}")
                    print("-" * 50)
            except Exception as e:
                print(f"게시물 처리 중 오류 발생: {e}")
                continue
        
        # 다음 페이지 버튼 찾기
        try:
            # 현재 페이지의 다음 페이지 번호 찾기
            next_page = None
            pages = driver.find_elements(By.CSS_SELECTOR, '.blog2_paginate a.page, .blog2_paginate strong.page')
            
            for page in pages:
                if page.get_attribute('class').startswith('page'):
                    page_text = page.text.strip()
                    if page_text.isdigit() and int(page_text) == page_num + 1:
                        next_page = page
                        break
            
            # 다음 페이지가 없으면 종료
            if not next_page:
                # 다음(>) 버튼 확인
                next_button = driver.find_element(By.CSS_SELECTOR, 'a.next.pcol2._goPageTop')
                if next_button:
                    next_button.click()
                else:
                    print("\n마지막 페이지에 도달했습니다.")
                    break
            else:
                next_page.click()
            
            # 페이지 로딩 대기
            time.sleep(2)
            
            # iframe 재설정
            driver.switch_to.default_content()
            iframe = driver.find_element(By.ID, 'mainFrame')
            driver.switch_to.frame(iframe)
            
            page_num += 1
            
        except NoSuchElementException:
            print("\n마지막 페이지에 도달했습니다.")
            break
        except Exception as e:
            print(f"\n페이지 이동 중 오류 발생: {e}")
            break

    print(f"\n총 {len(results)}개의 게시물을 찾았습니다.")
    
    # 결과를 파일로 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, result in enumerate(results, 1):
            f.write(f"{i}. 제목: {result['title']}\n")
            f.write(f"   링크: {result['url']}\n")
            f.write("-" * 50 + "\n")
        
    print(f"\n모든 결과가 '{output_file}'에 저장되었습니다.")

except Exception as e:
    print(f"오류 발생: {e}")

finally:
    driver.quit()
