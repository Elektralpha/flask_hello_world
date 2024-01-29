from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')


                                                                                                                                       
if __name__ == "__main__":
  app.run(debug=True)
