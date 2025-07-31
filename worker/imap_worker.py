import os
import redis
from rq import Queue, Worker, Connection
from utils.imap_utils import check_account
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
REDIS_URL = os.getenv("REDIS_URL")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
redis_conn = redis.from_url(REDIS_URL)
queue = Queue(connection=redis_conn)

# Background job function
def process_email_check(account, query):
    return check_account(account, query)

if __name__ == "__main__":
    with Connection(redis_conn):
        worker = Worker([queue])
        worker.work()
