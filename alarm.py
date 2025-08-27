import re
import time
import datetime
import threading
import os
import subprocess
import sys

# you can use this with speech recognition just add import speech and replace print with speak

class AlarmSystem:
    def __init__(self):
        self.alarms = []
        self.running = False
        
    def is_valid_time(self, s: str) -> bool:
        """Validate HH:MM time format."""
        m = re.match(r"^(\d{1,2}):(\d{2})$", s)
        if not m:
            return False
        h, m2 = int(m.group(1)), int(m.group(2))
        return 0 <= h <= 23 and 0 <= m2 <= 59
    
    def set_alarm(self, time_str: str):
        """Set an alarm for the specified time."""
        if not self.is_valid_time(time_str):
            print("Invalid time format. Use HH:MM (24-hour).")
            return
        
        # Save to file
        with open("Alarmtext.txt", "a", encoding="utf-8") as f:
            f.write(time_str + "\n")
        
        # Add to active alarms list
        self.alarms.append(time_str)
        print(f"Alarm set for {time_str}! I'll remind you at the right time.")
        
        # Start monitoring if not already running
        if not self.running:
            self.start_monitoring()
    
    def play_alarm_sound(self):
        """Play alarm sound based on the operating system."""
        system = sys.platform
        
        try:
            if system == "win32":
                # Windows
                import winsound
                # Play system beep
                for _ in range(5):
                    winsound.Beep(1000, 500)  # 1000Hz for 500ms
                    time.sleep(0.2)
            elif system == "darwin":
                # macOS
                subprocess.run(["afplay", "/System/Library/Sounds/Alarm.aiff"])
            else:
                # Linux
                subprocess.run(["paplay", "/usr/share/sounds/alsa/Front_Left.wav"])
        except Exception as e:
            # Fallback: print bell character (may produce system beep)
            for _ in range(10):
                print("\a", end="", flush=True)  # Bell character
                time.sleep(0.5)
    
    def show_notification(self, message):
        """Show desktop notification."""
        system = sys.platform
        
        try:
            if system == "win32":
                # Windows notification
                import win10toast
                #pip install win10toast (For Windows notifications (optional) or remove for no notifications)
                toaster = win10toast.ToastNotifier()
                toaster.show_toast("Alarm!", message, duration=10)
            elif system == "darwin":
                # macOS notification
                subprocess.run([
                    "osascript", "-e", 
                    f'display notification "{message}" with title "Alarm!"'
                ])
            else:
                # Linux notification
                subprocess.run(["notify-send", "Alarm!", message])
        except Exception as e:
            print(f"Could not show notification: {e}")
    
    def alarm_triggered(self, alarm_time):
        """Handle when an alarm is triggered."""
        current_time = datetime.datetime.now().strftime("%H:%M")
        message = f"ALARM! It's {current_time} - Time to wake up!"
        
        print("=" * 50)
        print(message)
        print("=" * 50)
        
        # Show notification
        self.show_notification(message)
        
        # Play sound
        self.play_alarm_sound()
        
        # Remove the triggered alarm
        if alarm_time in self.alarms:
            self.alarms.remove(alarm_time)
        
        # Update file
        self.update_alarm_file()
    
    def update_alarm_file(self):
        """Update the alarm file with remaining alarms."""
        with open("Alarmtext.txt", "w", encoding="utf-8") as f:
            for alarm in self.alarms:
                f.write(alarm + "\n")
    
    def load_alarms(self):
        """Load existing alarms from file."""
        try:
            with open("Alarmtext.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()
                self.alarms = [line.strip() for line in lines if line.strip() and self.is_valid_time(line.strip())]
        except FileNotFoundError:
            self.alarms = []
    
    def start_monitoring(self):
        """Start monitoring for alarms in a separate thread."""
        self.running = True
        monitor_thread = threading.Thread(target=self.monitor_alarms, daemon=True)
        monitor_thread.start()
        print("Alarm monitoring started...")
    
    def monitor_alarms(self):
        """Monitor alarms and trigger when time matches."""
        while self.running and self.alarms:
            current_time = datetime.datetime.now().strftime("%H:%M")
            
            # Check if any alarm matches current time
            triggered_alarms = [alarm for alarm in self.alarms if alarm == current_time]
            
            for alarm in triggered_alarms:
                self.alarm_triggered(alarm)
            
            # Sleep for 30 seconds to avoid constant checking
            time.sleep(30)
        
        self.running = False
    
    def list_alarms(self):
        """List all active alarms."""
        if not self.alarms:
            print("No active alarms.")
        else:
            print("Active alarms:")
            for i, alarm in enumerate(self.alarms, 1):
                print(f"{i}. {alarm}")
    
    def remove_alarm(self, time_str):
        """Remove a specific alarm."""
        if time_str in self.alarms:
            self.alarms.remove(time_str)
            self.update_alarm_file()
            print(f"Alarm for {time_str} removed.")
        else:
            print(f"No alarm found for {time_str}")
    
    def clear_all_alarms(self):
        """Clear all alarms."""
        self.alarms.clear()
        self.update_alarm_file()
        print("All alarms cleared.")

def main():
    alarm_system = AlarmSystem()
    alarm_system.load_alarms()
    
    # Start monitoring existing alarms
    if alarm_system.alarms:
        alarm_system.start_monitoring()
    
    while True:
        print("\n--- Alarm System ---")
        print("1. Set new alarm")
        print("2. List alarms")
        print("3. Remove alarm")
        print("4. Clear all alarms")
        print("5. Exit")
        
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            time_input = input("Enter time (HH:MM): ").strip()
            alarm_system.set_alarm(time_input)
        
        elif choice == "2":
            alarm_system.list_alarms()
        
        elif choice == "3":
            time_input = input("Enter time to remove (HH:MM): ").strip()
            alarm_system.remove_alarm(time_input)
        
        elif choice == "4":
            alarm_system.clear_all_alarms()
        
        elif choice == "5":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()



''' only for storing 
import re

def set_alarm(time_str: str):
    """Append a validated HH:MM time to Alarmtext.txt."""
    with open("Alarmtext.txt", "a", encoding="utf-8") as f:
        f.write(time_str + "\n")
    print("Alarm is set! I'll remind you at the right time.")

def is_valid_time(s: str) -> bool:
    m = re.match(r"^(\d{1,2}):(\d{2})$", s)
    if not m:
        return False
    h, m2 = int(m.group(1)), int(m.group(2))
    return 0 <= h <= 23 and 0 <= m2 <= 59

if __name__ == "__main__":
    query = input("Enter the time to set the alarm (in HH:MM format): ").strip()
    if not is_valid_time(query):
        print("Invalid time format. Use HH:MM (24-hour).")
    else:
        set_alarm(query) '''