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
      'Current Assets'
      'Long Term Assets', # total - current
      'Total Assets', 
      'Debt',
      'Long-Term Liabilities',
      'Total Liabilities',
      'Retained Earnings',
      'Total Equity',
    ]}, 
    {'name':'Income Statement', 'slug':'income_statement', 'offset':13, 'fields':[
      'Total Revenue',
      'Cost of Revenue',
      'SG&A', 
      'Operating Expense', 
      'Operating Income',
      'Gross Profit',
      'Net Income',
      'Earnings per Share',
    ]},
    {'name':'Statement of Cash Flows', 'slug':'cash_flows', 'offset':19, 'fields':[
      'Capital Expenditures',
      # 'Net Cash from Operations',
      # 'Net Cash from Financing',
      # 'Net Cash used in Investing',
      # 'Net Change in Cash',
      'Depreciation & Amortization',
      'Common Stock Value',
    ]},
  ]
  divisions = [ 
    {'name':'Agriculture, Forestry, And Fishing', 'id':'A', 'start':'01', 'end':'09', 'major_groups': [
      {'name':'Agricultural Production Crops', 'id':'01', 'industry_groups': [
        {'name':'Wheat', 'id':'0111'},
        ]
      },
      ]
    },
  ]
  return render_template('index.html', statements=statements, divisions=divisions)

@app.route('/api/example/')
def api_example():
  description = [
    ('entity_name','string','Entity Name'),
    ('fiscal_period', 'number','Period'),
    # balance sheet
    ('CashAtCarryingValue','number','Total Cash'),
    ('AccountsReceivable','number','Accounts Receivable'),
    ('Inventories','number','Inventories'),
    ('PPE','number','PP&E'),
    ('AssetsCurrent','number','Current Assets'),
    ('AssetsLongTerm','number','Long Term Assets'), # WE NEED TO CALCULATE THIS
    ('Assets','number','Total Assets'),
    ('Debt','number','Debt'),
    ('Liabilities','number','Total Liabilities'),
    ('RetainedEarnings','number','RetainedEarnings')
    ('StockholdersEquity','number','Total Equity'),

    # income statement
    ('Revenues','number','Total Revenue'),
    ('COGS','number','Cost of Revenue'),
    ('SGnA','number','SG&A'),
    ('OperatingExpenses','number','Operating Expense'),
    ('OperatingIncome','number','Operating Income'),
    ('Gross Profit','number','Gross Profit')
    ('NetIncome','number','Net Income'),
    ('EPS','number','Earnings Per Share'),

    # statement of cash flows
    ('CapEx','number','Capital Expenditures')
    # ('','number','Net Cash from Operations'),
    # ('NetCashFromFinancingNetIncome','number','Net Cash from Financing'),
    # ('','number','Net Cash used in Investing'),
    # ('','number','Net Change in Cash'),
    ('DepreciationAndAmortization','number','Depreciation & Amortization'),
    ('CommonStockValue','number','Common Stock Value'),
    
    ('SIC','string','SIC'),

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
'''
  TO JOSH: 
   google_friendly_data should take the form:
  [
  [str('entity_name'), str('fiscal_period'), float('CashAtCarryingValue'), etc... str('SIC')]
  eg:
  ['Google', '2012Q1', 234234324.35, 234234,67,5456,546, etc ... '5464'] 
  ]
'''
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(google_friendly_data)
  jsonstuff = data_table.ToJSon(columns_order=columns_order, order_by=order_by)
  return jsonstuff


if __name__ == '__main__':
  app.debug = True
  app.run()