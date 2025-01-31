import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def load_data(csv_file):
    """
    Loads the CSV data into a pandas DataFrame.
    """
    return pd.read_csv(csv_file)

def synchronize_start_time(df):
    """
    Shifts the timestamps of all trajectories so that they start from the same reference.
    The first timestamp of each trajectory will be aligned to 0.
    """
    df['Timestamp'] = df.groupby('Trajectory_ID')['Timestamp'].transform(lambda x: x - x.min())
    return df



def plot_variable_for_all_trajectories(df, columns, title_template, ylabel_template, pdf):
    """
    Plots specified variables (from the given columns) for all Trajectory_IDs.
    This function works for any kind of data (joint, Cartesian, current, voltage).
    """
    trajectory_ids = df['Trajectory_ID'].unique()
    
    for column in columns:
        plt.figure(figsize=(10, 6))
        for trajectory_id in trajectory_ids:
            trajectory_data = df[df['Trajectory_ID'] == trajectory_id]
            plt.plot(trajectory_data['Timestamp'], trajectory_data[column], label=f"Trajectory {trajectory_id}")
        
        plt.xlabel('Time (aligned)')
        plt.ylabel(ylabel_template.format(column))
        plt.title(title_template.format(column))
        plt.legend(title="Trajectory_ID")
        plt.grid(True)
        plt.tight_layout()
        pdf.savefig()
        plt.close()


# Calculate power for each trajectory
def calculate_power(df):
    """
    Calculates the power for each trajectory by multiplying the current and voltage
    for each joint, then summing the results to generate a total power column.
    """
    current_columns = ['Current_1', 'Current_2', 'Current_3', 'Current_4', 'Current_5', 'Current_6']
    voltage_columns = ['Voltage_1', 'Voltage_2', 'Voltage_3', 'Voltage_4', 'Voltage_5', 'Voltage_6']
    
    power = sum(df[current] * df[voltage] for current, voltage in zip(current_columns, voltage_columns))
    df['Power'] = power
    
    return df

def plot_power_for_all_trajectories(df, pdf):
    """
    Plots the power values over time (aligned) for all Trajectory_IDs and saves the plots in a PDF.
    """
    trajectory_ids = df['Trajectory_ID'].unique()
    plt.figure(figsize=(10, 6))
    for trajectory_id in trajectory_ids:
        trajectory_data = df[df['Trajectory_ID'] == trajectory_id]
        plt.plot(trajectory_data['Timestamp'], trajectory_data['Power'], label=f"Trajectory {trajectory_id}")
    
    plt.xlabel('Time (aligned)')
    plt.ylabel('Power (W)')
    plt.title('Power for All Trajectories (Aligned Start Times)')
    plt.legend(title="Trajectory_ID")
    plt.grid(True)
    plt.tight_layout()
    pdf.savefig()
    plt.close()

def calculate_total_energy(df):
    """
    Calculates the total energy for each trajectory by summing the power values over time.
    """
    energy_dict = {}

    # Iterate through each trajectory ID and compute total energy
    for trajectory_id in df['Trajectory_ID'].unique():
        trajectory_data = df[df['Trajectory_ID'] == trajectory_id]

        # Compute the time step (Delta t) assuming uniform timestamps
        delta_t = trajectory_data['Timestamp'].diff().mean()  # Time difference in seconds

        # Calculate the total energy for the trajectory by summing Power * Delta t
        total_energy = (trajectory_data['Power'] * delta_t).sum()
        
        # Store the total energy for each trajectory
        energy_dict[trajectory_id] = total_energy

    # Convert the energy dictionary into a DataFrame for easy plotting
    energy_df = pd.DataFrame(list(energy_dict.items()), columns=['Trajectory_ID', 'Energy'])
    return energy_df

def plot_total_energy(df, energy_df, pdf):
    """
    Plots the total energy for each trajectory as a single point with energy values displayed on the plot.
    Saves the plot to a PDF.
    """
    plt.figure(figsize=(10, 6))
    
    # Plot a single point for each trajectory representing its total energy
    plt.scatter(energy_df['Trajectory_ID'], energy_df['Energy'], color='blue', label='Total Energy')

    # Annotate each point with the corresponding energy value
    for i, row in energy_df.iterrows():
        plt.text(row['Trajectory_ID'], row['Energy'], f"{row['Energy']:.2f}", fontsize=9, ha='center', va='bottom')
    
    # Add labels and title
    plt.xlabel('Trajectory ID')
    plt.ylabel('Total Energy (Joules)')
    plt.title('Total Energy for Each Trajectory')

    # Show grid and layout
    plt.grid(True)
    plt.tight_layout()

    # Save the plot to the PDF
    pdf.savefig()
    plt.close()



def save_plots_as_pdf(df, output_pdf="plots.pdf"):
    """
    Saves all plots for joint variables, Cartesian positions, currents, voltages, and power into a single PDF.
    """
    with PdfPages(output_pdf) as pdf:
        joint_columns = ['Joint_1', 'Joint_2', 'Joint_3', 'Joint_4', 'Joint_5', 'Joint_6']
        cartesian_columns = ['Cartesian_x', 'Cartesian_y', 'Cartesian_z', 'Cartesian_rx', 'Cartesian_ry', 'Cartesian_rz']
        current_columns = ['Current_1', 'Current_2', 'Current_3', 'Current_4', 'Current_5', 'Current_6']
        voltage_columns = ['Voltage_1', 'Voltage_2', 'Voltage_3', 'Voltage_4', 'Voltage_5', 'Voltage_6']

        plot_variable_for_all_trajectories(df, joint_columns, "Joint Variable ({}) for All Trajectories (Aligned Start Times)", "Joint Angle", pdf)
        plot_variable_for_all_trajectories(df, cartesian_columns, "Cartesian Position ({}) for All Trajectories (Aligned Start Times)", "Cartesian Position", pdf)
        plot_variable_for_all_trajectories(df, current_columns, "Current ({}) for All Trajectories (Aligned Start Times)", "Current", pdf)
        plot_variable_for_all_trajectories(df, voltage_columns, "Voltage ({}) for All Trajectories (Aligned Start Times)", "Voltage", pdf)

        # Calculate power and plot it
        df = calculate_power(df)
        plot_power_for_all_trajectories(df, pdf)
        
        # Calculate total energy for each trajectory
        energy_df = calculate_total_energy(df)
        
        # Plot total energy as a point for each trajectory
        plot_total_energy(df, energy_df, pdf)

        print(f"All plots saved to {output_pdf}")

if __name__ == "__main__":
    csv_file = 'robot_data_current.csv'  # Update this with your actual file path
    df = load_data(csv_file)
    df = synchronize_start_time(df)
    save_plots_as_pdf(df, output_pdf="robot_trajectory_plots.pdf")
