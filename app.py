from flask import Flask, render_template, request, redirect
import requests
import pandas as pd

stem = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES'
filetype_csv = '.csv?'
t_query = 'ticker='
ticker = 'GOOG' #returns Google stock prices by default

a_query = 'api_key='
api_key = 'uMSAPoLS_hMKaPdsa9y2'

app = Flask(__name__)

app.vars = {}

@app.route('/', methods=['GET'])
def index():
    small_csv_query = stem + filetype_csv + t_query + ticker + '&' + a_query + api_key
    df_full_csv = pd.read_csv(small_csv_query, index_col='date', parse_dates=True)
    print(df_full_csv.head())
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index2():
    # request was a POST
    app.vars['ticker'] = request.form['ticker']
    app.vars['options'] = request.form['options']

    f = open('%s_%s.txt'%(app.vars['ticker'],app.vars['options']),'w')
    f.write('Ticker: %s\n'%(app.vars['ticker']))
    f.write('Options: %s\n\n'%(app.vars['options']))
    f.close()

    return redirect('/graph')

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    small_csv_query = stem + filetype_csv + t_query + app.vars['ticker'] + '&' + a_query + api_key
    df_full_csv = pd.read_csv(small_csv_query, index_col='date', parse_dates=True)
    
    
    return render_template('graph.html')

if __name__ == '__main__':
  app.run(port=33507, debug=True)
