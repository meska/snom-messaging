#!/usr/bin/env python3

"""
Script to monitor messaging server activity in real time.
Useful for debugging during tests with real phones.
"""

import os
import subprocess
import time


def monitor_server_logs():
    """
    Monitors server logs in real time showing only relevant lines.
    """
    print("🔍 Snom DECT Server Monitoring")
    print("Press Ctrl+C to exit")
    print("=" * 50)

    try:
        # Start server if not already running
        try:
            subprocess.run(["pgrep", "-f", "snom_messaging.py"], check=True, capture_output=True)
            print("✅ Server already running")
        except subprocess.CalledProcessError:
            print("🚀 Starting server...")
            server_process = subprocess.Popen(
                ["python3", "snom_messaging.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
            )
            time.sleep(2)

        # Monitor log files if they exist
        log_files = []
        if os.path.exists("logs"):
            print("📁 Monitoring logs/ folder")

        print("\n📊 Server Log:")
        print("-" * 30)

        # For now we simply monitor the output
        while True:
            time.sleep(1)

            # Here you could add log file monitoring
            # or other specific checks

    except KeyboardInterrupt:
        print("\n\n👋 Monitoring interrupted")
    except Exception as e:
        print(f"\n❌ Monitoring error: {e}")


def show_roaming_table():
    """
    Shows current roaming table status.
    """
    print("\n📋 To see current roaming table:")
    print("   1. Check server logs")
    print("   2. Wait for automatic print every 2 minutes")
    print("   3. Or send a message to trigger activity")


def show_test_instructions():
    """
    Shows instructions for testing with real phones.
    """
    print("\n🧪 REAL PHONE TESTING INSTRUCTIONS")
    print("=" * 40)
    print("1. 📱 Take phone with extension 106")
    print("2. 💬 Send message to extension 122")
    print("3. 👀 Watch logs to see:")
    print("   • Registration of 106 in roaming table")
    print("   • Message reception")
    print("   • Send attempt to 122")
    print("4. 📱 If 122 is not registered, take that phone too")
    print("5. 💬 Login or send message from 122")
    print("6. 🔄 Retry sending from 106 to 122")
    print("\n💡 Tip: Keep this monitoring open while testing!")


def main():
    """
    Main menu for monitoring.
    """
    while True:
        print("\n🎛️  SNOM DECT MONITORING")
        print("1. 🔍 Monitor server in real time")
        print("2. 📋 Show roaming table status")
        print("3. 🧪 Show test instructions")
        print("4. 📊 Analyze existing logs")
        print("5. 🚪 Exit")

        try:
            choice = input("\nChoice (1-5): ").strip()

            if choice == "1":
                monitor_server_logs()
            elif choice == "2":
                show_roaming_table()
            elif choice == "3":
                show_test_instructions()
            elif choice == "4":
                subprocess.run(["python3", "analyze_logs.py", "--detailed"])
            elif choice == "5":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice!")

        except KeyboardInterrupt:
            print("\n\n👋 User interruption")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
