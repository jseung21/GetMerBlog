from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os

def save_blog_posts():
    driver = None
    try:
        print("프로그램 시작...")
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"현재 디렉토리: {current_dir}")
        
        # 목록 파일 읽기
        list_file = os.path.join(current_dir, '메르경제관련글목록.txt')
        print(f"목록 파일 경로: {list_file}")
        
        print("\n파일 전체 읽기 시작...")
        with open(list_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        print(f"총 {len(lines)}줄을 읽었습니다.")
        
        # 제목과 링크 추출
        posts = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if '. 제목:' in line:  # 제목 줄 찾기
                title = line.split('제목:', 1)[1].strip()
                if i + 1 < len(lines):
                    link_line = lines[i + 1].strip()
                    if '링크:' in link_line:
                        link = link_line.split('링크:', 1)[1].strip()
                        posts.append({'title': title, 'url': link})
                i += 3  # 다음 포스트로 건너뛰기
            else:
                i += 1
        
        print(f"\n총 {len(posts)}개의 포스트를 찾았습니다.")
        
        if len(posts) > 0:
            # MerBlogs 폴더 생성
            merblogs_dir = os.path.join(current_dir, 'MerBlogs')
            os.makedirs(merblogs_dir, exist_ok=True)
            print(f"MerBlogs 폴더 준비 완료: {merblogs_dir}")
            
            print("\nChrome WebDriver 초기화 중...")
            options = webdriver.ChromeOptions()
            options.add_argument('--start-maximized')
            driver = webdriver.Chrome(options=options)
            wait = WebDriverWait(driver, 10)
            print("Chrome WebDriver 초기화 완료")
            
            # 각 포스트 처리
            for i, post in enumerate(posts, 1):
                try:
                    # 파일명에 부적합한 문자를 "_"로 치환
                    safe_title = post['title']
                    # 윈도우 파일시스템에서 사용할 수 없는 문자들
                    invalid_chars = r'<>:"/\|?*'
                    for char in invalid_chars:
                        safe_title = safe_title.replace(char, '_')
                    # 추가적인 특수문자도 "_"로 치환
                    safe_title = ''.join(c if c.isalnum() or c in (' ', '-', '_', '.') else '_' for c in safe_title)
                    safe_title = safe_title.strip()
                    
                    file_path = os.path.join(merblogs_dir, f'{safe_title}.txt')
                    
                    # 이미 처리된 파일 건너뛰기
                    if os.path.exists(file_path):
                        print(f"\n[{i}/{len(posts)}] 이미 처리됨: {safe_title}")
                        continue
                        
                    print(f"\n[{i}/{len(posts)}] 처리 중: {safe_title}")
                    print(f"URL: {post['url']}")
                    
                    driver.get(post['url'])
                    print("페이지 로딩 중...")
                    time.sleep(3)
                    
                    # 본문 내용 찾기
                    print("본문 내용 추출 중...")
                    content_elements = driver.find_elements(By.CLASS_NAME, 'se-text-paragraph')
                    content = '\n'.join([elem.text for elem in content_elements if elem.text.strip()])
                    
                    if not content:
                        print("본문을 찾을 수 없습니다. 다른 방법 시도...")
                        content_elements = driver.find_elements(By.CLASS_NAME, 'se-component')
                        content = '\n'.join([elem.text for elem in content_elements if elem.text.strip()])
                    
                    if content:
                        print(f"본문 길이: {len(content)} 글자")
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(f"제목: {post['title']}\n\n")
                            f.write(content)
                        
                        print(f"저장 완료: {file_path}")
                    else:
                        print("본문 내용을 찾을 수 없습니다.")
                    
                    time.sleep(1)
                    
                except TimeoutException:
                    print(f"시간 초과: {safe_title}")
                    continue
                except Exception as e:
                    print(f"포스트 처리 중 오류 발생: {str(e)}")
                    continue
                    
        else:
            print("처리할 포스트가 없습니다.")
                
    except Exception as e:
        print(f"프로그램 실행 중 오류 발생: {str(e)}")
        
    finally:
        if driver:
            print("\nChrome WebDriver 종료 중...")
            driver.quit()
            print("Chrome WebDriver 종료 완료")

if __name__ == "__main__":
    save_blog_posts()
    print("\n프로그램 종료")
