"""This is a module to filter/search data in the summary table.
    The summary table will be changed based on what user has filtered/searched."""

import data_helper

# read the dataset into a data table using Pandas
df = data_helper.get_dataframe()

# declare dictionary to store the values
in_dict = {}


def get_unique(column):
    """Display all the values of a column in a dataframe

    Parameters:
    column: (str) the name of the variable in the dataframe

    Returns:
    (list) all the values in the column in ascending order
    """
    try:
        column_value = df[column].unique()
        column_value = sorted(list(map(str, column_value)))
        return column_value
    except ValueError:
        print("Please enter a valid column name in the dataframe.")


def dict_input(filter_option, selected_input):
    """Get all user input and store it as a dictionary.
    It will be updated for each input the user select.
    It will be updated for any changes in the input selection.

    Parameters:
    filter_option_: (str) a column name
    selected_input: (str) the selected value

    Returns:
    in_dict dictionary. key = (str) column, value = column data value
    """
    try:
        in_dict.update({filter_option: selected_input})
        # if the filter option is in the in_dict dictionary, the new input will be updated
        if filter_option in in_dict:
            in_dict[filter_option] = selected_input
        # if the filter_option is "region", the available inputs for "town" will be updated
        if filter_option == "region":
            region_input = selected_input
            return data_helper.get_filtered_towns(region_input)
        return in_dict
    except IndexError:
        print("Input is mandatory. Please select an input.")


def get_filtered_data(in_dict):
    """Display the data rows according to the user input

    Parameters:
    in_dict dictionary. key = (str) column, value = column data value

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
                    print("No data found.")
                    return df
        return df
