import sys
import re
import psycopg2
from pymongo import Connection
from collections import defaultdict

"""
The mongo database now contains the following data
(for any company we could find a suitable mapping for):
AccountsReceivable
Assets
AssetsCurrent
CapEx
CashAtCarryingValue
COGS
CommonStockValue
CostOfGoodsSold
Debt
Depreciation #
DepreciationAndAmortization
EarningsPerShare 
GrossProfit
IncomeTaxes #
Inventories
Inventory #
Liabilities
NetCashFromFinancing
NetIncome
OperatingExpenses
OperatingIncome
PPE
Profit #
RetainedEarnings
Revenues
SGnA
StockholdersEquity
"""


connection = Connection('data.10-g.com', 27017)


def get_companies_dict(infile="cik_ticker.txt"):
    companies = {}
    for line in open(infile):
        try:
            cik, ticker, name = [token.strip() for token in line.split('|')]
        except:
            continue
        if re.search("[0-9]+", ticker):
            #throw this out (usually cik######)
            continue
        #remove trailing /blah blah/ or other symbols from name
        name_groups = re.search("([A-Za-z0-9.,\-' &]+)", name)
        name = name_groups.group(0)
        name = name.title()
        if name[-1] == '.':
            name = name [:-1]
        #name = re.sub("/.*/", "", name)
        cik = cik.strip()
        ticker = ticker.strip()
        name = name.strip()
        companies[ticker] = {
            'name': name,
            'cik': cik }
    return companies

if __name__ == "__main__":
    #for testing
    companies = get_companies_dict(sys.argv[1])
    for ticker, company in companies.items():
        print company['cik'], ticker, company['name']

ALL_INFO = [ "CashAtCarryingValue",
"AccountsReceivable", "Inventories",
"PPE", "AssetsCurrent", "AssetsLongTerm",
"Assets", "Debt", "Liabilities",
"RetainedEarnings", "StockholdersEquity",
"Revenues", "COGS", "SGnA", "OperatingExpenses",
"OperatingIncome", "GrossProfit", "NetIncome",
"EPS", "CapEx", "DepreciationAndAmortization",
"CommonStockValue", "SIC" ]


def get_listings(ciks, company_info = ALL_INFO):
    db = connection.sec_data2
    companies = db.companies
    output = []
    for cik in ciks:
        company = companies.find_one({'cik' : cik})
        temp_dic = defaultdict(dict)
        if not company:
            continue
        for key, values in company['values'].items():
            for value in values:
                if len(value['period']) == 2 and value['period'][1] == 'Q':
	            temp_dic[str(value['year']) + value['period'][::-1]][key] = value
        for time, info in temp_dic.items():
            # print info
            line = [company['name'], time]
            for values in company_info:
                if values in info:
                    line.append(info[values]['value'])
                else:
                    line.append(0)
            output.append(line)
    return output

def clean(query_results):
    answer = []
    for result in query_results:
        out_res = dict(zip(result_keys, result))
        out_res['effective_value'] = float(out_res['effective_value'])
        answer.append(out_res)
    return answer
