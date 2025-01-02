import subprocess
import time
import os
import json
import csv

CSV_FILE_NAME = "bluetooth_metrics.csv"

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode("utf-8").strip()

def get_bt_pid():
    try:
        bt_pid = subprocess.check_output(["pidof", "Bluetooth"]).decode("utf-8").strip()
        return bt_pid
    except subprocess.CalledProcessError:
        print("Bluetooth process not found.")
        return None

def get_fd_count(pid):
    try:
        fd_count = len(os.listdir(f"/proc/{pid}/fd"))
        return fd_count
    except FileNotFoundError:
        print("Error retrieving file descriptor count.")
        return None

def get_memory_usage(pid):
    try:
        mem_output = subprocess.check_output(["pmap", "-x", pid]).decode("utf-8")
        mem_usage = mem_output.splitlines()[-1].split()[2]
        return mem_usage
    except subprocess.CalledProcessError:
        print("Error retrieving memory usage.")
        return None

def get_cpu_details():
    bt_pid = get_bt_pid()
    if bt_pid:
        print(f"Bluetooth process ID: {bt_pid}")
        time_output = run_command(["ps", "-p", bt_pid, "-o", "%t"])
        time_output = time_output.strip().split()[1]
        print("ELAPSED Time:", time_output)

        mem_output = run_command(["ps", "-p", bt_pid, "-o", "%mem"])
        mem_output = mem_output.strip().split()[1]
        print("MEM:", mem_output)

        cpu_output = run_command(["ps", "-p", bt_pid, "-o", "%cpu"])
        cpu_output = cpu_output.strip().split()[1]
        print("CPU:", cpu_output)

        fd_count = get_fd_count(bt_pid)
        print(f"Open File Descriptor Count: {fd_count}")

        mem_usage = get_memory_usage(bt_pid)
        print(f"Process Memory Usage: {mem_usage} KB")

        # Write to CSV file
         # Check if the file is empty (no header) and write the header if needed
        file_exists = os.path.isfile(CSV_FILE_NAME)
        with open(CSV_FILE_NAME, "a", newline="") as csvfile:
            fieldnames = ["Time", "Elapsed Time", "Memory", "CPU", "File Descriptors", "Memory Usage"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()  # Write header only if file is empty
            writer.writerow({
                "Time" : time.strftime("%Y-%m-%d %H:%M:%S"),
                "Elapsed Time": time_output,
                "Memory": mem_output,
                "CPU": cpu_output,
                "File Descriptors": fd_count,
                "Memory Usage": mem_usage
            })
        print("Metrics written to bluetooth_metrics.csv")
    else:
        print("Bluetooth process not found.")

def main():
        get_cpu_details()

        while True:
            print("............................")

            # Run frontdoorutil command and print output
            frontdoor_output = run_command(["frontdoorutil", "-c", "POST", "/bluetooth/source/scan", "{}"])
            print(json.loads(frontdoor_output))

            time.sleep(5)

            get_cpu_details()

            time.sleep(10)

            # Stop Bluetooth scan
            frontdoor_output = run_command(["frontdoorutil", "-c", "POST", "/bluetooth/source/stopScan", "{}"])
            print(json.loads(frontdoor_output))

            time.sleep(1)


if __name__ == "__main__":
    main()