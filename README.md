# LostArk Newbie Problem

## 기획 이유

특정한 게임에 유저들의 로열티가 충분한 경우 그 유저들은 다른 게임을 하다가도 결국엔 귀소 본능처럼 다시 자신이 재밌어하고 즐겨하던 그 게임으로 돌아오는 것을 많이 목격했습니다. 이를 참고로 봤을 때 기존 유저들을 붙잡아 두는 것도 중요하지만, 게임의 가장 중요한 요소는 **신규 유저들의 리텐션**이라고 생각합니다.

<center><h5>(절대 기존 유저를 등한시 하는 것은 아닙니다!)</h5></center>

정말 많은 분들이 게임을 취미로 가지고 여가 시간을 보내는데, 생각보다 많은 유저분들이 뉴비일 때 진입 장벽을 크게 느껴 초기 콘텐츠에서부터의 이탈률이 높습니다. 저 또한 많은 게임을 접해보았고 스스로 헤비한 게이머라고 생각하는 편입니다. 하지만 그런 저와 제  주변 지인들도 새로운 게임에 도전 할 때 막막함과 두려움이 느껴집니다.

---

<span style="font-size:120%">최근 '로스트아크'를 다시 시작하려는 유저의 입장에서 출시가 그렇게 오래되지 않았고 게임의 UI가 크게 불편하지 않았음에도 생각보다 쉽게 게임에 적응하지 못하는 제 모습이 보였습니다.</span>

---

이에 따라 뉴비들이 느끼는 문제점을 파악하고 분석하여 저와 제 지인들은 물론 정말 많은 게이머분들에게 도움이 되고 게임 기업의 입장에서 어떻게 하면 **유저 리텐션**을 높일 수 있을지 공부해보고자 이 프로젝트를 기획하게 됐습니다.

<br/>

## 기술 스택 및 버전

- OS : Windows 10

- Anaconda (가상환경 이름 : 3_7)
- IDE : **Jupter Notebook**
- Python 3.7 (Mecab이 3.8 이상 지원 안 함)
  - BeautifulSoup (4.10.0)
  - Selenium (4.1.0)
  - pandas (1.3.4)
  - numpy (1.19.5)
- 자연어 처리
  - KoNLPy - Mecab (설치 방법 아래 참고)
    - jdk 1.8
    - JPype1-1.3.0-cp37-cp37-win_amd64.whl
    - mecab_python-0.996_ko_0.9.2_msvc-cp37-cp37m-win_amd64.whl
    - mecab-ko-msvc (0.9.2)
    - mecab-ko-dic-mscv (2.1.1)

  - PyKoSpacing - Spacing (띄어쓰기 처리)
    - numpy 1.20 넘으면 Tensoflow 미지원으로 에러 발생

- VCS  : Github

## 참고 사이트 (추가 예정)

<span style="font-size: 300%">👨‍✈️</span>Robots.txt 참고하여 스크래핑하였지만 혹시 문제가 된다면 말씀해주세요!!!

