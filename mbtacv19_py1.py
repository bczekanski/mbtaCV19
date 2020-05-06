from matplotlib.figure import Figure
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

gses = pd.read_csv('./Desktop/MBTACV19/MBTA_Gated_Station_Entries.csv', nrows = 3e6)
gses['date'] = pd.to_datetime(gses['service_date'])
gses_agg_line = gses[['date', 'station_name', 'route_or_line', 'gated_entries']].groupby(['date', 'route_or_line'])['gated_entries'].sum().reset_index(name='entries')


fig, axes = plt.subplots(3, 2)
for i, rol in enumerate(gses_agg_line.route_or_line.unique()):
    gses_agg_line[(gses_agg_line.route_or_line == rol) & (gses_agg_line.date >= '2020-01-01')].set_index('date').plot(ax=axes.flat[i])
axes[-1, -1].axis('off')
fig.suptitle('MBTA GSEs by Line, 2020')
# plt.show()

# gses_agg_line['month'] =  gses_agg_line['date'].dt.month
gses_agg_line['year'] =  gses_agg_line['date'].dt.year
gses_agg_line['doy'] = gses_agg_line['date'].dt.dayofyear

fig, axes = plt.subplots(3, 2)
for i, rol in enumerate(gses_agg_line.route_or_line.unique()):
    for yr in [2018, 2019, 2020]:
        gses_agg_line.loc[(gses_agg_line['year'] == yr) & (gses_agg_line.route_or_line == rol), ['doy', 'entries']].set_index('doy').plot(ax=axes.flat[i])
axes[-1, -1].axis('off')
fig.suptitle('MBTA GSEs by Line and Year, 2018-2020')

plt.show()