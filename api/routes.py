from flask import Blueprint, request, jsonify
from supabase import create_client
import os
import redis
from rq import Queue
from dotenv import load_dotenv

from utils.imap_utils import check_account

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
REDIS_URL = os.getenv("REDIS_URL")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
redis_conn = redis.from_url(REDIS_URL)
queue = Queue(connection=redis_conn)

bp = Blueprint("api", __name__)

@bp.route("/api/check", methods=["GET"])
def check_subject():
    query = request.args.get("query", "")
    response = supabase.table("boites").select("*").execute()
    results = []

    for item in response.data:
        job = queue.enqueue("worker.imap_worker.process_email_check", item, query)
        results.append({"email": item["email"], "status": "queued"})

    return jsonify(results)
