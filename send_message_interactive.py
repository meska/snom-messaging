#!/usr/bin/env python3

"""
Example script for sending messages via the Snom DECT system.
This script provides a simple interface for sending messages.
"""

import logging
import os
import sys

from send_message import MessageSender

# Add the send_message module path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def send_simple_message():
    """
    Simple interface for sending a message.
    """
    print("=== Snom DECT Message Sending System ===\n")

    # Ask user for parameters
    to_ext = input("Enter recipient extension: ").strip()
    if not to_ext:
        print("❌ Recipient extension required!")
        return False

    message = input("Enter message to send: ").strip()
    if not message:
        print("❌ Message cannot be empty!")
        return False

    # Optional parameters
    from_name = input("Sender name (press Enter for 'System'): ").strip() or "System"
    server = input("Server address (press Enter for 'localhost'): ").strip() or "localhost"

    print("\n📤 Sending message...")
    print(f"   From: {from_name}")
    print(f"   To: {to_ext}")
    print(f"   Server: {server}")
    print(f"   Message: {message}\n")

    # Configure minimal logging
    logging.basicConfig(level=logging.WARNING)

    # Send the message
    sender = MessageSender(server)
    success, external_id, error = sender.send_message(to_ext, message, from_name=from_name)

    if success:
        print("✅ Message sent successfully!")
        print(f"   Message ID: {external_id}")
        return True
    else:
        print(f"❌ Send error: {error}")
        return False


def send_batch_messages():
    """
    Send multiple messages in batch.
    """
    print("=== Batch Message Sending ===\n")

    server = input("Server address (press Enter for 'localhost'): ").strip() or "localhost"
    from_name = input("Sender name (press Enter for 'System'): ").strip() or "System"

    print("\nEnter messages in format: extension,message")
    print("Press Enter with empty line to finish\n")

    messages = []
    while True:
        line = input("Message (ext,text): ").strip()
        if not line:
            break

        if "," not in line:
            print("❌ Invalid format. Use: extension,message")
            continue

        ext, msg = line.split(",", 1)
        messages.append((ext.strip(), msg.strip()))

    if not messages:
        print("❌ No messages to send!")
        return False

    print(f"\n📤 Sending {len(messages)} messages...")

    # Configure minimal logging
    logging.basicConfig(level=logging.WARNING)

    sender = MessageSender(server)
    success_count = 0

    for ext, msg in messages:
        print(f"   Sending to {ext}: {msg[:50]}{'...' if len(msg) > 50 else ''}")
        success, external_id, error = sender.send_message(ext, msg, from_name=from_name)

        if success:
            print(f"   ✅ Sent (ID: {external_id})")
            success_count += 1
        else:
            print(f"   ❌ Error: {error}")

    print(f"\n📊 Result: {success_count}/{len(messages)} messages sent successfully")
    return success_count == len(messages)


def main():
    """
    Main menu.
    """
    try:
        print("Select an option:")
        print("1. Send a single message")
        print("2. Send batch messages")
        print("3. Exit")

        choice = input("\nChoice (1-3): ").strip()

        if choice == "1":
            send_simple_message()
        elif choice == "2":
            send_batch_messages()
        elif choice == "3":
            print("👋 Goodbye!")
            return
        else:
            print("❌ Invalid choice!")

    except KeyboardInterrupt:
        print("\n\n👋 User interruption. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
