"""This is a module to show the Top 10 Cheapest Resale Flats based on what flat type that user has selected
Function(get_cheapest_hdb) :  Retrieve Top 10 Cheapest HDB based on the selected flat_type with
other details, as a dataframe.
"""

import data_helper

# Read the dataset into a data table using Pandas.
df = data_helper.get_dataframe()
in_dict = {}


# Get all values in a column, this only get 1 column, call in GUI.
def get_unique(column):
    """Display the all values of a column in a dataframe

    Parameters:
    column is the name of the variable in the dataframe

    Returns:
    all the values in the column
    """
    column_value = df[column].unique()
    column_value = sorted(list(map(str, column_value)))
    return column_value


# Get column name/ name of combo box and selected input for the combobox, call in GUI.
def dict_input(filter_option, selected_input):
    """Get all user input and store it as a dictionary.
    It will be updated for each input the user select.
    It will be updated for any changes in the input selection.

    Parameters:
    filter_option_: a column name
    selected_input: the selected value

    Returns:
    in_dict dictionary. key = column, value = column data value
    """
    in_dict.update({filter_option: selected_input})
    # if the filter option is in the in_dict dictionary, the new input will be updated
    if filter_option in in_dict:
        in_dict[filter_option] = selected_input
    return in_dict


# Call when clicked on button.
def get_filtered_data(in_dict):
    """Display the data rows according to the user input

    Parameters:
    in_dict dictionary. key = column, value = column data value

    Returns:
    dataframe: dataframe of filtered results
    """
    # user did not select any inputs to filter the dataframe, return dataframe result
    df = data_helper.get_dataframe()
    if in_dict == {}:
        return df
    # user did select at least 1 input to filter the dataframe, return dataframe result
    else:
        for column in df.columns:
            if column in in_dict.keys():
                # get the rows based on the condition in in_col
                df = df[df[column].isin(in_dict.values())]
                if df.empty:
                    print("No result found.\nPlease check your filter selection for 'flat_type'.\n")
                    return df

        return df


def get_cheapest_hdb(rows=10):
    """Get cheapest HDB based on user filtered result
    Top n cheapest HDB based on each flat type

    Parameters:
    rows (int): number of rows for each flat type

    Returns:
    dataframe: dataframe of cheapest HDB based on flat type
    """
    cheap_data = get_filtered_data(in_dict) \
        .sort_values(['flat_type', 'resale_price']) \
        .groupby('flat_type').head(rows) \
        .reset_index(drop=True)

    return cheap_data


# Testing functions
print(dict_input("flat_type", "1 ROOM"))
# Call get_cheapest_hdb function to retrieve Top 10 Cheapest HDB
#   based on the selected flat_type with other details, as a dataframe.
print(get_cheapest_hdb())
