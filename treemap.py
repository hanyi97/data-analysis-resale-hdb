import pandas as pd
import plotly.express as px

df = pd.read_csv("resources/resale_flat_prices.csv")
df['Region'] = 'Region'
fig = px.treemap(df, path=['Region', 'region', 'town'], color='resale_price', color_continuous_scale=['#ccffcc', '#ffa751', '#fb1003'], maxdepth=2)
fig.show()

