import threading
import time
import datetime #Get time
import pytz #pip install pytz
import subprocess #Run Bash code from Python
import sys #Args
import os
from pathlib import Path #create a folder
import platform #Type of OS

# Global variables
CurrentMin = None
Now = False
port = None


# Function to perform the comparison
def compare_and_set_flag(port, folder_name_str):
    global CurrentMin, Now
    chosen_time = "37"
    print(f"Next report at MM: {chosen_time}")
    while True:
        # Compare with "01" every minute
        print("CurrentMin:", CurrentMin, "|" , "Now status:", Now)
        if CurrentMin == chosen_time:
            Now = True
            ToDo(Now, port, folder_name_str)
        else:
            Now = False

        # Sleep for 60 seconds
        time.sleep(60)

# Function to update CurrentMin every minute
def update_current_minute():
    global CurrentMin

    while True:
        # Get the current minute
        CurrentMin = time.strftime("%M")

        # Sleep for 60 seconds
        time.sleep(60)

#Get Pacific's time
def get_pacific_time():
    # Set the time zone for Pacific Time
    pacific_tz = pytz.timezone('America/Los_Angeles')

    # Get the current time in the Pacific Time zone
    pacific_time = datetime.datetime.now(pacific_tz)

    return pacific_time.strftime('%Y-%m-%d-%H:%M:%S')

def get_linux_distribution():
    try:
        with open("/etc/os-release", "r") as f:
            for line in f:
                if line.startswith("PRETTY_NAME"):
                    return line.split("=")[1].strip().strip('"')
    except FileNotFoundError:
        return "Unknown distribution"


#Get Tehran's time
def get_iran_time():
    # Set the time zone for Iran
    iran_tz = pytz.timezone('Asia/Tehran')

    # Get the current time in the Iran time zone
    iran_time = datetime.datetime.now(iran_tz)

    return iran_time.strftime('%Y%m%d-%H%M%S')

# Function to perform the task when condition is met
def ToDo(flag, port, folder_name_str):
    #print("Port: ", port)
    print("\n")
    if flag:
        print("Condition met. Performing task now.")

        #Creating a file
        iran_time = get_iran_time()
        filename = iran_time  # Specify the desired filename
        #Add .log to filename
        filename += ".log"

        # Construct the full filepath within the folder
        filepath = os.path.join(folder_name_str, filename)

        # Get the operating system
        operating_system = platform.system()
        print(f"OS is {operating_system}")
        if operating_system == "Windows":
            Check_port_for_windows(port, filepath)
        elif operating_system == "Linux":
            print("Confirmed Linux.")
            distribution = get_linux_distribution().lower()
            #distribution = platform.linux_distribution()[0].lower()
            print(f"Distribution is {distribution}")
            if "debian" in distribution:
                Check_port_for_debian(port, filepath)
            elif "ubuntu" in distribution:
                print("Confirmed Ubuntu.")
                Check_port_for_ubuntu(port, filepath)
            elif "kali" in distribution:
                #perform_task_for_kali_linux()
                print("Kalinux is here ...")
            else:
                print(f"Unsupported Debian-based distribution: {distribution}")
        else:
            print("Unsupported operating system")


def Check_port_for_windows(port, filepath):
    pacific_time = get_pacific_time()

    netstat_output = subprocess.check_output(["netstat", "-an"], universal_newlines=True)

    # Split the output into lines and filter for the specified port
    output_lines = [line for line in netstat_output.split('\n') if f':{port}' in line]

    # Check if there are no connections
    if not output_lines:
        output_lines.append(f'No connection for port {port} - {pacific_time}')
    else:
        output_lines.insert(0, f'List of connections for port {port} - {pacific_time}')

    # Join the lines into a single string
    output_string = '\n'.join(output_lines)

    # Write the output string
    with open(filepath, 'w') as file:
        file.write(output_string)

    print(f"Output written to {filepath}.")

def Check_port_for_ubuntu(port, filepath):
    pacific_time = get_pacific_time()
    # Task to perform on Debian (or Debian-based systems)
    print("Performing task for Ubuntu...")
    try:
        # Run the netstat and grep command
        command = f"netstat -tn | grep ':{port}' | grep 'ESTABLISHED' | awk '{{print $5}}' | awk -F ':' '{{print " \
                  f"$1\":\"$2}}' "

        # Execute the command and capture the output
        output = subprocess.check_output(command, shell=True, text=True)
        # Split the output into lines and filter for the specified port
        output_lines = [line for line in output.split('\n') if f':{port}' in line]
        # Check if there are no connections
        if not output_lines:
            output_lines.append(f'No connection for port {port} - {pacific_time}')
        else:
            output_lines.insert(0, f'List of connections for port {port} - {pacific_time}')

        # Join the lines into a single string
        output_string = '\n'.join(output_lines)

        # Write the output string
        with open(filepath, 'w') as file:
            file.write(output_string)
        """
        # Save the output to the specified file
        with open(filepath, 'w') as file:
            # file.write("A")
            file.write(output)
        """
        print(f"Output appended to {filepath}.")

    except ValueError:
        print("Command couldn't run")


def Check_port_for_debian(port, filepath):
    # Task to perform on Debian (or Debian-based systems)
    print("Performing task for Debian...")
    try:
        # Run the netstat and grep command
        command = f"netstat -tn | grep ':{port}' | grep 'ESTABLISHED' | awk '{{print $5}}' | awk -F ':' '{{print " \
                  f"$1\":\"$2}}' "

        # Execute the command and capture the output
        output = subprocess.check_output(command, shell=True, text=True)

        # Save the output to the specified file
        with open(filepath, 'w') as file:
            #file.write("A")
            file.write(output)

        print(f"Output appended to {filepath}.")

    except ValueError:
        print("Command couldn't run")

if __name__ == "__main__":
    print("Welcome to Port detector!\n")

    if len(sys.argv) != 2:
        print("Usage: python script.py <port_number>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])

        # Create the folder using os
        # Specify the folder name
        folder_name = port
        # Convert the integer to a string
        folder_name_str = str(folder_name)


        """
        # Check if the folder was created
        if os.path.exists(folder_name_str):
            print(f"Folder '{folder_name_str}' created successfully.")
        else:
            print(f"Failed to create folder '{folder_name_str}'.")
        """
        if not os.path.exists(folder_name_str):
            # Create the folder
            os.mkdir(folder_name_str)
            print(f"Folder '{folder_name_str}' created.")
        else:
            print(f"Folder '{folder_name_str}' already exists.")

        """
        # Alternatively, you can use pathlib for a more Pythonic approach:
        folder_path = Path(folder_name)
        folder_path.mkdir()

        # Check if the folder was created
        if folder_path.exists():
            print(f"Folder '{folder_name}' created successfully.")
        else:
            print(f"Failed to create folder '{folder_name}'.")

        """
        # Create and start the threads
        update_thread = threading.Thread(target=update_current_minute)
        compare_thread = threading.Thread(target=compare_and_set_flag, args=(port, folder_name_str))

        # Start the threads
        update_thread.start()
        compare_thread.start()

        # Join the threads to ensure they finish before exiting
        update_thread.join()
        compare_thread.join()

    except ValueError:
        print("Port number should be an integer.")
        sys.exit(1)

#wget https://github.com/arkh91/PortDetector/archive/master.zip && unzip master.zip
