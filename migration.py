import psycopg2

from collections import defaultdict
from pymongo import Connection
from api import get_companies_dict

base_query = """select
local_name,
effective_value,
fiscal_year,
calendar_period
from
entity
natural join
accession
natural join
fact
natural join
element
natural join
qname
natural join
context
natural join
context_aug"""

DB_CREDS = open('database_info.txt')
PG_CONN = psycopg2.connect(DB_CREDS.read())

DICT_KEYS = ['value', 'year', 'period']

MAPPINGS_DICT = {}

with open("mappings.dict", 'r') as MAPPINGS_FILE:
    for line in MAPPINGS_FILE:
        try:
            key, value = line.split()
        except:
            print line
        MAPPINGS_DICT[key] = value

def do_db_query(cik):
    cur = PG_CONN.cursor()
    cur.execute(base_query + " where entity_code = '%s'" % (cik))
    results = cur.fetchall()
    results_dict = defaultdict(list)
    for result in results:
        result = list(result)
        try:
            result[1] = int(result[1])
        except:
            continue
        results_dict[result[0]].append(dict(zip(DICT_KEYS, result[1:])))
    json_out = {}
    for key, value in results_dict.items():
        if key not in MAPPINGS_DICT:
            continue
            # if len(key) > 70:
            #     print "*%s" % key
            #     mapping = "ignore"
            # else:
            #     mapping = raw_input("%s: " % key)
            # if mapping == '':
            #     mapping = 'ignore'
            # MAPPINGS_DICT[key] = mapping
            # with open("mappings.dict", 'a') as MAPPINGS_FILE:
            #     MAPPINGS_FILE.write(key + " " + mapping + "\n")
        if MAPPINGS_DICT[key] == 'ignore':
            continue
        mapping = MAPPINGS_DICT[key]
        json_out[mapping] = value
    return json_out

companies_dict = get_companies_dict()
connection = Connection()
db = connection.sec_data
companies = db.companies
companies.remove()

count = 0
for company_ticker, company in companies_dict.items():
    count += 1
    company_name = company['name']
    print "###%d %s ###" % (count, company_name)
    company_cik = company['cik']
    #make json shit

    cur = PG_CONN.cursor()
    cur.execute("""select standard_industrial_classification 
                   from
                   accession natural join entity
                   where entity_code = '%s'""" % (company_cik))
    
    company_json = {}
    company_data = cur.fetchone()
    company_json['sic_code'] = company_data[0]
    company_json['values'] = do_db_query(company_cik)
    company_json['ticker'] = company_ticker
    company_json['name'] = company_name
    company_json['cik'] = company_cik
    companies.insert(company_json)
