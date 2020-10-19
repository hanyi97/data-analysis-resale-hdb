import pandas as pd
import data_helper
import plotly.express as px

df = pd.read_csv("resources/resale_flat_prices.csv")
df['all'] = 'Singapore'
fig = px.treemap(df, path=['all', 'region', 'town','year'],
    color='resale_price',
    color_continuous_scale=['#82ff97', '#ff0000'],
    )

fig.data[0].hovertemplate = '%{label}<br>Number of flats: %{value} <br>Average resale price: $%{color:,.0f}'
fig.write_image("resources/treemap.png")
fig.show()

