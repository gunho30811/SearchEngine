from flask import Flask, request, render_template, jsonify
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

# ✅ .env 설정 로드
load_dotenv()

# ✅ Elasticsearch 연결
es = Elasticsearch("http://localhost:9200")

# ✅ SentenceTransformer 모델 로딩
model = SentenceTransformer("jhgan/ko-sbert-sts")

# ✅ Flask 앱 초기화
app = Flask(__name__, static_folder="templates", static_url_path="")

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.json.get("query")
    if not query:
        return jsonify({"error": "검색어가 비어 있습니다"}), 400

    try:
        vector = model.encode(query).tolist()

        body = {
            "size": 5,
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                        "params": {
                            "query_vector": vector
                        }
                    }
                }
            }
        }

        res = es.search(index="kostat_vector_index", body=body)

        hits = [
            {
                "title": doc["_source"].get("title"),
                "content": doc["_source"].get("content"),
                "score": doc["_score"]
            }
            for doc in res["hits"]["hits"]
        ]
        return jsonify(hits)

    except Exception as e:
        return jsonify({"error": f"검색 실패: {str(e)}"}), 500
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
