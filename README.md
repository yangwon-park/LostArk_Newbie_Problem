# LostArk Newbie Problem

## 계획 이유

특정한 게임에 유저들의 로열티가 충분한 경우 그 유저들은 다른 게임을 하다가도 결국엔 귀소 본능처럼 다시 자신이 재밌어하고 즐겨하던 그 게임으로 돌아오는 것을 많이 목격했습니다. 이를 참고로 봤을 때 기존 유저들을 붙잡아 두는 것도 중요하지만, 게임의 가장 중요한 요소는 **신규 유저들의 리텐션**이라고 생각합니다.

<center><h5>(절대 기존 유저를 등한시 하는 것은 아닙니다!)</h5></center>

정말 많은 분들이 게임을 취미로 가지고 여가 시간을 보내는데, 생각보다 많은 유저분들이 뉴비일 때 진입 장벽을 크게 느껴 초기 콘테츠에서부터의 이탈률이 높습니다. 저 또한 많은 게임을 접해보았고 스스로 헤비한 게이머라고 생각하는 편입니다. 하지만 그런 저와 제  주변 지인들도 새로운 게임에 도전 할 때 막막함과 두려움이 느껴집니다.

---

<span style="font-size:120%">최근 '로스트아크'를 다시 시작하려는 유저의 입장에서 출시가 그렇게 오래되지 않았고 게임의 UI가 크게 불편하지 않았음에도 생각보다 쉽게 게임에 적응하지 못하는 제 모습이 보였습니다.</span>

---

이에 따라 뉴비들이 느끼는 문제점을 파악하고 분석하여 저와 제 지인들은 물론 정말 많은 게이머분들에게 도움이 되고 게임 기업의 입장에서 어떻게 하면 **유저 리텐션**을 높일 수 있을지 공부해보고자 이 프로젝트를 기획하게 됐습니다.

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
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('window-size=2560x1440')
options.add_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36')

# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome()
```

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

  

- 두 번째 메커니즘
  - '뉴비' 검색 => 게시글 번호 스크래핑 => 번호 별 url 접근 => 스크래핑 => 페이지 이동
  - 











