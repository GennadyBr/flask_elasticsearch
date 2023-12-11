import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# @app.route('/')
@app.route('/search')
def search_autocomplete():
    return "HIHIHIHIHIHIHIHIHI"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('FLASK_PORT'), debug=True)
