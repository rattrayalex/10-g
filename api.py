import sys
import re
import psycopg2
from itertools import cycle
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


connection = Connection("data.10-g.com", 27017)


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
    """Lookup the listings for the given companies

    Example cik: 0000789019 - msft
    0000320193 - aapl
    0001288776 - goog
    """


    db = connection.sec_data
    companies = db.companies
    output = []
    inner_output = []
    for cik in ciks:
        company = companies.find_one({'cik' : cik})
        temp_dic = defaultdict(dict)
        for key, values in company['values'].items():
            for value in values:
                if len(value['period']) == 2 and value['period'][1] == 'Q':
                    temp_dic[str(value['year']) + value['period'][::-1]][key] = value
        for time, info in sorted(temp_dic.items()):
            #sorted in chronological order
            print info
            line = [company['name'], time]
            for values in company_info:
                if values in info:
                    line.append(info[values]['value'])
                else:
                    line.append(None)
            output.append(line)

        transpose = map(list, zip(*[x[2:] for x in output]))
        for param in transpose:
            prev_val = 0
            try:
                prev_val = next(s for s in param if s)
            except:
                pass
            #enumerate over the values of this parameter over time
            for index, value in enumerate(param):
                if value is not None:
                    param[index] = value
                    prev_val = value
                else:
                    param[index] = prev_val
        detransposed = zip(*transpose)
        inner_output.extend([zipped[0][:2] + list(zipped[1]) for zipped in zip(output, detransposed)])
    return inner_output

def get_ciks_for_group(x):
    divisions = connection.sec_data2.devisions
    companies = connection.sec_data.companies
    if type(x) == str:
        division = divisions.find({'id' : x})
        start_num = int(division['start'] + '00')
        end_num = int(division['end'] + '99')

    elif len(x) == 2:
        pass
    elif len(x) == 3:
        pass
    elif len(x) == 4:
        pass
