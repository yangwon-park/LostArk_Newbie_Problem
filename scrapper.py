import time, random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('window-size=2560x1440')
options.add_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36')

driver = webdriver.Chrome()

# 게시판 : 질문과 답변 (한 페이지에 50개)
# 키워드 : 뉴비
# 최근 한달 뉴비의 어려움 => 8 페이지
# 총 400개의 게시글을 토대로 분석 시작
url = 'https://www.inven.co.kr/board/lostark/4822?query=list&p=1&sterm=&name=subject&keyword=%EB%89%B4%EB%B9%84'
driver.get(url)

# 게시글 하나 클릭
board = driver.find_elements(By.CLASS_NAME, 'tit')
time.sleep(random.uniform(1, 3))

for b in board:
    print(b.text)
    print(len(board))

title = driver.find_element(By.CLASS_NAME, 'articleTitle').text
time.sleep(random.uniform(1, 3))
content = driver.find_element(By.ID, 'powerbbsContent').text
time.sleep(random.uniform(1, 3))
comment = driver.find_element(By.CLASS_NAME, 'comment').text

# print(comment)