import os
import time
import requests
import smtplib
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.align import Align

CHECK_INTERVAL = 300  # Interval for IP check in seconds (5 minutes)
IP_CHECK_URLS = [
    "https://api.ipify.org?format=json",
    "https://api.myip.com",
    "https://checkip.amazonaws.com"
]
NOTIFICATION_EMAIL = {
    "enabled": True,
    "smtp_server": "smtp.example.com",
    "port": 587,
    "username": "user@example.com",
    "password": "secure_password",
    "from_addr": "user@example.com",
    "to_addr": "recipient@example.com"
}
ALERT_SOUND = {
    "enabled": True,
    "sound_path": "alert.wav"
}
COMMAND_EXECUTION = {
    "enabled": True,
    "command": "echo IP address has changed!"
}
LOG_FILE = 'ip_change_log.txt'

console = Console()

class IPMonitorGUI:
    def __init__(self):
        self.last_ip = None
        self.status_table = Table(title="IP Monitor Status")
        self.status_table.add_column("Last Known IP", justify="center")
        self.status_table.add_column("Current IP", justify="center")
        self.status_table.add_column("Notifications", justify="center")
        self.layout = Layout()
        self.layout.split(
            Layout(Panel(Align.center("External IP Monitor", vertical="middle"), title="Header"), size=3),
            Layout(name="content"),
        )
        self.layout["content"].update(self.status_table)

    def update_status(self, current_ip, notifications):
        self.status_table.rows.clear()
        self.status_table.add_row(self.last_ip or "Unknown", current_ip or "Checking...", notifications)

    def run(self):
        while True:
            current_ip = self.get_external_ip()
            notifications = "None"
            if current_ip and current_ip != self.last_ip:
                notifications = self.handle_notifications(current_ip)
                self.log_ip_change(self.last_ip, current_ip)
                self.last_ip = current_ip
            self.update_status(current_ip, notifications)
            time.sleep(CHECK_INTERVAL)

    def get_external_ip(self):
        for url in IP_CHECK_URLS:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                return response.json().get("ip")
            except requests.RequestException as e:
                console.print(f"[red]Error fetching external IP from {url}: {e}")
        return None

    def handle_notifications(self, new_ip):
        notifications = []

        if NOTIFICATION_EMAIL["enabled"]:
            try:
                self.send_email_notification(new_ip)
                notifications.append("Email Sent")
            except Exception as e:
                console.print(f"[red]Error sending email: {e}")

        if ALERT_SOUND["enabled"] and os.path.exists(ALERT_SOUND["sound_path"]):
            try:
                self.play_alert_sound()
                notifications.append("Sound Played")
            except Exception as e:
                console.print(f"[red]Error playing sound: {e}")

        if COMMAND_EXECUTION["enabled"]:
            try:
                self.execute_command()
                notifications.append("Command Executed")
            except Exception as e:
                console.print(f"[red]Error executing command: {e}")

        return ", ".join(notifications)

    def log_ip_change(self, old_ip, new_ip):
        with open(LOG_FILE, 'a') as log_file:
            log_file.write(f"IP changed from {old_ip} to {new_ip} at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    def send_email_notification(self, new_ip):
        msg = MIMEMultipart()
        msg["From"] = NOTIFICATION_EMAIL["from_addr"]
        msg["To"] = NOTIFICATION_EMAIL["to_addr"]
        msg["Subject"] = "Alert: External IP Changed"
        body = f"The external IP address has changed to: {new_ip}"
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(NOTIFICATION_EMAIL["smtp_server"], NOTIFICATION_EMAIL["port"]) as server:
            server.starttls()
            server.login(NOTIFICATION_EMAIL["username"], NOTIFICATION_EMAIL["password"])
            server.send_message(msg)

    def play_alert_sound(self):
        if os.name == "nt":
            subprocess.run(["powershell", "-c", f"(New-Object Media.SoundPlayer '{ALERT_SOUND['sound_path']}').PlaySync()"])
        else:
            subprocess.run(["aplay", ALERT_SOUND["sound_path"]], check=True)

    def execute_command(self):
        subprocess.run(COMMAND_EXECUTION["command"], shell=True, check=True)

if __name__ == "__main__":
    try:
        gui = IPMonitorGUI()
        gui.run()
    except KeyboardInterrupt:
        console.print("[yellow]Exiting IP Monitor.")
