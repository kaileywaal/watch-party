#!/usr/bin/env python3

from flask import Flask, request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def main():
    return '''
    <h1>Hey, there!</h1>
    <p>What is your name?</p>
     <form action="/echo_user_input" method="POST">
         <input name="user_input">
         <input type="submit" value="Submit!">
     </form>
     '''

@app.route("/echo_user_input", methods=["POST"])
def echo_input():

    name_input_text = request.form.get("user_input", "")
    return render_template('hello_world.html', name=name_input_text)
# "You entered: " + name_input_text