from flask import Flask, render_template
import gviz_api, json, api, datetime, pickle
app = Flask(__name__)


description = [
  ('entity_name','string','Entity Name'),
  ('fiscal_period', 'string','Period'),
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
  ('RetainedEarnings','number','RetainedEarnings'),
  ('StockholdersEquity','number','Total Equity'),

  # income statement
  ('Revenues','number','Total Revenue'),
  ('COGS','number','Cost of Revenue'),
  ('SGnA','number','SG&A'),
  ('OperatingExpenses','number','Operating Expense'),
  ('OperatingIncome','number','Operating Income'),
  ('Gross Profit','number','Gross Profit'),
  ('NetIncome','number','Net Income'),
  ('EPS','number','Earnings Per Share'),

  # statement of cash flows
  ('CapEx','number','Capital Expenditures'),
  # ('','number','Net Cash from Operations'),
  # ('NetCashFromFinancingNetIncome','number','Net Cash from Financing'),
  # ('','number','Net Cash used in Investing'),
  # ('','number','Net Change in Cash'),
  ('DepreciationAndAmortization','number','Depreciation & Amortization'),
  ('CommonStockValue','number','Common Stock Value'),
  
  ('SIC','string','SIC'),
]

divisions = pickle.load(open('divisions.txt', 'rb'))

children_sics = {}
for division in divisions:
  division_id = division['id']
  division_children = []
  for major_group in division['major_groups']:
    mg_id = major_group['id']
    division_children.append(mg_id)
    mg_children = []
    for industry_group in major_group['industry_groups']:
      ig_id = industry_group['id']
      mg_children.append(ig_id)
      ig_children = []
      for industry in industry_group['industries']:
        ind_id = industry['id']
        ig_children.append(ind_id)
      children_sics[ig_id] = ig_children
    children_sics[mg_id] = mg_children
  children_sics[division_id] = division_children


@app.route('/')
def index():
  statements = [
    {'name':'Balance Sheet', 'slug':'balance_sheet', 'fields':[
      ('CashAtCarryingValue','number','Total Cash'),
      ('AccountsReceivable','number','Accounts Receivable'),
      ('Inventories','number','Inventories'),
      ('PPE','number','PP&E'),
      ('AssetsCurrent','number','Current Assets'),
      ('AssetsLongTerm','number','Long Term Assets'), # WE NEED TO CALCULATE THIS
      ('Assets','number','Total Assets'),
      ('Debt','number','Debt'),
      ('Liabilities','number','Total Liabilities'),
      ('RetainedEarnings','number','RetainedEarnings'),
      ('StockholdersEquity','number','Total Equity'),
    ]}, 
    {'name':'Income Statement', 'slug':'income_statement', 'fields':[
      ('Revenues','number','Total Revenue'),
      ('COGS','number','Cost of Revenue'),
      ('SGnA','number','SG&A'),
      ('OperatingExpenses','number','Operating Expense'),
      ('OperatingIncome','number','Operating Income'),
      ('Gross Profit','number','Gross Profit'),
      ('NetIncome','number','Net Income'),
      ('EPS','number','Earnings Per Share'),
    ]},
    {'name':'Statement of Cash Flows', 'slug':'cash_flows','fields':[
      ('CapEx','number','Capital Expenditures'),
      # ('','number','Net Cash from Operations'),
      # ('NetCashFromFinancingNetIncome','number','Net Cash from Financing'),
      # ('','number','Net Cash used in Investing'),
      # ('','number','Net Change in Cash'),
      ('DepreciationAndAmortization','number','Depreciation & Amortization'),
      ('CommonStockValue','number','Common Stock Value'),
    ]},
  ]
  return render_template('index.html', statements=statements, divisions=divisions)

@app.route('/api/ciks/<ciks>/<x>/<y>/<color>/<size>/')
def api_ciks_four(ciks, x, y, color, size):
  ciks = ciks.split(',')
  return get_company_shit(ciks, x, y, color, size)

def get_company_shit(ciks, x, y, color, size):
  params = [x, y, color, size]
  long_params = [description[0][0],description[1][0]]
  long_params += params
  # long_params.append(description[-1][0])
  print long_params
  short_description = []
  for p in long_params:
    for d in description:
      if d[0] == p:
        short_description.append(d)
  print short_description
  columns_order = tuple(i[0] for i in short_description)
  order_by = columns_order[0]
  listings = api.get_listings(ciks, params)
  print listings
  data_table = gviz_api.DataTable(short_description)
  data_table.LoadData(listings)
  jsonstuff = data_table.ToJSon(columns_order=columns_order, order_by=order_by)
  return jsonstuff

@app.route('/api/companies/<sic>/<x>/<y>/<color>/<size>/')
def api_companies_sic_four(sic, x, y, color, size):
  ciks = api.get_ciks_for_group(sic)
  return get_company_shit(ciks, x, y, color, size)

@app.route('/api/children/<sic>/<x>/<y>/<color>/<size>/')
def api_children_sic_four(sic, x, y, color, size):
  # length = len(sic)
  sics = children_sics[sic]
  params = [x, y, color, size]
  long_params = [description[0][0],description[1][0]]
  long_params += params
  # long_params.append(description[-1][0])
  print long_params
  short_description = []
  for p in long_params:
    for d in description:
      if d[0] == p:
        short_description.append(d)
  print short_description
  columns_order = tuple(i[0] for i in short_description)
  order_by = columns_order[0]
  listings = [api.get_agg_stats_for_group(s, params) for s in sics]
  print listings
  data_table = gviz_api.DataTable(short_description)
  data_table.LoadData(listings)
  jsonstuff = data_table.ToJSon(columns_order=columns_order, order_by=order_by)
  return jsonstuff

@app.route('/api/example/')
def api_example():
  columns_order = tuple(i[0] for i in description)
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
  listings = api.get_listings(ciks)
  print listings
  # print json.dumps(listings[0])
  # # {"effective_value": 18235000000.0, "entity_name": "Google Inc.", "calendar_period": "Y", "fiscal_year": 2010, "ticker": "goog", "field_name": "CommonStockIncludingAdditionalPaidInCapital"}
  # google_friendly_data = []
  # for item in listings:
  #   if item['calendar_period'] == 'Y':
  #     this_date = item['fiscal_year']
  #     ev = item['effective_value']
  #     print this_date
  #     thing = [item['entity_name'], this_date, ev, ev, ev]
  #     google_friendly_data.append(thing)
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
  data_table.LoadData(listings)
  jsonstuff = data_table.ToJSon(columns_order=columns_order, order_by=order_by)
  return jsonstuff


if __name__ == '__main__':
  app.debug = True
  app.run()
