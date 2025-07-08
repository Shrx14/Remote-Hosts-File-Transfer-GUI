# Remote Hosts File Transfer GUI

## Description
Remote Hosts File Transfer GUI is a Python Tkinter GUI application that allows users to copy a selected file to multiple remote hosts (IP addresses or hostnames) at a specified destination path. The application performs the copy operation in parallel threads to keep the interface responsive and logs the results of each copy attempt in a CSV file.

## Features
- Enter multiple IP addresses or hostnames (one per line).
- Browse and select the source file to copy.
- Specify the destination path relative to each host.
- Copy files concurrently to all specified hosts.
- View status updates and completion messages.
- Logs all copy attempts with timestamps, hosts, file names, destination paths, and status in `copy_log.csv`.

## Requirements
- Python 3.x
- Tkinter (usually included with standard Python installations)
- Network access to the target hosts with appropriate permissions to write to the destination path.

## Installation
No special installation is required. Ensure Python 3 and Tkinter are installed on your system.

## Usage
1. Run the application:
   ```bash
   python copy_to_hosts.py
   ```
2. In the GUI:
   - Enter the IP addresses or hostnames of the target hosts, one per line.
   - Click the "Browse" button to select the file you want to copy.
   - Enter the destination path relative to each host (e.g., `C$\Users\Public\Documents`).
   - Click the "Copy File" button to start copying.
3. The status label will show progress, and a popup will notify when the copy operation is complete.

## Logging
All copy attempts are logged in `copy_log.csv` in the same directory as the script. The log includes:
- Date and time of the copy attempt
- Hostname or IP address
- File copied
- Destination path
- Status (Success or error message)

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
