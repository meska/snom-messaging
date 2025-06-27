# Snom DECT Message Analysis - XML Format

Based on real system log analysis, here are the XML formats used by the Snom DECT system.

## `request` Type Messages (Incoming/Outgoing Messages)

### Basic Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<request version="19.11.12.1403" type="job">
<externalid>1234567890</externalid>
<systemdata>
<n>server</n>
<datetime>27.06.2025 17:08:41</datetime>
<timestamp>1751036921</timestamp>
<status>1</status>
<statusinfo>System running</statusinfo>
</systemdata>
<jobdata>
<priority>0</priority>
<messages>
<message1></message1>
<message2></message2>
<messageuui>Message text here</messageuui>
</messages>
<status>0</status>
<statusinfo></statusinfo>
</jobdata>
<senderdata>
<address>sender_extension</address>
<n>Sender Name</n>
<location>sender_location</location>
</senderdata>
<persondata>
<address>recipient_extension</address>
</persondata>
</request>
```

### Key Fields

#### `<externalid>`

-   Unique message ID (10 digits)
-   Used for tracking and confirmations

#### `<systemdata>`

-   `<n>`: Always "server"
-   `<datetime>`: Format DD.MM.YYYY HH:MM:SS
-   `<timestamp>`: Unix timestamp
-   `<status>`: Always "1" (system active)

#### `<jobdata>`

-   `<priority>`: Always "0"
-   `<messageuui>`: **Text message content**
-   `<status>`:
    -   "0" = message pending/not sent
    -   "1" = message delivered

#### `<senderdata>` (Sender)

-   `<address>`: Sender extension
-   `<n>`: Sender name
-   `<location>`: Sender location

#### `<persondata>` (Recipient)

-   `<address>`: Recipient extension

## `response` Type Messages (Delivery Confirmations)

### Basic Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<response version="19.11.12.1403" type="job">
<externalid>1234567890</externalid>
<systemdata>
<n>server</n>
<datetime>27.06.2025 17:08:41</datetime>
<timestamp>1751036921</timestamp>
<status>1</status>
<statusinfo>System running</statusinfo>
</systemdata>
<jobdata>
<priority>0</priority>
<messages>
<message1></message1>
<message2></message2>
<messageuui></messageuui>
</messages>
<status>1</status>
<statusinfo></statusinfo>
</jobdata>
<senderdata>
<address>confirming_extension</address>
<n>name</n>
<location>server</location>
</senderdata>
<persondata>
<address>original_extension</address>
<n>Original Name</n>
<location>original_location</location>
</persondata>
</response>
```

### Response Characteristics

1. **`<messageuui>` is empty** - Confirmations contain no text
2. **`<status>` in jobdata** = "1" (message received)
3. **Senderdata and persondata are swapped** compared to original message

## Observed Message Types

### 1. Messages from Our Script → System

-   **Tag**: `request`
-   **Type**: `job`
-   **Status jobdata**: `0` (pending send)
-   **Sender**: `server` / `System`
-   **Characteristics**: Messages sent via our script

### 2. Messages from Real Devices → System

-   **Tag**: `request`
-   **Type**: `job`
-   **Status jobdata**: `0` (received, pending forward)
-   **Sender**: Real extension (e.g. `106`)
-   **Characteristics**: Messages from physical phones

### 3. Delivery Confirmations (System → Sender)

-   **Tag**: `response`
-   **Type**: `job`
-   **Status jobdata**: `1` (confirmed)
-   **Characteristics**: Automatic confirmations sent by system

## Identified Issues

### 1. Empty Roaming Table

**Problem**: `extension not found in roaming table`
**Cause**: Extensions are not registered in the roaming system
**Solution**: Devices must register by sending system messages or login

### 2. Name Tag Format

**Observation**: `<n>` tags sometimes appear truncated in logs
**Cause**: Possible truncation or system parsing
**Impact**: Does not seem to affect functionality

## Sending Recommendations

### send_message.py Script

Our script generates the correct format, but for effective sending:

1. **Target Extensions**: Ensure they exist in the system
2. **Roaming**: Devices must be online and registered
3. **Monitoring**: Use logs to verify sending

### Optimal Template Format

Based on real logs, the template in our script is correct:

-   XML Version: `19.11.12.1403`
-   Type: `job`
-   Status systemdata: `1`
-   Status jobdata: `0` (for new messages)
-   Priority: `0`

## Debugging

### Log Checking

```bash
# Complete analysis
python3 analyze_logs.py --detailed --format-compare

# Summary only
python3 analyze_logs.py

# Export to JSON
python3 analyze_logs.py --export results.json
```

### Roaming Table Verification

Devices must appear in logs with message types:

-   `systeminfo` - Location updates
-   `login` - Login/logout events

### Send Testing

```bash
# Basic test
python3 send_message.py 106 "Test message"

# With debug
python3 send_message.py 106 "Test message" --debug

# Check logs after sending
ls -la logs/
python3 analyze_logs.py
```
