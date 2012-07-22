from flask import Flask, render_template
import gviz_api, json, api, datetime
app = Flask(__name__)

@app.route('/')
def index():
  statements = [
    {'name':'Balance Sheet', 'slug':'balance_sheet', 'offset':2, 'fields':[
      'Total Cash',
      'Accounts Receivable',
      'Inventories',
      'PP&E',
      'Long Term Assets', # total - current
      'Total Assets', 
      'Current Liabilities',
      'Long-Term Liabilities',
      'Total Liabilities',
      'Total Equity',
    ]}, 
    {'name':'Income Statement', 'slug':'income_statement', 'offset':12, 'fields':[
      'Total Revenue',
      'Cost of Revenue',
      'SG&A', # calc: oi - rev + cogs
      # 'Research and Development',
      'Operating Expense', # calc: cogs + sga
      'Operating Income',
      'Net Income',
    ]},
    {'name':'Statement of Cash Flows', 'slug':'cash_flows', 'offset':18, 'fields':[
      'Net Cash from Operations',
      'Net Cash from Financing',
      'Net Cash used in Investing',
      'Net Change in Cash',
      'Depreciation & Amortization',
    ]},
  ]
  return render_template('index.html', statements=statements)

@app.route('/api/example/')
def api_example():
  description = [
    ('entity_name','string','Entity Name'),
    ('fiscal_year', 'number','Fiscal Year'),
    ('effective_value','number','Effective Value'),
    ('effective_value_2','number','Effective Value 2'),
    ('effective_value_3','number','Effective Value 3'),
    ]
  columns_order = (
    'entity_name',
    'fiscal_year',
    'effective_value',
    'effective_value_2',
    'effective_value_3',
    )
  order_by = columns_order[0]
  # infile = 'cik_ticker.txt'
  # companies = api.get_companies_dict(infile)
  # ciks = [c['cik'] for t, c in companies.items()]
  # print ciks
  # for ticker, company in companies.items():
  #     print company['cik'], ticker, company['name']
  ciks = ['0000789019', #msft
    '0000320193', #appl
    '0001288776', #goog
  ]
  listings = api.get_listings({'entity_codes' : ciks, "field_name": '%Revenue'})
  print listings[0]
  print json.dumps(listings[0])
  # {"effective_value": 18235000000.0, "entity_name": "Google Inc.", "calendar_period": "Y", "fiscal_year": 2010, "ticker": "goog", "field_name": "CommonStockIncludingAdditionalPaidInCapital"}
  google_friendly_data = []
  for item in listings:
    if item['calendar_period'] == 'Y':
      this_date = item['fiscal_year']
      ev = item['effective_value']
      print this_date
      thing = [item['entity_name'], this_date, ev, ev, ev]
      google_friendly_data.append(thing)
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(google_friendly_data)
  jsonstuff = data_table.ToJSon(columns_order=columns_order, order_by=order_by)
  return jsonstuff

@app.route('/old/')
def old_index():
  # size = assets, color = NI/Revenue, x = revenue, y = cogs/Revenue
  statements = [
    {'name':'Balance Sheet', 'slug':'balance_sheet', 'fields':[
      'Total Cash',
      'Accounts Receivable',
      'Inventories',
      'PP&E',
      'Long Term Assets', # total - current
      'Total Assets', 
      'Current Liabilities',
      'Long-Term Liabilities',
      'Total Liabilities',
      'Total Equity',
    ]}, 
    {'name':'Income Statement', 'slug':'income_statement', 'fields':[
      'Total Revenue',
      'Cost of Revenue',
      'SG&A', # calc: oi - rev + cogs
      # 'Research and Development',
      'Operating Expense', # calc: cogs + sga
      'Operating Income',
      'Net Income',
    ]},
    {'name':'Statement of Cash Flows', 'slug':'cash_flows', 'fields':[
      'Net Cash from Operations',
      'Net Cash from Financing',
      'Net Cash used in Investing',
      'Net Change in Cash',
      'Depreciation & Amortization',
    ]},
  ]
  return render_template('old_index.html', statements=statements)

if __name__ == '__main__':
  app.debug = True
  app.run()