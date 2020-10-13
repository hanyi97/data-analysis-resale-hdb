"""This is a module to filter/search data in the summary table.
    The summary table will be changed based on what user has filtered/searched."""

import data_helper
import pandas as pd

# read the dataset into a data table using Pandas
df = data_helper.get_dataframe()

# user filter selection input
# in_col = {"year": 2019, "town": "YISHUN"}
in_col = {"year": 2019, "month": 6, "town": "HOUGANG", "region": "CENTRAL", "flat_type": "4 ROOM", "block": 220,
          "street_name": "HOUGANG ST 21", "storey_range": "01 TO 03", "floor_area_sqm": 103,
          "flat_model": "Model A", "lease_commence_date": 1992, "remaining_lease": "71 - 80", "resale_price": 520000}


def get_filtered_data(in_col):
    """Select the data rows according to the user input

    Parameters:
    in_col dictionary. key = column, value = column data value

    Returns:
    dataframe: dataframe of filtered results
    """
    df = data_helper.get_dataframe()
    # user did not select any inputs to filter the dataframe, return dataframe result
    if in_col == {}:
        return df
    # user did select at least 1 input to filter the dataframe, return dataframe result
    else:
        for column in df.columns:
            if column in in_col.keys():
                # get the rows based on the condition in in_col
                df = df[df[column].isin(in_col.values())]
                if df.empty:
                    print("No result found.\nPlease check your filter selection for 'town' and 'region'.\n")
                    return df
        return df


# Call get_filtered_data function to display filtered dataset
print(get_filtered_data(in_col))
