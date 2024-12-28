# System Performance Monitor

This project provides a Python script to monitor system performance, including CPU usage, memory usage, disk space usage, and top CPU-consuming processes. It also includes an alert mechanism for predefined thresholds and supports customizable output formats.

## Features
1. **System Information Collection**
   - CPU usage percentage.
   - Memory usage (total, used, free, and percentage).
   - Disk space usage (total, used, free, and percentage for each mounted filesystem).
   - Top 5 CPU-consuming processes.

2. **Alert Mechanism**
   - Triggers warnings if:
     - CPU usage exceeds 80%.
     - Memory usage exceeds 75%.
     - Disk space usage exceeds 90%.

3. **Customizable Options**
   - Monitoring interval (via `--interval`).
   - Output format (text or JSON) using `--format`.
   - Save the report to a file with `--output_file`.

4. **Error Handling**
   - Handles permission issues and invalid inputs gracefully.

## Requirements
- Python 3.8 or higher.
- `psutil` library.

To install `psutil`, run:
```bash
pip install psutil
```

## Usage
### Running the Script
Save the script as `monitor_system.py` and run it from the terminal:
```bash
python monitor_system.py [OPTIONS]
```

### Command-Line Options
- `--interval`: Monitoring interval in seconds (default: 10 seconds).
- `--format`: Output format (text or json; default: text).
- `--output_file`: File to save the report (optional).

### Examples
1. Monitor system performance with default settings:
   ```bash
   python monitor_system.py
   ```

2. Set a custom monitoring interval:
   ```bash
   python monitor_system.py --interval 5
   ```

3. Output the report in JSON format:
   ```bash
   python monitor_system.py --format json
   ```

4. Save the report to a file:
   ```bash
   python monitor_system.py --format text --output_file system_report.txt
   ```

### Example Output
#### Text Format:
```
System Performance Report
=========================
CPU Usage: 45%
Memory Usage:
  Total: 16777216000 bytes
  Used: 8388608000 bytes
  Free: 8388608000 bytes
  Percent: 50%
Disk Usage:
  /dev/sda1: {'total': 500000000000, 'used': 250000000000, 'free': 250000000000, 'percent': 50%}
Top 5 CPU-Consuming Processes:
  PID 1234, Name: python, CPU%: 12.5
  PID 5678, Name: chrome, CPU%: 10.0
  ...
```


## Notes
- Use `Ctrl+C` to stop monitoring.
- Make sure to run the script with sufficient permissions.




