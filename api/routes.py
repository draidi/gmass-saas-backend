from flask import Blueprint, request, jsonify
from supabase import create_client
from redis import Redis
from rq import Queue
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
REDIS_URL = os.getenv("REDIS_URL")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
redis_conn = Redis.from_url(REDIS_URL)
queue = Queue(connection=redis_conn)

api_bp = Blueprint("api", __name__)

@api_bp.route('/api/check', methods=["GET"])
def check_subject():
    query = request.args.get("query", "")
    response = supabase.table("boites").select("*").execute()
    return jsonify(response.data)
