import sys
import re

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
