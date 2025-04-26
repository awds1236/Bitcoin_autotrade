# Bitcoin_autotrade

### 1.autotrade.py, instruction.md
- 데이터: 일(30일), 시간(24시간) OHLCV, Moving Averages, RSI, Stochastic Oscillator, MACD, Bollinger Bands, Orderbook Data
- 전략: 1시간에 한번 판단하여 전량 매수/매도 or 홀드

### 2.autotrade_v2.py, instruction_v2.md
- 데이터: 일(30일), 시간(24시간) OHLCV, Moving Averages, RSI, Stochastic Oscillator, MACD, Bollinger Bands, Orderbook Data, 최신 뉴스 데이터(SerpApi), 공포/탐욕 지수
- 전략:  8시간에 한번 판단하여 부분 매수/매도 or 홀드, 투자 데이터 기록하고 AI 재귀 개선
- 뉴스 데이터 조회를 위한 [SerpApi](https://serpapi.com/) 가입 및 API KEY 등록 필요

### 3.autotrade_v3.py, instruction_v3.md
- 데이터: 일(30일), 시간(24시간) OHLCV, Moving Averages, RSI, Stochastic Oscillator, MACD, Bollinger Bands, Orderbook Data, 최신 뉴스 데이터(SerpApi), 공포/탐욕 지수, 차트 이미지(Selenium, GPT-4o 활용)
- 전략:  8시간에 한번 판단하여 부분 매수/매도 or 홀드, 투자 데이터 기록하고 AI 재귀 개선
- 뉴스 데이터 조회를 위한 [SerpApi](https://serpapi.com/) 가입 및 API KEY 등록 필요

## .env 파일 생성 및 설정
```
OPENAI_API_KEY="YourKey"
UPBIT_ACCESS_KEY="YourKey"
UPBIT_SECRET_KEY="YourKey"
SERPAPI_API_KEY="YourKey"
```

## 로컬 환경 설정
```
pip install -r requirements.txt
```

## AWS EC2 Ubuntu 서버 설정 방법
### 업비트 API 허용 IP 설정
[업비트 API 홈페이지](https://upbit.com/mypage/open_api_management)

### 기본 세팅
- 한국 기준으로 서버 시간 설정
```
sudo ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
```
- 패키지 목록 업데이트
```
sudo apt update
```
- 패키지 목록 업그레이드
```
sudo apt upgrade
```
- pip3 설치
```
sudo apt install python3-pip
```

### 실행하기
- 그냥 실행
```
python3 autotrade.py
```
- 백그라운드 실행
```
nohup python3 -u autotrade.py > output.log 2>&1 &
```
- 로그 보기
```
cat output.log
tail -f output.log
```
- 실행 확인
```
ps ax | grep .py
```
- 종료하기
```
kill -9 PID
ex. kill -9 13586
```
