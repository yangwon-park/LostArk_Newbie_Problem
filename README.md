# LostArk Newbie Problem

## 계획 이유

특정한 게임에 유저들의 로열티가 충분한 경우 그 유저들은 다른 게임을 하다가도 결국엔 귀소 본능처럼 다시 자신이 재밌어하고 즐겨하던 그 게임으로 돌아오는 것을 많이 목격했습니다. 이를 참고로 봤을 때 기존 유저들을 붙잡아 두는 것도 중요하지만, 게임의 가장 중요한 요소는 **신규 유저들의 리텐션**이라고 생각합니다.

<center><h5>(절대 기존 유저를 등한시 하는 것은 아닙니다!)</h5></center>

정말 많은 분들이 게임을 취미로 가지고 여가 시간을 보내는데, 생각보다 많은 유저분들이 뉴비일 때 진입 장벽을 크게 느껴 초기 콘테츠에서부터의 이탈률이 높습니다. 저 또한 많은 게임을 접해보았고 스스로 헤비한 게이머라고 생각하는 편입니다. 하지만 그런 저와 제  주변 지인들도 새로운 게임에 도전 할 때 막막함과 두려움이 느껴집니다.

---

<span style="font-size:120%">최근 '로스트아크'를 다시 시작하려는 유저의 입장에서 출시가 그렇게 오래되지 않았고 게임의 UI가 크게 불편하지 않았음에도 생각보다 쉽게 게임에 적응하지 못하는 제 모습이 보였습니다.</span>

---

이에 따라 뉴비들이 느끼는 문제점을 파악하고 분석하여 저와 제 지인들은 물론 정말 많은 게이머분들에게 도움이 되고 게임 기업의 입장에서 어떻게 하면 **유저 리텐션**을 높일 수 있을지 공부해보고자 이 프로젝트를 기획하게 됐습니다.

<br/>

## 기술 스택

- IDE : **Jupter Notebook**

- Python 3.9
  - BeautifulSoup (4.10.0)
  - Selenium (4.1.0)
  - Pandas (1.3.4)
  - Numpy (1.20.3)

## 참고 사이트 (추가 예정)

<span style="font-size: 300%">👨‍✈️</span>Robots.txt 참고하여 스크래핑하였지만 혹시 문제가 된다면 말씀해주세요!!!

