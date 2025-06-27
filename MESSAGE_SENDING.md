# Snom DECT Message Sending Scripts

These scripts allow sending messages to specific extensions in the Snom DECT system.

## Created Files

1. **`send_message.py`** - Main script for sending messages
2. **`send_message_interactive.py`** - Simplified interactive interface

## Usage

### 1. Command Line Script (`send_message.py`)

#### Basic usage:

```bash
python send_message.py <extension> "<message>"
```

#### Examples:

```bash
# Send simple message
python send_message.py 101 "Hello, this is a test message"

# Send with custom parameters
python send_message.py 102 "Meeting at 3:00 PM" --from-name "Secretary" --from-ext 100

# Send to remote server
python send_message.py 103 "System maintenance" --server 192.168.1.100 --port 1300

# Enable debug
python send_message.py 104 "Debug test" --debug
```

#### Available options:

-   `--from-ext`: Sender extension (default: "server")
-   `--from-name`: Sender name (default: "System")
-   `--from-location`: Sender location (default: "server")
-   `--server`: Server address (default: "localhost")
-   `--port`: Server port (default: 1300)
-   `--debug`: Enable debug output

#### Help:

```bash
python send_message.py --help
```

### 2. Interactive Script (`send_message_interactive.py`)

Start the script for a guided interface:

```bash
python send_message_interactive.py
```

The script offers two modes:

1. **Single message sending** - Guided interface for one message
2. **Batch sending** - Send multiple messages simultaneously

## Batch Message Format

For batch sending, use the format:

```
extension,message
```

Example:

```
101,Meeting at 2:00 PM
102,Call the client
103,System updated
```

## Prerequisites

-   Python 3.6+
-   Snom messaging server must be running
-   Network connection to server (default: localhost:1300)

## How It Works

The scripts create XML messages in the format required by the Snom DECT system and send them via UDP. The XML format follows the existing system standard:

-   Generates a unique external ID for each message
-   Includes current timestamps
-   Uses XML template compatible with Snom BaseStations
-   Sends via UDP to port 1300 (configurable)

## Integration with Existing System

These scripts are compatible with the existing messaging system (`messagesystem.py`) and can be used for:

-   Automatic notifications
-   System messages
-   Maintenance alerts
-   Broadcast communications
-   Integration with other systems

## Logging

The script supports different log levels:

-   **INFO**: Normal output with send confirmations
-   **DEBUG**: Detailed output with XML message content
-   **WARNING**: Only errors and warnings

## Practical Usage Examples

### Scheduled maintenance notification

```bash
python send_message.py 101 "System maintenance from 02:00 to 04:00" --from-name "IT Support"
```

### Urgent alert

```bash
python send_message.py 102 "URGENT: Building evacuation" --from-name "Security"
```

### Meeting reminder

```bash
python send_message.py 103 "Staff meeting 3:00 PM conference room" --from-name "Secretary"
```

## Troubleshooting

### Message not sent

-   Verify that the messaging server is active
-   Check the server IP address and port
-   Ensure the recipient extension is valid
-   Use `--debug` to see error details

### Connection timeout

-   Verify network connection
-   Check that port 1300 is not blocked by firewall
-   Try with a different server if available

### Extension not found

-   Verify that the extension is registered in the system
-   Check that the device is online
-   Consult the main system logs for extension status
