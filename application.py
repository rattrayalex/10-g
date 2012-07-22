from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
  statements = [
    {'name':'Balance Sheet', 'slug':'balance_sheet', 'fields':[
      'Total Assets', 
      'Total Liabilities',
      'Total Shareholder\'s Equity',
    ]}, 
    {'name':'Statement of Cash Flows', 'slug':'cash_flows', 'fields':[
      'Net Income',
      'Net Cash from Operations',
      'Net Cash from Financing',
      'Net Cash used in Investing',
      'Net change in Cash',
    ]},
    {'name':'Income Statement', 'slug':'income_statement', 'fields':[
      'Total Revenue',
      'Net Income',
      'SG&A',
      'Research and Development',
      'Cost of Revenue',
      'Total Operating Expenses',
      'Earnings Per Share (Diluted)',
      'Earnings Per Share (Basic)',
    ]},
  ]
  return render_template('index.html', statements=statements)

if __name__ == '__main__':
  app.debug = True
  app.run()