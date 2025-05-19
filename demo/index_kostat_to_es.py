import pymysql
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
from tqdm import tqdm

# 1. 설정 불러오기 (.env)
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# 2. DB 연결 테스트
try:
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        charset="utf8mb4"
    )
    cursor = conn.cursor()
    print("✅ DB 연결 성공")
except Exception as e:
    print("❌ DB 연결 실패:", e)
    exit(1)

# 3. Elasticsearch 연결 확인
try:
    es = Elasticsearch("http://localhost:9200")
    if es.ping():
        print("Elasticsearch 연결 성공")
    else:
        print("Elasticsearch 연결 실패")
        exit(1)
except Exception as e:
    print("Elasticsearch 예외(실패패):", e)
    exit(1)

# 4. 모델 로드
try:
    model = SentenceTransformer("jhgan/ko-sbert-sts")
    print("✅ 임베딩 모델 로딩 완료")
except Exception as e:
    print("❌ 모델 로딩 실패:", e)
    exit(1)

# 5. 인덱스 생성 (없으면)
index_name = "kostat_vector_index"
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body={
        "mappings": {
            "properties": {
                "id": {"type": "integer"},
                "title": {"type": "text"},
                "content": {"type": "text"},
                "source": {"type": "keyword"},
                "created_at": {"type": "keyword"},
                "embedding": {
                    "type": "dense_vector",
                    "dims": 768,
                    "index": True,
                    "similarity": "cosine"
                }
            }
        }
    })
    print(f"✅ 인덱스 '{index_name}' 생성 완료")
else:
    print(f"ℹ️ 인덱스 '{index_name}' 이미 존재")

# 6. 데이터 조회
cursor.execute("SELECT id, title, content, source, created_at FROM kostatSample LIMIT 100")
rows = cursor.fetchall()
print(f"ℹ️ {len(rows)}개 데이터 가져옴")

# 7. 벡터 임베딩 + 인덱싱
for row in tqdm(rows, desc="인덱싱 진행 중중"):
    id, title, content, source, created_at = row
    combined = f"{title} {content or ''}"
    try:
        embedding = model.encode(combined).tolist()
        doc = {
            "id": id,
            "title": title,
            "content": content,
            "source": source,
            "created_at": created_at,
            "embedding": embedding
        }
        es.index(index=index_name, id=id, body=doc)
    except Exception as e:
        print(f"인덱싱 실패 (id={id}):", e)

print("✅ 전체 인덱싱 완료")
conn.close()

#필요한 패키지 설치치
# pip install pymysql python-dotenv sentence-transformers elasticsearch tqdm 