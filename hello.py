from flask import Flask, url_for, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello World!'

@app.route('/name/<name>/')
def name(name):
  img = url_for('static', filename="screenshot.png")
  return '<html><body><img src="%s"></body></html>' % img

if __name__ == '__main__':
  app.debug = True
  app.run()