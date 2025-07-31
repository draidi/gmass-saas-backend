from flask import Flask
from api.routes import api_bp
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Create the Flask app
app = Flask(__name__)

# Register API routes
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def index():
    return {'status': '✅ GMass SaaS Backend is Running'}

# Start the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
