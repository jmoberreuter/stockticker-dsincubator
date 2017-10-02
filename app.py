from flask import Flask, render_template, request, redirect
import simplejson as json
from bokeh.plotting import figure, output_file, save
import pandas as pd
import requests

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/stockticker', methods = ['get', 'post'])
def plotstockprices():
    stockname = 'FB'
    output_file("templates/stockticker.html")
    p = figure(title="stock price: "+stockname, x_axis_label='time', y_axis_label='USD', x_axis_type = 'datetime')
    date = list(pd.to_datetime(getstockprices(stockname)['Date']))
    price = list(getstockprices(stockname)['Close'])
    p.line(date, price, legend = stockname, line_width = 2)
    save(p)
    return render_template('stockticker.html')

def getstockprices(tickerinput):
    url = 'https://www.quandl.com/api/v3/datasets/WIKI/'+tickerinput+'/data.json?api_key=GNKyX_ZEQBue_DPmsymt'
    jsondata = requests.get(url)
    stockdf = pd.DataFrame(jsondata.json()['dataset_data']['data'], columns=jsondata.json()['dataset_data']['column_names'])
    return stockdf


if __name__ == '__main__':
  app.run(port=33507)
