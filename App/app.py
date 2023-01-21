from flask import Flask
from views import views

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")


@app.after_request
def add_header(response):
    response.cache_control.public = True
    response.cache_control.max_age = 1
    return response

if __name__ == '__main__':
    app.run(debug=True, port=8000, host="127.0.0.1")
