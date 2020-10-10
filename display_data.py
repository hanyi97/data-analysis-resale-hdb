"""This is a module to display dataset as a summary table
    For user to view everything in the dataset"""

import data_helper

# read the dataset into a data table using Pandas
df = data_helper.get_dataframe()


# Function to display dataset.
def display_dataset():
    return print(df)


# Display no. of rows and columns in dataset
print('This dataset has %d rows and %d columns.' % (df.shape[0], df.shape[1]))
# Call function to display dataset
display_dataset()

# user filter selection input
in_col = {"year": 2019, "town": "YISHUN"}


def get_filtered_data(in_col):
    """Select the data rows according to the user input

    Parameters:
    in_col dictionary. key = column, value = column data value

    Returns:
    dataframe: dataframe of filtered results
    """
    df = data_helper.get_dataframe()
    for row in df.iterrows():
        for column in df.columns:
            for key in in_col.keys():
                if column == key:
                    # get the rows based on the condition in in_col
                    df = df[df[column].isin(in_col.values())]
        return df

    # user did not select any inputs to filter the dataframe, return dataframe result
    if in_col == {}:
        return df


# Call get_filtered_data function to display filtered dataset
print(get_filtered_data(in_col))
