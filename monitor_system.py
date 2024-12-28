import psutil
import argparse
import time
import json
import os


def collect_system_info():
    # Collect CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)

    # Collect memory usage
    memory = psutil.virtual_memory()
    memory_info = {
        "total": memory.total,
        "used": memory.used,
        "free": memory.free,
        "percent": memory.percent
    }

    # Collect disk usage
    disk_partitions = psutil.disk_partitions()
    disk_usage = {}
    for partition in disk_partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_usage[partition.device] = {
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent
            }
        except PermissionError:
            disk_usage[partition.device] = "Permission Denied"

    # Get top 5 CPU-consuming processes
    processes = [(proc.info['pid'], proc.info['name'], proc.info['cpu_percent'])
                 for proc in psutil.process_iter(['pid', 'name', 'cpu_percent'])]
    top_processes = sorted(processes, key=lambda x: x[2], reverse=True)[:5]

    return {
        "cpu_usage": cpu_usage,
        "memory_info": memory_info,
        "disk_usage": disk_usage,
        "top_processes": top_processes
    }

def trigger_alerts(info):
    alerts = []

    if info["cpu_usage"] > 80:
        alerts.append("Warning: CPU usage exceeds 80%!")

    if info["memory_info"]["percent"] > 75:
        alerts.append("Warning: Memory usage exceeds 75%!")

    for device, usage in info["disk_usage"].items():
        if isinstance(usage, dict) and usage["percent"] > 90:
            alerts.append(f"Warning: Disk usage on {device} exceeds 90%!")

    for alert in alerts:
        print(alert)

def output_report(info, format, output_file=None):
    if format == "text":
        report = """
System Performance Report
=========================
CPU Usage: {cpu_usage}%
Memory Usage:
  Total: {memory_total} bytes
  Used: {memory_used} bytes
  Free: {memory_free} bytes
  Percent: {memory_percent}%
Disk Usage:
{disk_report}
Top 5 CPU-Consuming Processes:
{processes}
        """.format(
            cpu_usage=info["cpu_usage"],
            memory_total=info["memory_info"]["total"],
            memory_used=info["memory_info"]["used"],
            memory_free=info["memory_info"]["free"],
            memory_percent=info["memory_info"]["percent"],
            disk_report="\n".join(
                [f"  {device}: {usage}" for device, usage in info["disk_usage"].items()]
            ),
            processes="\n".join(
                [f"  PID {pid}, Name: {name}, CPU%: {cpu}" for pid, name, cpu in info["top_processes"]]
            )
        )
        if output_file:
            with open(output_file, "w") as f:
                f.write(report)
        else:
            print(report)

    elif format == "json":
        if output_file:
            with open(output_file, "w") as f:
                json.dump(info, f, indent=4)
        else:
            print(json.dumps(info, indent=4))
    # csv can be added to
    
    else:
        print("Unsupported format! Please choose text or json.")

def main():
    parser = argparse.ArgumentParser(description="System Performance Monitor")
    parser.add_argument("--interval", type=int, default=10, help="Monitoring interval in seconds")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--output_file", help="File to save the report")

    args = parser.parse_args()

    try:
        while True:
            info = collect_system_info()
            trigger_alerts(info)
            output_report(info, args.format, args.output_file)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
