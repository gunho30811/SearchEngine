🧪 Demo: 벡터 검색 연습 프로젝트

이 `demo` 폴더는 **벡터 검색(Vector Search)**을 간단히 실습해보기 위한 예제입니다.  
로컬 환경에서 데이터베이스를 구성하고, 벡터 기반 검색 결과를 테스트할 수 있습니다.

---

## 📁 Demo 폴더 구성

- `demo/`  
  벡터 검색을 실습하기 위한 전체 프로젝트 폴더입니다.

- `demo/db/`  
  DB 테이블 생성 및 데이터 삽입을 위한 **SQL 파일**이 포함되어 있습니다.

- `demo/install/`  
  elasticsearch-7.17.10-windows-x86_64 가 들어 있습니다.
  위 폴더는 ignore 되고 있음으로, install 폴더에 설치하면 됩니다.

- `demo/templates/`  
  간단한 UI/UX 파일이 있습니다. 

- `env.txt`
  개별적으로 설정해야 할 파일의 예시를 담아두었습니다. 위 파일을 개인화 이후 .env 파일로 변경해주시면 됩니다.

- `index.kostat_to_es.py`
  벡터 검색을 위한 인덱싱하는 파일 입니다.

- `env.txt`
  메인 서버로 5000 포트에 WAS인 플라스크 서버를 기동 중이고 , 검색 엔진은 9200번 포트에 기동 합니다.

## ⚙️ Demo 실행 방법

#### 🧪 1. 사전 요구 사항
- Python 3.8 이상
- MySQL (또는 호환 DB)
- Elasticsearch 7.17.10
- 인터넷 연결 (모델 다운로드 1회 필요)

### ✅ 2. Elasticsearch 설치

1. [Elasticsearch 7.17.10 다운로드](https://www.elastic.co/downloads/past-releases/elasticsearch-7-17-10)
2. 압축 해제 후 `demo/install/` 폴더에 저장 (폴더 이름은 `elasticsearch-7.17.10`)
3. `config/elasticsearch.yml` 맨 아래에 아래 설정 추가:

    ```yaml
    xpack.security.enabled: false
    discovery.type: single-node
    ```

4. 실행:

    ```bash
    cd demo/install/elasticsearch-7.17.10/bin
    elasticsearch.bat
    ```

5. 브라우저에서 `http://localhost:9200` 접속해 JSON 응답이 뜨면 성공

### ✅ 3. 데이터베이스 설정

1. `.env` 파일 생성 (`env.txt` 참고):

    ```env
    DB_HOST=localhost
    DB_PORT=3306
    DB_NAME=wisenut
    DB_USER=root
    DB_PASSWORD=패스워드
    ```

2. `demo/db/` 폴더에 있는 `.sql`로 테이블 생성 및 데이터 삽입  
   예: `kostatSample` 테이블


### ✅ 4. Python 패키지 설치
pip install pymysql python-dotenv sentence-transformers elasticsearch flask tqdm

### ✅ 5. 인덱싱 실행 (DB → 임베딩 → ES 저장)
python index_kostat_to_es.py

### ✅ 6. 검색 서버 실행 (Flask)
python app.py
브라우저에서 http://localhost:9200 접속 확인

실행 이미지
--
![image](https://github.com/user-attachments/assets/09771d6c-7d72-4b74-8560-36ef3da858ed)
--
![image](https://github.com/user-attachments/assets/ce9a006d-da86-439a-a19d-9e2b281a6d20)
--


### ✅ 7. 포트 정리
서비스	포트	설명
1. Flask WAS	5000	검색 웹서버
2. Elasticsearch	9200	벡터 검색 인덱스 저장 및 질의
3. MySQL	3306	원본 데이터 저장 (kostatSample 등)


## 💡 참고

- 벡터 검색 예제는 Embedding 모델 기반으로 작동하며,  
  연습용 환경에서는 간단한 형태의 문장 매칭을 통해 작동 방식을 이해할 수 있습니다.
- 정식 서비스 수준의 구현은 포함되어 있지 않으며, 학습 및 테스트 목적입니다.

---
## 📝 문의

해당 프로젝트에 대한 문의는 gunho30811@naver.com or 카톡 gunho30811 로 해주세요.
