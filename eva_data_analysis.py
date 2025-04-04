#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import matplotlib.pyplot as plt
import pandas as pd

def read_json_to_dataframe(input_file):
    """Reads json input file.

    Args:
        input_file (_io.TextIOWrapper): JSON input file.

    Returns:
        pandas.core.frame.DataFrame: data from the JSON file as a pandas dataframe
    """
    # Read the data from a JSON file into a Pandas dataframe
    eva_df = pd.read_json(input_file, convert_dates=['date'])
    eva_df['eva'] = eva_df['eva'].astype(float)
    # Clean the data by removing any incomplete rows and sort by date
    eva_df.dropna(axis=0, inplace=True)
    eva_df.sort_values('date', inplace=True)
    return eva_df

def write_dataframe_to_csv(df, output_file):
    """Write a pandas dataframe to a CSV file.

    Args:
        df (pandas.core.frame.DataFrame): pandas dataframe to write to CSV
        output_file (_io.TextIOWrapper): Output file object.
    """
    print(f'Saving to CSV file {output_file}')
    # Save dataframe to CSV file for later analysis
    df.to_csv(output_file, index=False)

def add_duration_hours_variable(df):
    """
    Add duration in hours (duration_hours) variable to the dataset

    Args:
        df (pd.DataFrame): The input dataframe.

    Returns:
        df_copy (pd.DataFrame): A copy of df_ with the new duration_hours variable added
    """
    df_copy = df.copy()
    df_copy["duration_hours"] = df_copy["duration"].apply(
        text_to_duration
    )
    return df_copy

def text_to_duration(duration):
    """
    Convert a text format duration "HH:MM" to duration in hours

    Args:
        duration (str): The text format duration

    Returns:
        duration_hours (float): The duration in hours
    """
    hours, minutes = duration.split(":")
    duration_hours = int(hours) + int(minutes)/60
    return duration_hours

def plot_cumulative_time_in_space(df, graph_file):
    """
    Plot the cumulative time spent in space over years

    Convert the duration column from strings to number of hours
    Calculate cumulative sum of durations
    Generate a plot of cumulative time spent in space over years and
    save it to the specified location

    Args:
        df (pd.DataFrame): The input dataframe.
        graph_file (str): The path to the output graph file.

    Returns:
        None
    """
    print(f'Plotting cumulative spacewalk duration and saving to {graph_file}')
    df = add_duration_hours_variable(df)
    df['cumulative_time'] = df['duration_hours'].cumsum()
    plt.plot(df.date, df.cumulative_time, 'ko-')
    plt.xlabel('Year')
    plt.ylabel('Total time spent in space to date (hours)')
    plt.tight_layout()
    plt.savefig(graph_file)
    plt.show()

def main(input_file, output_file, graph_file):
    print("--START--")

    # Read the data from JSON file
    print(f'Reading JSON file {input_file}')
    eva_data = read_json_to_dataframe(input_file)

    # Add crew size column.
    eva_data = add_crew_size_column(eva_data)

    # Convert and export data to CSV file
    write_dataframe_to_csv(eva_data, output_file)

    # Plot data
    plot_cumulative_time_in_space(eva_data, graph_file)

    print("--END--")

def calculate_crew_size(crew):
    """
    Calculate the size of the crew for a single crew entry

    Args:
        crew (str): The text entry in the crew column containing a list of crew member names

    Returns:
        (int): The crew size
    """
    if crew.split() == []:
        return None
    else:
        return len(re.split(r';', crew))-1

def add_crew_size_column(df):
    """
    Add crew_size column to the dataset containing the value of the crew size

    Args:
        df (pd.DataFrame): The input data frame.

    Returns:
        df_copy (pd.DataFrame): A copy of df with the new crew_size variable added
    """
    print('Adding crew size variable (crew_size) to dataset')
    df_copy = df.copy()
    df_copy["crew_size"] = df_copy["crew"].apply(
        calculate_crew_size
    )
    return df_copy

# Main code
if __name__ == '__main__':
    if len(sys.argv) < 3:
        input_file = open('./data/eva-data.json', 'r', encoding='utf-8')
        output_file = open('./eva-data.csv', 'w', encoding='utf-8')
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

    graph_file = './cumulative_eva_graph.png'
    main(input_file, output_file, graph_file)
