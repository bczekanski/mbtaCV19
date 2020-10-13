import pandas as pd
import requests
import json
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import urllib




# Load JSON
def load_daily(stdt, enddt):
    # gses = pd.DataFrame([])
    dts = pd.date_range(stdt, enddt)
    params = dict()
    params["outFields"] = 'service_date, time_period, station_name, route_or_line, gated_entries'
    params["f"] = "json"
    base_url = 'https://services1.arcgis.com/ceiitspzDAHrdGO1/arcgis/rest/services/GSE/FeatureServer/0/query?'          
    attrs = []
    for dat in dts:
        print(dat)
        dat = pd.to_datetime(dat)
        dat_prev = dat-dt.timedelta(1)
        dat = str(dat)[:-9]
        dat_prev = str(dat_prev)[:-9]
        for rol in ['Green', 'Blue', 'Red', 'Orange', 'Silver']:
            print(rol)
            params["where"] = "route_or_line='" + rol + " Line'" +\
                            " AND service_date>TIMESTAMP'" + dat_prev + "'"  +\
                               " AND service_date<=TIMESTAMP '" + dat + "'"
            encoded_params = urllib.parse.urlencode(params)
            url = base_url + encoded_params
            resp = requests.get(url)
            data = resp.json()
            if (len(list(data)) >= 6):
                print("The request appears to be too large")
                print(data['exceeededTransferLimit'])
            for row in data['features']:
                attrs.append(row['attributes'])
    gses = pd.DataFrame.from_dict(attrs)
    # gses = gses.append(attrs)
    return(gses)
        


gses = load_daily("2020-03-01", "2020-04-01")
print(gses.head())

gses['date'] = pd.to_datetime(gses.service_date, unit='ms').dt.date
gses['gated_entries'] = pd.to_numeric(gses['gated_entries'])
gses_agg_line = gses[['date', 'station_name', 'route_or_line', 'gated_entries']].\
                    groupby(['date', 'route_or_line'])['gated_entries'].\
                    sum().\
                    reset_index(name='entries')

print(gses_agg_line.head(100))


fig, axes = plt.subplots(3, 2)
for i, rol in enumerate(gses_agg_line.route_or_line.unique()):
    gses_agg_line[(gses_agg_line.route_or_line == rol) & (gses_agg_line.date >= pd.to_datetime('2014-01-01'))].set_index('date').plot(ax=axes.flat[i])
axes[-1, -1].axis('off')
fig.suptitle('MBTA GSEs by Line, 2020')
plt.show()
