import pandas as pd
import data_helper
import plotly.express as px
import chart_studio
import chart_studio.plotly as py

df = pd.read_csv("resources/resale_flat_prices.csv")
df['all'] = 'Singapore'
fig = px.treemap(df, path=['all', 'region', 'town','year'],
    color='resale_price',
    color_continuous_scale=['#82ff97', '#ff0000'],
    )

fig.data[0].hovertemplate = '%{label}<br>Number of flats: %{value} <br>Average resale price: $%{color:,.0f}'
fig.write_image("resources/treemap.png")
fig.show()
# url=py.iplot(fig, filename='resources/treemap.png')
# print(url)

username = 'si00' # your username
api_key = '8lS8m4e7TxpSF03SfLcU' # your api key - go to profile > settings > regenerate key
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

py.plot(fig, filename = 'treemap', auto_open=True)


