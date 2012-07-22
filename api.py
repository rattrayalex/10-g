import sys
import re
import psycopg2

f = open('database_info.txt')
conn = psycopg2.connect(f.read())

result_keys = ["ticker", "entity_name", "effective_value", "fiscal_year", 
               "calendar_period", "field_name"]

base_query = """select
                    ticker(entity_id),
                    entity_name,
                    effective_value,
                    fiscal_year,
                    calendar_period,
                    local_name
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

def get_companies_dict(infile):
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


#Entity_codes, field_name, quarter, fiscal_year
#{'entity_code' : '0000789019', "field_name": '%Capital'}

def get_listings(params):
    conditions = []
    if "entity_codes" in params:
        params['entity_codes'] = tuple(params['entity_codes'])
        conditions.append("entity_code in %(entity_codes)s")
    
    if "entity_code" in params:
        conditions.append("entity_code = %(entity_code)s")
    
    if "field_name" in params:
        conditions.append("local_name like %(field_name)s")

    if "quarter" in params:
        conditions.append("quarter like %(quarter)s")

    if "year" in params:
        conditions.append("fiscal_year like %(fiscal_year)s")

    cur = conn.cursor()
    cur.execute(base_query + " where " +
                " and ".join(conditions), params)
    return clean(cur.fetchall())




def clean(query_results):
    answer = []
    for result in query_results:
        out_res = dict(zip(result_keys, result))
        out_res['effective_value'] = float(out_res['effective_value'])
        answer.append(out_res)
    return answer