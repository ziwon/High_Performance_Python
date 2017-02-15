from flask import Flask,request
import time
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/add")
def add():
    name = request.args.get('name', '')
    delay = float(request.args.get('delay',''))
    print('name = %s delay = %s' % (name,delay))
    time.sleep(delay/1000.0)
    return('name = %s delay = %s' % (name,delay))

if __name__ == "__main__":
    app.run(port=8080, debug=True, threaded=True)
