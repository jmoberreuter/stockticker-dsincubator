from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure, output_file, save
import pandas as pd
import requests
import os

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/stockticker', methods = ['get', 'post'])
def plotstockprices():
    #get the stock name and put the data into a dataframe
    stockname = request.form['ticker']
    url = 'https://www.quandl.com/api/v3/datasets/WIKI/'+stockname+'/data.json?api_key=GNKyX_ZEQBue_DPmsymt'
    jsondata = requests.get(url)
    stockdf = pd.DataFrame(jsondata.json()['dataset_data']['data'], columns=jsondata.json()['dataset_data']['column_names'])
    #set up the figure
    output_file("templates/stockticker.html")
    p = figure(title="stock price: "+stockname, x_axis_label='time', y_axis_label='USD', x_axis_type = 'datetime')
    date = list(pd.to_datetime(stockdf[(stockdf.Date >= request.form['from']) & (stockdf.Date <= request.form['to'])].Date))
    colors = ['blue','red','green','brown']
    for feat in request.form.getlist('features[]'):
        price = list(stockdf[(stockdf.Date >= request.form['from']) & (stockdf.Date <= request.form['to'])][feat.encode('utf-8')])
        p.line(date, price, legend = stockname+': '+feat, line_width = 0.5, color = colors.pop(0))
    save(p)
    return render_template('stockticker.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
