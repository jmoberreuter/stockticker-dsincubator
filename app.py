from flask import Flask, render_template, request, redirect
import simplejson as json
from bokeh.plotting import figure, output_file, show
import pandas

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')
  
def getstockprices(tickerinput):
    jsondata = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/'+'tickerinput'+'/data.json?api_key=GNKyX_ZEQBue_DPmsymt')
    data = pandas.read_json(jsondata)
    print(data)



if __name__ == '__main__':
  app.run(port=33507)