- [LostArk 인벤 - 질문과 답변 게시판](https://www.inven.co.kr/board/lostark/4822)



## 개발 과정

### 00. 기본 개발환경 구성

```python
import time, random
import requests, re, csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# 브라우저를 실행시키고 싶지 않을 때 부여하는 옵션
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('window-size=2560x1440')

# 아래와 같이 User-Agent를 임의로 부여하지 않으면
# Chrome이 아니라 HeadlessChrome으로 들어가
# 사이트 측에 벤 당할 수도 있다
options.add_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36')

# 브라우저를 실행하고 싶지 않으면 주석 제거
# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome()
```

---

<span style="font-size:120%">해당 코드는 크롤러가 아니라 단순히 데이터 수집을 하기 위한 스크래퍼입니다.<br/>즉, 사이트의 구조가 변경되면 언제든지 코드가 작동하지 않을 수도 있습니다.</span>

[웹 크롤러에 대한 참고 블로그](https://velog.io/@mowinckel/%EC%9B%B9-%ED%81%AC%EB%A1%A4%EB%A7%81-I)

---

<br/>

### 01. LostArk 인벤 스크래핑

- 게시판 : 질문과 답변 (페이지 당 게시글 50개)
- 검색 키워드 : 뉴비
- 최근 한달 뉴비의 어려움에 관련된 게시글을 모음 (7페이지 정도)
- 총 350개의 게시글을 데이터로 수집

#### 01-1. 게시글 번호 가져오기

- 처음 생각한 메커니즘

  - '뉴비' 검색 => 게시글 클릭 => 스크래핑 => 뒤로가기 => 다음 게시글 클릭 => 페이지 이동

  - 위와 같이 하니 아래와 같은 에러가 발생함

  - ```python
    # "Message: stale element reference: element is not attached to the page document"
    ```

  - Selenium 객체가 뒤로가기 과정에서 새로고침되어 매번 객체를 재호출해야하는 문제가 발생

  - 위의 에러가 다른 곳에서도 발생한다면 코드 사이에 interval을 줘서 로드가 될 때까지 조금 기다려준다

- 두 번째 메커니즘
  - '뉴비' 검색 => 게시글 번호 스크래핑 => 번호 별 url 접근 => 스크래핑 => 페이지 이동
  - 작동은 되지만 이것보다 한 번에 게시글 번호를 불러온 후 작업하는게 더 용이하다고 판단
- 세 번째 메커니즘 (선택)
  - '뉴비' 검색 => 모든 페이지 게시글 번호 스크래핑 => 번호 별 url 접근 => 스크래핑
- 게시글 번호 스크래핑 코드

```python
# 게시글의 번호를 받아올 리스트 선언
# 최근 게시글의 번호부터 들어가므로 내림차순 정렬된다
num=[]

# 7페이지 (대략 한달 누적 게시글) 확인
for i in range(1, 8):
    
    # 게시판 페이지 url
    main_url = "https://www.inven.co.kr/board/lostark/4822?name=subject&keyword=%EB%89%B4%EB%B9%84&p={}".format(i)
    
    driver.get(main_url)

    # 게시글 번호 받아오기
    # 게시글 하나 하나에 직접 접근하려고 하니까
    # element is not attached to the page document 에러 발생
    # 이 경우 selenium 객체를 매번 새로 생성하려하니 비효율적인 것 같아
    # 차라리 처음 로딩 때 게시글 번호를 받은 후, 해당 번호로 게시글에 접근하는 것이
    # 더 용이하다고 판단
    board_num = driver.find_elements(By.CLASS_NAME, 'num')  

    for b in board_num:
        num.append(b.text)

    # CLASS_NAME이 num인 태그가 또 존재해서 다른 값도 들어옴
    # 필요없는 값들은 제거
    # 빈 문자열과 최근 게시글 번호에 비해 값이 매우 작은 번호는 다 제외
    num = [x for x in num if x and int(x) > 20] 
```

#### 01-2. 게시글 제목, 내용, 댓글 가져오기

- 뉴비 유저들의 고충을 분석하기 위해 게시글의 제목, 내용, 댓글을 가져옴
- [필요없는 태그 삭제 참고](https://lovelydiary.tistory.com/17)
- [\xa0 삭제 참고](https://stackoverflow.com/questions/10993612/how-to-remove-xa0-from-string-in-python)
- 제목, 내용, 댓글 가져오기 코드

```python
#  정상 작동하는지 확인하는데 모든 게시글을 다 쓰기엔
# 테스트에 시간이 너무 오래 걸려서
# 스크래핑한 게시물 번호 중 3개만 사용
# num = num[:3]

# 최종적으로 모든 내용을 담을 리스트
result = []

for i in num:
    url = 'https://www.inven.co.kr/board/lostark/4822/{}?name=subject&keyword=%EB%89%B4%EB%B9%84'.format(i)

    # driver.get(url)
    res = requests.get(url, headers=headers)

    # 에러 발생시 종료
    res.raise_for_status()

    soup = BeautifulSoup(driver.page_source, 'lxml')
    
    time.sleep(random.uniform(1,3))
    
    title = soup.find("div", attrs={"class":"articleTitle"})
    content = soup.find("div", attrs={"id":"powerbbsContent"})  
    
    # 댓글은 엘리먼트가 여러개
    # find_all로 받아오면 html 태그와 non-breaking space 코드(\xa0)가 같이 들어옴
    # 더티 데이터를 최소화 하기 위해 전처리
    # 댓글이 없는 경우 => '' 으로 입력됨
    comment = soup.find_all("div", attrs={"class":"comment"})  
    comment = str(comment)
    comment = re.sub('<.+?>','',comment,0).strip()  # html 제거
    comment = comment.replace(u'\xa0', u'')        # \xa0 제거
    comment = comment.lstrip('[').rstrip(']')            # 댓글의 양 끝에 []가 딸려오길래 제거
    
    result.append([title.text.strip(), content.text, comment])
    
print(len(result)) # 최종 결과의 길이가 350이면 정상
```

#### 01-3. csv 파일로 내보내기

- 이 과정에서 모든 데이터가 csv에 담기지 않는 경우가 있음

```python
today = datetime.today().strftime("%Y_%m_%d")
filename = today + '로아_final.csv'

# encoding을 다음과 같이 주지 않으면
# 한글이 깨져 나온다
f = open(filename, 'w', encoding='utf-8-sig', newline='')
writer = csv.writer(f)
title = "title,content,comment".split(',')
    
writer.writerow(title)
writer.writerows(result)
```

<br/>

### 02. CSV 파일로 데이터 분석

- 01 과정에서 추출한 데이터를 활용하여 분석을 시작

#### 02-1. 