- [LostArk 인벤 - 질문과 답변 게시판](https://www.inven.co.kr/board/lostark/4822)
- [LostArk 공홈 - Q&A 게시판](https://lostark.game.onstove.com/Library/Qa/List) (아직 X)



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
- 검색 키워드 : 뉴비, 모코코(추가 예정)
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

#### 02-0. matplotilb 한글 폰트 깨짐 방지 (시스템 영구 등록)

0. 한글 폰트 설치 완료 - [네이버 폰트](https://hangeul.naver.com/2017/nanum)

1. 아래 코드로 설치

```python
import matplotlib as mpl
import matplotlib.pyplot as plt

# matplotlibrc 파일의 경로 확인
print(mpl.matplotlib_fname())

# 위의 경로에 있는 matplotlibrc 파일을 수정
# font.family 부분의 주석을 제거하고
# sans_serif => 원하는 폰트(ex NanumGothic)로 변경
# axes.unicode_minus의 값 True => False로 변경

# 해당 폴더로 이동하여 내부 파일 전부 삭제 (캐시 삭제)
print(mpl.get_cachedir())

# 주피터 노트북 재시작

plt.figure().add_subplot().set_title('안녕하세요')
plt.show()
```

#### 02-1. 데이터 구조 파악

```python
import pandas as pd
import numpy as np
import seaborn as sns

# 앞서 저장했던 csv 파일 불러오기
df = pd.read_csv('2022-02-24로아_final.csv')

# row, col 파악
# 결측값이 들어오지 않아서 예정된 350개 보다 더 작은 340개의 데이터가 들어옴
df.shape

# 결측치 확인 => 없음
df.isnull().sum()

# 전체 데이터 구조 파악
df.info()

# 상위 5개 데이터 확인
df.head()

# 혹시나 중복되어 들어온 데이터가 있나 확인
df = df.drop_duplicates(['title', 'content'], keep='first')

# 기존값과 변화 없으므로 중복된 데이터가 없다고 판정
df.shape
```

#### 02-2. 데이터 전처리

- [자연어 처리 참고](https://wikidocs.net/92961)
    
1. 형태소 분석기
    - KoNLPY 설치
        - [KoNLPy API](https://konlpy.org/ko/v0.4.3/morph/)
        - [KoNLPY 설치 참고](https://konlpy.org/en/latest/install/)
        - Windows에서 KoNLPY를 사용하려면 jdk1.7 이상이 설치되어 있어야 함
            - [jdk1.8 설치](https://www.oracle.com/java/technologies/downloads/#java8-windows)
        - pip install --upgrade pip
        - [JPype 다운로드](https://www.lfd.uci.edu/~gohlke/pythonlibs/#jpype)
        - pip install JPype1-1.3.0-cp37-cp37-win_amd64.whl
            - 0.5.7 이상, 본인 파이썬 버전, 윈도우 32 or 64 bit에 맞춰서 설치
            - whl 파일을 다운로드 받은 경로에서 해당 명령어 실행   
        - pip install konlpy
    - Mecab 설치
        - [Mecab API](https://konlpy-ko.readthedocs.io/ko/v0.6.0/api/konlpy.tag/#mecab-class)
        - [Mecab 설치 참고](https://lsjsj92.tistory.com/612)
        - [Mecab tag표](https://openuiz.tistory.com/90)
        - [mecab-ko-msvc](https://github.com/Pusnow/mecab-ko-msvc/releases/tag/release-0.9.2-msvc-3) => 윈도우 bit에 맞춰서 다운로드
        - [mecab-ko-dic-msvc.zip](https://github.com/Pusnow/mecab-ko-dic-msvc/releases/tag/mecab-ko-dic-2.1.1-20180720-msvc-2) => mecab-ko-dic-msvc.zip 다운로드
        - C:/에 mecab 디렉토리 생성 => 위 두 zip파일 mecab 디렉토리에 압축해제
        - [mecab_python-0.996_ko_0.9.2_msvc-cp37-cp37m-win_amd64.whl](https://github.com/Pusnow/mecab-python-msvc/releases/tag/mecab_python-0.996_ko_0.9.2_msvc-2)
            - 본인 파이썬 버젼, 윈도우 32 or 64 bit에 맞춰서 설치 (3.8 이상 지원 X)
            - whl 파일을 다운로드 받은 경로에서 해당 명령어 실행
2. 띄어쓰기 확인 패키지
    - PyKoSpacing 설치
        - pip install git+https://github.com/haven-jeon/PyKoSpacing.git
    
- 연습

  ```python
  from konlpy.tag import Mecab
  
  # Mecab은 일반적인 Konlpy의 토크나이저와는 다르게 dicpath를 파라미터로 지정해줘야함
  # mecab-ko-dic-msvc.zip의 압축을 푼 경로에 있음
  m = Mecab('C:\mecab\mecab-ko-dic')
  m.morphs(u'아버지가방에들어가신다')
  
  # 출력 (list)
  # ['아버지', '가', '방', '에', '들어가', '신다']
  ```

### 03. 케이스 별 WordCloud 만들기

#### 03-1. Case-01

- 형태소 분석기 : Mecab
- 띄어쓰기 처리 : O (Spacing)

- 사용 컬럼 : 제목, 본문

- 데이터 종류 : 한글, 숫자

- RPG 게임 특성상 레벨, 과금 요소가 영향을 줄 거라고 판단하여 숫자도 남겨둠

  ```python
  # 데이터를 붙이는 도중에 단어끼리 붙어버리는 경우가 있어서 공백 추가
  df['title_content'] = df['title'].values + ' ' + df['content'].values
  
  # 한글, 숫자 데이터만 남겨둠
  df['ko_num_title_content'] = df['title_content'].apply(lambda x: re.sub('[^0-9가-힣\s]','',x))
  
  # ko_num_title_content 컬럼의 값들을 list로 만듬
  ko_num_title_content_list = list(df['ko_num_title_content'].values)
  
  # 띄어쓰기 처리해준 값들을 담을 list
  spacing_ko_num_title_content_list = []
  
  # PyKoSpacing를 사용하여 띄어쓰기 적용
  for i in ko_num_title_content_list:
      spacing_ko_num_title_content_list.append(spacing(i))
  
  # 띄어쓰기 적용한 문장의 명사들을 담을 리스트
  spacing_ko_num_title_content_word_lst = []
  
  # 띄어쓰기 적용한 리스트의 명사들만 따로 담음
  for word in spacing_ko_num_title_content_list:
      for i in range(len(m.nouns(word))):
          spacing_ko_num_title_content_word_lst.append(m.nouns(word)[i])
          
  # Counter 라이브러리로 각각의 개수 센 후 많은 순서대로 내림차순 정렬
  from collections import Counter
  count = Counter(spacing_ko_num_title_content_word_lst)
  words_dict = dict(count)
  words_dict = sorted(words_dict.items(), key=lambda item: item[1], reverse=True)        
  
  words_dict = dict(count)
  
  # 분석 결과를 보기 위해 WordCloud 사용
  from wordcloud import WordCloud
  
  # 폰트를 프로젝트 폴더에 그냥 복사해서 바로 불러옴
  wordcloud = WordCloud(font_path='NanumBarunGothic.ttf', width=500, height=500, background_color='white').generate_from_frequencies(words_dict)
  
  # WordCloud 출력
  plt.figure(figsize=(7,7))
  plt.imshow(wordcloud)
  plt.axis('off')
  plt.show()
  ```

- 결과 WordCloud

<p align="center"><img style="width:70%" src='https://user-images.githubusercontent.com/97505799/155759219-edc6ed66-10b3-4c33-b3b8-8e75bca9ff84.png'></p>

- Case-01. 결론
  - WordCloud에 더티 데이터가 너무 많다.
    - 불용어 선정을 할 엄두가 나지 않을 만큼 더티 데이터가 많다 ㅠㅠ.
      - 게임 관련 게시글인 만큼 고유명사가 많아서 PyKoSpacing을 적용하면 더티 데이터가 많이 발생
      - 해당 명사들을 따로 처리해주자!

#### 03-2. Case-02

- 형태소 분석기 : Mecab
- 띄어쓰기 처리 X
- Mecab 사용자 Dict 설정
  - (방법 추가 예정)

- 사용 컬럼 : 제목, 본문
- 데이터 종류 : 한글, 숫자

```python
# 한글, 숫자 데이터만 남겨둠
df['ko_num_title_content'] = df['title_content'].apply(lambda x: re.sub('[^0-9가-힣\s]','',x))

# ko_num_title_content 컬럼의 값들을 list로 만듬
ko_num_title_content_list = list(df['ko_num_title_content'].values)

# 명사들을 담을 리스트
ko_num_title_content_word_lst = []

for word in ko_num_title_content_list:
    for i in range(len(m.nouns(word))):
        ko_num_title_content_word_lst.append(m.nouns(word)[i])
        
# 불용어
# 뉴비, 질문, 만약, 입문, 처음과 같은 단어들은
# 어려운 점 자체와는 거리가 있는 단어들이기 때문에
# 불용어로 선정

# 동음이의어 선정 기준 => 더 많이 나온 단어로 선정
# 건슬 => 건슬링어가 따로 있어서 불용어 선정
# 캐릭터 => 캐릭이 따로 있어서 불용어 선정
stop_words='뉴비 질문 그거 건 드 때 만 번 캐 차 부탁 추천 사 안녕 \
            둘 디 막 입문 처음 건가요 데 팁 방법 필요 뭘 트 여 등등 후 \
            이게 노 이후 포 만약 내 건지 쌩 지 나 다음 방향 카 건슬 로아 \
            로스트아크 중 게임 시작 개 캐릭터 뭐 퀘 정도 여기 조언 현재 고민 \
            저 생각 글 제 것'

# 불용어 적용
ko_num_title_content_word_lst = [word for word in ko_num_title_content_word_lst
                                    			if not word in stop_words]

# Counter 라이브러리로 단어의 빈도수 체크 후 많은 순서대로 내림차순 정렬
from collections import Counter
count = Counter(ko_num_title_content_word_lst)
words_dict = dict(count)
words_dict = sorted(words_dict.items(), key=lambda item: item[1], reverse=True)

# 정렬 후 list로 반환되어 다시 dict로 변환
words_dict = dict(count)

from wordcloud import WordCloud
# 폰트를 프로젝트 폴더에 그냥 복사해서 바로 불러왔습니다.
wordcloud = WordCloud(font_path='NanumBarunGothic.ttf', 
                      min_font_size=7, max_font_size=150,
                      margin=3, width=500, height=500,
                      background_color='white').generate_from_frequencies(words_dict)

# WordCloud 출력
plt.figure(figsize=(10,10))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()
```

- 결과 WorldCloud

<p align="center"><img style="width:70%" src='https://user-images.githubusercontent.com/97505799/155831438-e1e3cf20-9c75-4926-af01-378780fe2c75.png'></p>

- Case-02. 결론
  - 띄어쓰기를 하지 않고 Mecab의 사용자 Dictionary를 사용하니 확실히 더티 데이터가 줄어들었다.
  - 직업 고민에 대한 고민이 역시 많고, 뉴비들에게 하익, 스익과 같은 점핑 익스프레스 시스템이 생각보다 어렵다고 느끼는 것 같다.

#### 03-3. Case-03

- 형태소 분석기 : **soynlp**
- content는 답변 위주의 데이터라 1차적으로 제목, 본문 내용으로만 처리
- soynlp 설치
  - pip install soynlp

```python
# 한글, 숫자 데이터만 남겨둠
df['ko_num_title_content'] = df['title_content'].apply(lambda x: re.sub('[^0-9가-힣\s]','',x))

# ko_num_title_content 컬럼의 값들을 list로 만듬
ko_num_title_content_list = list(df['ko_num_title_content'].values)

# WordExtractor의 3가지 알고리즘
# Branching Entropy
# Accessor Variety
# Cohesion Score
# WordExtractor를 이용하여 세개의 알고리즘에 대해 계산한 각 단어별 score를 집계
from soynlp.word import WordExtractor

# API 기본 파라미터 설정값 그대로 사용
we = WordExtractor(min_frequency=100,
                    min_cohesion_forward=0.05,
                    min_right_branching_entropy=0.0
)
we.train(df['ko_num_title_content'].values)
words = we.extract()

# 한글은 L + R의 언어 패턴을 가지고 있음
# 그 중 L부분에 해당하는 명사, 형용사 등을 가지고 옴
from soynlp.tokenizer import LTokenizer

cohesion_score = {word:score.cohesion_forward for word, score in words.items()}
tokenizer = LTokenizer(scores=cohesion_score)

# 위에서 생성한 토크나이저를 
# 해당 컬럼에 적용
df['token'] = df['ko_num_title_content'].apply(lambda x: tokenizer.tokenize(x, remove_r=True))

soy_token = []
for i in df['token'].values:
    for k in i:
        soy_token.append(k)

# 불용어
stop_words='뉴비 질문 더 제가 좀 부탁드립니다 하나 싶어서 왜 뭔가 전부 꼭 시작한지 \
            되나요 되는 너무 하면 해야 같아서 도와주세요 안녕하세요 잘 지금 그냥 \
            하는 관련 될까요 근데 이번에 정말 있고 중에 같이 모르고 및 다시 아니면 \
            다른 어떤 된 감사하겠습니다 좋을지 하루 하려고 맞추고 했는데 \
            같은데 알려주세요 원래 궁금합니다 뭐가 그리고 바로 보니까 있을까요 \
            또 오늘 나머지 하나요 일단 이제 해서 있는데 써서 첫 있어서 있나요 아직 \
            어떻게 혹시 계속 이미 따로 쓰고 어제 보니까 이것저것 우선 모르겠네요 \
            없이 어떤게 알려주시면 모르겠습니다 매일 저는 보고 있는지 맞는지 계정 \
            있습니다 빨리 어떤게 있다고 싶은데 부탁드려요 대충 적용해서 여기서 \
            맞나요 갈 완전 있으면 입니다 없어서 하면서 추천좀 좋은 할 하고 많이 \
            이렇게 걍 그래도 좋나요 1 33333 3333 3 몇가지 가도 해야하는지'

# 불용어 적용
soy_token = [word for word in soy_token if not word in stop_words]        
  
# Counter 라이브러리로 단어의 빈도수 체크 후 많은 순서대로 내림차순 정렬
from collections import Counter
count = Counter(soy_token)
words_dict = dict(count)
words_dict = sorted(words_dict.items(), key=lambda item: item[1], reverse=True)

# 정렬 후 list로 반환되어 다시 dict로 변환
words_dict = dict(count)

from wordcloud import WordCloud
# 폰트를 프로젝트 폴더에 그냥 복사해서 바로 불러왔습니다.
wordcloud = WordCloud(font_path='NanumBarunGothic.ttf', 
                      min_font_size=7, max_font_size=150,
                      margin=3, width=500, height=500,
                      background_color='white').generate_from_frequencies(words_dict)

# WordCloud 출력
plt.figure(figsize=(10,10))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()    
```

- 결과 WordCloud

<p align="center"><img style="width:70%" src='https://user-images.githubusercontent.com/97505799/155882519-9884ea7e-c296-43fd-bb8c-a7f1e47f8f1d.png'></p>

- Case03. 결론
  - 비지도 학습 기반이라 별도의 명사처리를 하지 않아도 고유 명사들에 상대적으로 좋은 성능을 보여줌
  - 훈련 데이터 셋이 많을 수록 유리할 것으로 판단



#### Case-04. 제목, 본문 (한글, 숫자, 띄어쓰기 처리 X, 별도의 명사 처리 O)

- 형태소 분석기 : **soynlp**
    - 비지도 학습 접근법을 지향하는 형태소 분석기
    - 여러 개의 문서로부터 학습한 통계 정보를 이용하여 작동
    - 패턴을 이용하여 단어를 추출하기 때문에 어느 정도 규모가 있는 동일 집단 문서에서 잘 작동
- content는 답변 위주의 데이터라 1차적으로 제목, 본문 내용으로만 처리
- soynlp 설치
    - [soynlp Github Guide](https://github.com/lovit/soynlp) <= 매우 상세
    - pip install soynlp

```python
# 한글, 숫자 데이터만 남겨둠
df['ko_num_title_content'] = df['title_content'].apply(lambda x: re.sub('[^0-9가-힣\s]','',x))

# ko_num_title_content 컬럼의 값들을 list로 만듬
ko_num_title_content_list = list(df['ko_num_title_content'].values)

from soynlp.noun import LRNounExtractor_v2
from soynlp.word import WordExtractor
from soynlp.tokenizer import LTokenizer

# 명사만 추출
ne = LRNounExtractor_v2(verbose=True)
ko_num_title_content_nouns_list = ne.train_extract(ko_num_title_content_list)

# 워드 추출
we = WordExtractor(min_frequency=100,
                    min_cohesion_forward=0.05,
                    min_right_branching_entropy=0.0
)

we.train(ko_num_title_content_nouns_list)
words = we.extract()

# https://sanghyu.tistory.com/169 참고
noun_score = {word:score.score for noun, score in nouns.items()}
cohesion_score = {word:score.cohesion_forward for word, score in words.items()}

combine_score = {noun:score + cohesion_score.get(noun, 0)
                    for noun, score in noun_score.items()
                }

combine_score.update(
    {subword:cohesion for subword, cohesion in cohesion_score.items()
        if not (subword in combined_score)
    }
)

tokenizer = LTokenizer(scores=combine_score)

df['noun_token'] = df['ko_num_title_content'].apply(lambda x: tokenizer.tokenize(x, remove_r=True))

soy_noun_token = []
for i in df['noun_token'].values:
    for k in i:
        soy_noun_token.append(k)
        
# 불용어 => 명사 구분이 잘 됐나 보려고 똑같은 불용어 사용
stop_words='뉴비 질문 더 제가 좀 부탁드립니다 하나 싶어서 왜 뭔가 전부 꼭 시작한지 \
            되나요 되는 너무 하면 해야 같아서 도와주세요 안녕하세요 잘 지금 그냥 \
            하는 관련 될까요 근데 이번에 정말 있고 중에 같이 모르고 및 다시 아니면 \
            다른 어떤 된 감사하겠습니다 좋을지 하루 하려고 맞추고 했는데 \
            같은데 알려주세요 원래 궁금합니다 뭐가 그리고 바로 보니까 있을까요 \
            또 오늘 나머지 하나요 일단 이제 해서 있는데 써서 첫 있어서 있나요 아직 \
            어떻게 혹시 계속 이미 따로 쓰고 어제 보니까 이것저것 우선 모르겠네요 \
            없이 어떤게 알려주시면 모르겠습니다 매일 저는 보고 있는지 맞는지 계정 \
            있습니다 빨리 어떤게 있다고 싶은데 부탁드려요 대충 적용해서 여기서 \
            맞나요 갈 완전 있으면 입니다 없어서 하면서 추천좀 좋은 할 하고 많이 \
            이렇게 걍 그래도 좋나요 1 33333 3333 3 몇가지 가도 해야하는지'

# 불용어 적용
soy_noun_token = [word for word in soy_noun_token if not word in stop_words]        

# Counter 라이브러리로 단어의 빈도수 체크 후 많은 순서대로 내림차순 정렬
from collections import Counter
count = Counter(soy_noun_token)
words_dict = dict(count)
words_dict = sorted(words_dict.items(), key=lambda item: item[1], reverse=True)

# 정렬 후 list로 반환되어 다시 dict로 변환
words_dict = dict(count)

from wordcloud import WordCloud
# 폰트를 프로젝트 폴더에 그냥 복사해서 바로 불러왔습니다.
wordcloud = WordCloud(font_path='NanumBarunGothic.ttf', 
                      min_font_size=7, max_font_size=150,
                      margin=3, width=500, height=500,
                      background_color='white').generate_from_frequencies(words_dict)

# WordCloud 출력
plt.figure(figsize=(10,10))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()
```

- 결과 WorldCloud

<p align="center"><img style="width:70%" src='https://user-images.githubusercontent.com/97505799/155882798-9c876ce7-b603-4816-99d6-062738285939.png'></p>

- Case-04. 결론
  - Case-03과 별 차이가 없음
  - 명사를 별도로 처리해줬는데 잘못한 건지 구분이 거의 되지 않음



















