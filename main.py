import threading
import time
#Get time
import datetime
import pytz #pip install pytz
#Run Bash code from Python
import subprocess
import sys #Args

# Global variables
CurrentMin = None
Now = False
port = None


# Function to perform the comparison
def compare_and_set_flag(port):
    global CurrentMin, Now

    while True:
        # Compare with "01" every minute
        print("CurrentMin:", CurrentMin, "|" , "Now status:", Now)
        if CurrentMin == "25":
            Now = True
            ToDo(Now, port)
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

#Get Tehran's time
def get_iran_time():
    # Set the time zone for Iran
    iran_tz = pytz.timezone('Asia/Tehran')

    # Get the current time in the Iran time zone
    iran_time = datetime.datetime.now(iran_tz)

    return iran_time.strftime('%Y%m%d-%H%M%S')

# Function to perform the task when condition is met
def ToDo(flag, port):
    print("Port: ", port)
    if flag:
        print("Condition met. Performing task now.")
        iran_time = get_iran_time()
        filename = iran_time  # Specify the desired filename

        # Run the netstat and grep command
        command = f"netstat -tn | grep :{port} >> {filename}"
        subprocess.run(command, shell=True)

        print(f"Output appended to {filename}.")

if __name__ == "__main__":
    print("Welcome to Port detector!\n")

    if len(sys.argv) != 2:
        print("Usage: python script.py <port_number>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
        # Create and start the threads
        update_thread = threading.Thread(target=update_current_minute)
        compare_thread = threading.Thread(target=compare_and_set_flag, args=(port,))

        # Start the threads
        update_thread.start()
        compare_thread.start()

        # Join the threads to ensure they finish before exiting
        update_thread.join()
        compare_thread.join()

    except ValueError:
        print("Port number should be an integer.")
        sys.exit(1)
