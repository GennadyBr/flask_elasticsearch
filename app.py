from flask import Flask

app = Flask(__name__)

@app.route('/search')
def search_autocomplete():
    return ""

if __name__ == '__main__':
    app.run(debug=True)
