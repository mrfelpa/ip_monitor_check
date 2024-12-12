# Key Features

- Checks external IP address at configurable intervals
- Automatic email sending
- Alert sound playback
- Custom command execution
- Windows and Linux compatible

  ![figure](https://github.com/user-attachments/assets/427feeab-c44b-4455-af11-ded456f715ee)


# Pre-requisites

Python 3.7+

# Installation

    git clone https://github.com/mrfelpa/ip_monitor_check.git

    cd ip_monitor_check.

    pip install -r requirements.txt

# Custom Configuration

- In the main file, you can modify the following parameters:

-  ***CHECK_INTERVAL:*** IP check interval (default: 300 seconds)
-  ***NOTIFICATION_EMAIL:*** Email settings
-  ***ALERT_SOUND:*** Sound notification settings
- ***COMMAND_EXECUTION:*** Command to execute on IP change

# Running

    python ip_monitor.py

- Checks external IP via API
- Compares with last known IP
- Triggers configured notifications in case of change
- Updates status interface
- Waits for next check interval

# Limitations

- Internet connectivity dependent
- Performance may vary depending on network configuration
- Request instructions to execute system commands

# Future improvements

- [ ] Add IP Address Identifier (Old and New)
- [ ] Add support for multiple IP check APIs
- [ ] Implement change log
- [ ] Create daemon/service for continuous execution
