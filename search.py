"""This is a module to filter/search data in the summary table.
    The summary table will be changed based on what user has filtered/searched."""
# note that the comments will be updated

import data_helper

# read the dataset into a data table using Pandas
df = data_helper.get_dataframe()
in_dict = {}


# get all values in a column, this only get 1 column, call in GUI
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


# get column name/ name of combo box and selected input for the combobox, call in GUI
# input eg. filter_option_year, filter_option_month, filter_option_town...etc
# incomplete: if user select an input then decided not to filter anything for that column (b4 sumission)
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
    # if the filter_option is region, the available inputs for town will be updated
    if filter_option == "region":
        region_input = selected_input
        return data_helper.get_filtered_towns(region_input)
    return in_dict


# call when clicked on button
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
                    print("No result found.\nPlease check your filter selection for 'town' and 'region'.\n")
                    return df

        return df


# to test the functions
print(dict_input("region", "NORTH"))
print(dict_input("town", "YISHUN"))
# call to get_filtered_data function to display filtered dataset
print(get_filtered_data(in_dict))
