import data_helper
import plotly.express as px
import chart_studio
import chart_studio.plotly as py

""" This module is to display the data as a treemap and enables 

   Parameters:
   px.treemap = Selecting the name of the variable in the dataframe (region, town, year)
   color = The variable to compare against (resale_price)
   color_continuous_scale = Differentiate the resale values based on the colour
   
   Returns:
   An interactive treemap based on the filtering of the specific data selected
   """

# Read the dataset via  Pandas
df = data_helper.get_dataframe()
df['all'] = 'Singapore'
# Filtering out the treemap based on the region, town and year and to compare against resale price.
fig = px.treemap(df, path=['all', 'region', 'town', 'year'],
                 color='resale_price',
                 color_continuous_scale=['#82ff97', '#ff0000'],
                 )
# Enables user to view the number of flats sold with the average resale price
fig.data[0].hovertemplate = '%{label}<br>Number of flats: %{value} <br>Average resale price: $%{color:,.0f}'
# Export the treemap as a static image
fig.write_image('resources/treemap.png')
fig.show()

username = 'si00'  # your username
api_key = '8lS8m4e7TxpSF03SfLcU'  # your api key - go to profile > settings > regenerate key
# Enables the use of the interactive treemap in the GUI
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

py.plot(fig, filename='treemap', auto_open=True)
