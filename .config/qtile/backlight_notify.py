import subprocess
from gi.repository import Notify, GLib

# Initialize the notification system
Notify.init("Brightness Notification")

# Create a persistent notification object
brightness_notification = Notify.Notification.new("Brightness", "")

def notify_brightness():
    # Get current brightness
    result = subprocess.run(["brightnessctl", "get"], stdout=subprocess.PIPE)
    current_brightness = int(result.stdout.decode().strip())

    # Get max brightness
    result = subprocess.run(["brightnessctl", "max"], stdout=subprocess.PIPE)
    max_brightness = int(result.stdout.decode().strip())

    # Calculate percentage
    brightness_percentage = (current_brightness / max_brightness) * 100

    # Update the notification content
    brightness_notification.update(f"Brightness: {brightness_percentage:.0f}%")
    brightness_notification.set_hint("value", GLib.Variant('i', int(brightness_percentage)))

    # Show the notification
    brightness_notification.show()
