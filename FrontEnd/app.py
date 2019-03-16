from flask import Flask, render_template

app = Flask(__name__)


@app.template_filter("call")
def call():
    print("Call" )


@app.route("/")
def hello_world():
    return render_template("Frontend.html")

