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

def plot_cumulative_time_in_space(df, graph_file):
    # add extra columns used for plotting
    df = add_duration_hours_variable(df)

    print(f'Plotting cumulative spacewalk duration and saving to {graph_file}')
    # Plot cumulative time spent in space over years
    plt.plot(df['date'], df['cumulative_time'], 'ko-')
    plt.xlabel('Year')
    plt.ylabel('Total time spent in space to date (hours)')
    plt.tight_layout()
    plt.savefig(graph_file)
    plt.show()

def add_duration_hours_variable(df):
    df_copy = df.copy()
    df_copy['duration_hours'] = df['duration'].str.split(":").apply(lambda x: int(x[0]) + int(x[1])/60)
    df_copy['cumulative_time'] = df_copy['duration_hours'].cumsum()
    return df_copy

def main(input_file, output_file, graph_file):
    print("--START--")

    # Read the data from JSON file
    print(f'Reading JSON file {input_file}')
    eva_data = read_json_to_dataframe(input_file)

    # Convert and export data to CSV file
    write_dataframe_to_csv(eva_data, output_file)

    # Plot data
    plot_cumulative_time_in_space(eva_data, graph_file)

    print("--END--")

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
