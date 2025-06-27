#!/usr/bin/env python3

import argparse
import logging
import random
import socket
import sys
import time
from datetime import datetime

logger = logging.getLogger(__name__)


class MessageSender:
    """
    Class for sending messages to specific extensions via the Snom DECT system.
    """

    def __init__(self, server_host="localhost", server_port=1300):
        """
        Initialize the sender with the UDP server address.

        Args:
            server_host: IP address of the message server (default: localhost)
            server_port: Port of the message server (default: 1300)
        """
        self.server_host = server_host
        self.server_port = server_port
        self.sock = None

    def create_message_xml(self, to_ext, message_text, from_ext="server", from_name="System", from_location="server"):
        """
        Creates the message XML in the format required by the Snom system.

        Args:
            to_ext: Recipient extension
            message_text: Message text
            from_ext: Sender extension (default: "server")
            from_name: Sender name (default: "System")
            from_location: Sender location (default: "server")

        Returns:
            Formatted XML string for sending
        """
        # Generate a unique 10-digit external ID
        external_id = f"{random.randrange(9999999999):010d}"

        # Get current timestamp
        now = datetime.now()
        datetime_str = now.strftime("%d.%m.%Y %H:%M:%S")
        timestamp_str = str(int(time.time()))

        # XML template for the message
        xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<request version="19.11.12.1403" type="job">
<externalid>{external_id}</externalid>
<systemdata>
<name>server</name>
<datetime>{datetime}</datetime>
<timestamp>{timestamp}</timestamp>
<status>1</status>
<statusinfo>System running</statusinfo>
</systemdata>
<jobdata>
<priority>0</priority>
<messages>
<message1></message1>
<message2></message2>
<messageuui>{message}</messageuui>
</messages>
<status>0</status>
<statusinfo></statusinfo>
</jobdata>
<senderdata>
<address>{from_ext}</address>
<name>{from_name}</name>
<location>{from_location}</location>
</senderdata>
<persondata>
<address>{to_ext}</address>
</persondata>
</request>
\0"""

        # Replace placeholders with actual values
        xml_message = xml_template.format(
            external_id=external_id,
            datetime=datetime_str,
            timestamp=timestamp_str,
            message=message_text,
            from_ext=from_ext,
            from_name=from_name,
            from_location=from_location,
            to_ext=to_ext,
        )

        return xml_message, external_id

    def send_message(self, to_ext, message_text, from_ext="server", from_name="System", from_location="server"):
        """
        Sends a message to a specific extension.

        Args:
            to_ext: Recipient extension
            message_text: Message text
            from_ext: Sender extension (default: "server")
            from_name: Sender name (default: "System")
            from_location: Sender location (default: "server")

        Returns:
            Tuple (success: bool, external_id: str, error_msg: str)
        """
        try:
            # Create UDP socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.settimeout(10)  # 10 second timeout

            # Create XML message
            xml_message, external_id = self.create_message_xml(to_ext, message_text, from_ext, from_name, from_location)

            logger.info(f"Sending message to extension {to_ext} with ID {external_id}")
            logger.debug(f"Message content:\n{xml_message}")

            # Send the message
            self.sock.sendto(xml_message.encode("utf-8"), (self.server_host, self.server_port))

            # Wait for response (optional, system might not respond immediately)
            try:
                response, addr = self.sock.recvfrom(4096)
                logger.debug(f"Received response from {addr}: {response.decode('utf-8', errors='ignore')}")
            except socket.timeout:
                logger.debug("No immediate response from server (normal)")

            return True, external_id, None

        except Exception as e:
            error_msg = f"Error sending message: {e}"
            logger.error(error_msg)
            return False, None, error_msg

        finally:
            if self.sock:
                self.sock.close()


def main():
    """
    Main function for command line usage.
    """
    parser = argparse.ArgumentParser(description="Send a message to a Snom DECT extension")
    parser.add_argument("to_ext", help="Recipient extension")
    parser.add_argument("message", help="Message text to send")
    parser.add_argument("--from-ext", default="server", help="Sender extension (default: server)")
    parser.add_argument("--from-name", default="System", help="Sender name (default: System)")
    parser.add_argument("--from-location", default="server", help="Sender location (default: server)")
    parser.add_argument("--server", default="localhost", help="Server address (default: localhost)")
    parser.add_argument("--port", type=int, default=1300, help="Server port (default: 1300)")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")

    args = parser.parse_args()

    # Configure logging
    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Create sender and send message
    sender = MessageSender(args.server, args.port)
    success, external_id, error = sender.send_message(args.to_ext, args.message, args.from_ext, args.from_name, args.from_location)

    if success:
        print("✅ Message sent successfully!")
        print(f"   Recipient: {args.to_ext}")
        print(f"   Message ID: {external_id}")
        print(f"   Text: {args.message}")
        sys.exit(0)
    else:
        print(f"❌ Error sending message: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
