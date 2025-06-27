#!/usr/bin/env python3

"""
Example of programmatic usage of MessageSender.
This script shows how to integrate message sending into other applications.
"""

import logging
import time

from send_message import MessageSender


def system_notifications_example():
    """
    Example: Sending automatic system notifications.
    """
    print("=== Example: System Notifications ===")

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Create the sender
    sender = MessageSender("localhost", 1300)

    # List of extensions to notify
    extensions = ["101", "102", "103"]

    # Scheduled maintenance message
    message = "Server maintenance scheduled for 02:00. Estimated duration: 2 hours."

    print(f"Sending notification to {len(extensions)} extensions...")

    successes = 0
    for ext in extensions:
        success, msg_id, error = sender.send_message(
            to_ext=ext, message_text=message, from_name="IT System", from_ext="support", from_location="server"
        )

        if success:
            print(f"✅ Notification sent to {ext} (ID: {msg_id})")
            successes += 1
        else:
            print(f"❌ Send error to {ext}: {error}")

        # Pause between sends to avoid system overload
        time.sleep(0.5)

    print(f"\nResult: {successes}/{len(extensions)} notifications sent")
    return successes == len(extensions)


def urgent_alert_example():
    """
    Example: Sending urgent alert to all extensions.
    """
    print("\n=== Example: Urgent Alert ===")

    sender = MessageSender()

    # Emergency alert
    alert_msg = "ATTENTION: Immediate building evacuation. Follow safety procedures."

    # Emergency extension list
    emergency_extensions = ["100", "101", "102", "103", "104", "105"]

    print("🚨 Sending emergency alert...")

    for ext in emergency_extensions:
        success, msg_id, error = sender.send_message(
            to_ext=ext, message_text=alert_msg, from_name="SECURITY", from_ext="911", from_location="central"
        )

        if success:
            print(f"🚨 Alert sent to {ext}")
        else:
            print(f"❌ CRITICAL ERROR: unable to send alert to {ext}")


def custom_reminders_example():
    """
    Example: Sending custom reminders.
    """
    print("\n=== Example: Custom Reminders ===")

    sender = MessageSender()

    # Dictionary with custom reminders
    reminders = {
        "101": "Client meeting at 2:30 PM - Room A",
        "102": "Report deadline today by 5:00 PM",
        "103": "Call supplier for material order",
        "104": "Safety check at 4:00 PM",
    }

    print("📅 Sending custom reminders...")

    for ext, message in reminders.items():
        success, msg_id, error = sender.send_message(to_ext=ext, message_text=f"REMINDER: {message}", from_name="Secretary", from_ext="200")

        if success:
            print(f"📅 Reminder sent to {ext}")
        else:
            print(f"❌ Error sending reminder to {ext}: {error}")

        time.sleep(0.3)


def system_status_example():
    """
    Example: System status notification.
    """
    print("\n=== Example: System Status ===")

    sender = MessageSender()

    # Simulate system status check
    import random

    cpu_usage = random.randint(20, 80)
    disk_space = random.randint(60, 95)

    if cpu_usage > 75 or disk_space > 90:
        # Alert administrators
        admin_exts = ["100", "101"]
        alert_msg = f"SYSTEM WARNING: CPU {cpu_usage}%, Disk {disk_space}% full"

        for ext in admin_exts:
            success, msg_id, error = sender.send_message(to_ext=ext, message_text=alert_msg, from_name="System Monitor", from_ext="system")

            if success:
                print(f"⚠️  System alert sent to admin {ext}")
    else:
        # Notify normal status
        success, msg_id, error = sender.send_message(
            to_ext="100", message_text=f"System OK: CPU {cpu_usage}%, Disk {disk_space}%", from_name="System Monitor", from_ext="system"
        )

        if success:
            print("✅ Normal system status notified")


def main():
    """
    Runs all examples.
    """
    print("🚀 MessageSender Usage Examples\n")

    try:
        # Run examples
        system_notifications_example()
        urgent_alert_example()
        custom_reminders_example()
        system_status_example()

        print("\n✅ All examples completed!")

    except KeyboardInterrupt:
        print("\n\n👋 User interruption")
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")


if __name__ == "__main__":
    main()
