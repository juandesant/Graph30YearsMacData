# Get the data from Apple's website
import requests
first_mac_json_url = "http://www.apple.com/30-years/api/mac/data/first-mac.json"
machine_json_url = "http://www.apple.com/v/30-years/a/scripts/datavis/machinelist.json"
machine_use_json_url = "http://www.apple.com/30-years/api/mac/data/use.json"

rMachines  = requests.get(machine_json_url)
rUsage     = requests.get(machine_use_json_url)
rFirstMacs = requests.get(first_mac_json_url)
machines   = rMachines.json()['machines'] # See [1]
usage      = rUsage.json()['data'] # See [2]
first_mac  = rFirstMacs.json()['data'] # See [3]

# [1] machines is a list of dictionaries, each element
# corresponding to a different Mac model; each 
# dictionary is of the form:
# {
#     'id': 'model_id',
#     'name': 'Model name',
#     'year': 'Year of introduction',
#     'character': 'Unicode character in the mac-icon-standard font that represents it'
# }

# [2] usage is a list of dictionaries, each element
# corresponding to a different Mac model; each
# dictionary is of the form:
# { 
#     'id': 'model_id',
#     'categories': {
#         'category1': 'category1-users-per-1',
#         'category2': 'category2-users-per-1',
#         ...
#         'categoryN': 'categoryN-users-per-1',
#     }
# }

# [3] first_mac is a list of 5 dictionaries of the form:
# {
#     'id':    'model_id',
#     'value': 'percentage'
# }
# corresponding to the five most popular Macs used as an
# entry point

# Get list of machine ids

# Get all available categories; works even if not all categories are
# given for each model
from sets import Set
categories = list(
    reduce(
        lambda x,y: x.union(y), # assumes x and y are of class Set
        map(
            lambda x: Set(x['categories'].keys()), # Set of individual categories
            usage
        ) # list of categories for each model
    ) # union set of categories
) # list

def model_name(model_id):
    return filter(lambda x: x['id'] == model_id, machines)[0]['name']

years = range(1984,2014+1)
# Get the machines launched each year, using dictionary comprehension
machines_per_year = {
    year: map(
            lambda x: (x['id'], model_name(x['id'])),
            filter(lambda x: x['year'] == str(year), machines)
    )
    for year in years
}

num_machines_per_year = {
    year: len(machines_per_year[year])
    for year in years # machines_per_year.keys()
}


# Get values for each category over the years:
