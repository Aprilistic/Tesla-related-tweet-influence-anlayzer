# Watt's Up with Tesla? A Twitter Sentiment Analysis

[https://github.com/Aprilistic/Watt-s-Up-with-Tesla-A-Twitter-Sentiment-Analysis](https://github.com/Aprilistic/Watt-s-Up-with-Tesla-A-Twitter-Sentiment-Analysis)

[BLACKBUN/tesla-related-unrelated-classification · Hugging Face](https://huggingface.co/BLACKBUN/tesla-related-unrelated-classification)

# Objective

본 프로젝트는 [Tesla.Inc](https://www.notion.so/Tesla-related-tweet-influence-analyzer-df420b14aa5042f081b9d477ded231aa?pvs=21) 와 관련된 자연어 텍스트를 구분하여 Tesla 주식에 맞춰진 감성 분석을 목적으로 만들어졌습니다. 일론 머스크(Tesla, Twitter CEO)의 트윗은 종종 주가에 영향을 미치는 것으로 유명합니다. 이에 착안하여 트윗과 같은 짧은 텍스트를 Tesla 와의 관련성 여부를 판단, 그리고 주식과 관련된 감성 분류 모델을 통해 주식에 미칠 수 있는 영향을 예측합니다.

# How to run?

Build environment:

OS: macOS Ventura 13.4.1

Python: 3.10.11

Flask, request, transformers, jsonify

(pip install flask, request, transformers, jsonify)

Run:

1. Clone repository and go to the clonned directory
2. Run this command: “python Flask_API/Flask_API.py”
    
    (This process might take some time at first, so please wait for a while)
    
3. Open “[http://127.0.0.1:5000](http://127.0.0.1:5000/)”
4. Enter text whatever you want. News, tweets … etc

# Methodology

### 데이터 수집

1. 테슬라 관련 뉴스 41000건
    1. Bing news search API 이용
        
        키워드: Tesla, 순서: 관련도 순, 기간: 05/21-06/20
        
2. 최신 BBC News 18000건
    1. Kaggle BBC News 데이터셋([링크](https://www.kaggle.com/datasets/gpreda/bbc-news))
    2. 테슬라 관련 기사는 삭제함

ChatGPT 등장 이후 주요 언론(Bloomberg, CNBC, TechCrunch 등), SNS(Twitter, Reddit) 크롤링이 어려워짐. 따라서 API 이용

### 데이터 전처리

1. Data Cleaning
    
    Dataframe 이용 필요 열(Title, Description) 추출 및 HTML 태그 등 불필요한 토큰 제거
    
2. Lowercase converting
    
    모든 입력은 소문자로 가정. 모든 문자 소문자 변환
    
3. Domain specific word processing
    
    ‘model 3’ → ‘model_3’, ‘model s’ → ‘model_s’ 와 같이 테슬라 관련 단어 토큰 ‘_’ 이용해 전처리
    
4. Dataset
    
    데이터 불균형 해소 및 라벨링
    
    | Label | Count |
    | --- | --- |
    | 0(Not related) | 18639 |
    | 1(Related) | 20000 |
    
    ```cpp
    {"label": 1, "text": "Tesla news description",
    "label": 0, "text": "Other news description", ...}
    ```
    
    Train : Test = 9 : 1 비율로 조정
    

### 모델

Huggingface API 이용

- 오픈소스로 공개 가능
- 추론 시 편리한 이용 가능
- 전이학습 용이

1. BLACKBUN/tesla-related-unrelated-classification([링크](https://huggingface.co/BLACKBUN/tesla-related-unrelated-classification))
    
    distilbert-base-uncased(67M) 파인튜닝
    
    - 토크나이저 커스터마이징
        - ‘tesla’, ‘model_3’ 등 도매인 특화 토큰 추가
    - 하이퍼파라미터 튜닝
    - Binary classification
    
    | model_type | distilbert |
    | --- | --- |
    | activation | gelu |
    | dropout | 0.1 |
    | vocab_size | 30531 |
    | max_position_embeddings | 512 |
    
2. zhayunduo/roberta-base-stocktwits-finetuned([링크](https://huggingface.co/zhayunduo/roberta-base-stocktwits-finetuned))
    
    데이터 수집 한계로 사전 학습 모델 이용
    

### 프로그램 개요

[![](https://mermaid.ink/img/pako:eNplkcuOwiAUhl_lhNVMoi_gYhK1VSdzibGdVeuCwLElUmgo2Gms7z60OBdHFoTz8fFzOxOmOZIZOUjdspIaC2mUK_Btnj2r2vkaP-0eptOnPkHFe1g8bA3WRjNsGhiVx7BgMUiQZCk2ksILdq02HJYlsuM-GMlo9O_awkq7IWx5DrZBiSeqGAb_cuMHNw5sOR5liNihpBZ9SJQNpQklWA1j5v6v_-PGWWI1O4K_ixWV72CuqOwa0Vz9OORjQa04YQ-r7I12UGjgulX_HGcNlT2sh_1LoYqb6a1uRIjYfEe4-mpE48V2cfLxmgayuiPrO7K5IYH9zpMJqdBUVHD_neeB5MSWWGFOZn7I8UCdtDnJ1cWr1FmddIqRmTUOJ8TV3D9QJGhhaBXg5QscA6oI?type=png)](https://mermaid.live/edit#pako:eNplkcuOwiAUhl_lhNVMoi_gYhK1VSdzibGdVeuCwLElUmgo2Gms7z60OBdHFoTz8fFzOxOmOZIZOUjdspIaC2mUK_Btnj2r2vkaP-0eptOnPkHFe1g8bA3WRjNsGhiVx7BgMUiQZCk2ksILdq02HJYlsuM-GMlo9O_awkq7IWx5DrZBiSeqGAb_cuMHNw5sOR5liNihpBZ9SJQNpQklWA1j5v6v_-PGWWI1O4K_ixWV72CuqOwa0Vz9OORjQa04YQ-r7I12UGjgulX_HGcNlT2sh_1LoYqb6a1uRIjYfEe4-mpE48V2cfLxmgayuiPrO7K5IYH9zpMJqdBUVHD_neeB5MSWWGFOZn7I8UCdtDnJ1cWr1FmddIqRmTUOJ8TV3D9QJGhhaBXg5QscA6oI)

프로그램은 로컬 Flask 서버로 실행됨.

사용자 입력으로 테슬라 관련 키워드 (”model_3”, “gigafactory”…) 포함 여부로 1차 관련성 확인

bert-finetuned 모델로 2차 확인

Related 일 경우 stock-sentiment 분석 모델 이용

# Findings

![wordcloud.png](wordcloud.png)

EDA 결과 테슬라와 관련된 단어들이 자주 등장함을 확인할 수 있었음

# Results

BLACKBUN/tesla-related-unrelated-classification

- Epochs: 2
- Accuracy: 0.9997

![일론머스크 트윗](examples.png)

일론머스크 트윗

# Limitations

distilbert-base-uncased([링크](https://huggingface.co/distilbert-base-uncased)) 전이학습 시 토크나이저에 테슬라 관련 term을 추가했지만 데이터 불충분(14MB)으로 새롭게 추가된 키워드(ex “model_3”, “supercharger”)는 등 유의미한 학습(단어 임베딩)이 되지 않았음. 

관련성 점수 계산을 위해 word2vec, tf-idf 모두 이용했으나 실 성능 낮았음

따라서 EDA를 통해 추출한 테슬라 관련 term이 존재할 경우 관련성 있음으로 판단하나, 맥락만을 통한 분류는 비교적 성능이 떨어지는 편

학습 데이터로 뉴스만을 이용했으므로 뉴스를 입력으로 넣었을 때보다 트윗으로 넣을 때 성능이 낮음

일론머스크의 실시간 트윗을 API로 연동하고 싶었으나, 최근 Twitter의 API 유료화 정책으로 불가능

데이터셋의 경우 2023년 5-6월의 데이터로 구성. 따라서 시간이 지남에 따라 성능 저하 발생 가능함.

# Conclusion

![Test.gif](Test.gif)

데이터 수집과 컴퓨팅 자원의 한계가 있었지만 특정 도매인에 맞춘 감성 분석 모델이 충분히 가능함을 확인했음. 처음 의도한 것보다는 목표가 많이 축소되었지만 재미있었다.

# References

BBC News Dataset: [https://www.kaggle.com/datasets/gpreda/bbc-news](https://www.kaggle.com/datasets/gpreda/bbc-news)

distilbert-base-uncased: [https://huggingface.co/distilbert-base-uncased](https://huggingface.co/distilbert-base-uncased)

zhayunduo/roberta-base-stocktwits-finetuned: [https://huggingface.co/zhayunduo/roberta-base-stocktwits-finetuned](https://huggingface.co/zhayunduo/roberta-base-stocktwits-finetuned)