from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__,template_folder='templates')

@app.route('/')
def index():
    pass

if __name__ == '__main__':
    app.run(debug=True) 