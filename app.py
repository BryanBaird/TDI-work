from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import jinja2
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components

stem = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES'
filetype_csv = '.csv?'
t_query = 'ticker='
sd_query = 'date.gte='

a_query = 'api_key='
api_key = 'uMSAPoLS_hMKaPdsa9y2'

app = Flask(__name__)

app.vars = {}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index2():
    # request was a POST
    app.vars['ticker'] = request.form['ticker']
    app.vars['startdate'] = request.form['startdate']

    return redirect('/graph')

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    csv_query = stem + filetype_csv + t_query + app.vars['ticker'] + '&' + sd_query + app.vars['startdate'] + '&' + a_query + api_key
    print('API call: %s' % csv_query)
    df = pd.read_csv(csv_query, index_col='date', parse_dates=True)
    
    print(df.head())
    plot = figure(tools="pan,wheel_zoom,box_zoom,reset", title='%s Opening Stock Price' %(app.vars['ticker']), x_axis_label='date', x_axis_type='datetime')

    # add a line renderer
    plot.line(df.index, df['open'], line_width=2)
    
    script, div = components(plot)
    
    return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
  app.run(port=33507, debug=True)
