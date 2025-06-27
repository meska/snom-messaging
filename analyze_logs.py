#!/usr/bin/env python3

"""
Script to analyze XML messages saved in logs.
This script helps understand the correct message format for the Snom system.
"""

import argparse
import glob
import json
import os
import xml.etree.ElementTree as ET


def analyze_xml_file(filepath):
    """
    Analyzes a single XML file and extracts key information.

    Args:
        filepath: Path of the XML file to analyze

    Returns:
        Dictionary with extracted information
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract header comments
        lines = content.split("\n")
        comments = [line for line in lines if line.startswith("<!--")]

        # Find the XML (skip comments)
        xml_start = None
        for i, line in enumerate(lines):
            if line.startswith("<?xml") or line.startswith("<request") or line.startswith("<response"):
                xml_start = i
                break

        if xml_start is None:
            return None

        xml_content = "\n".join(lines[xml_start:])
        xml_content = xml_content.strip()

        # Remove final null character if present
        if xml_content.endswith("\x00"):
            xml_content = xml_content[:-1]

        root = ET.fromstring(xml_content)

        # Estrai informazioni base
        info = {
            "filename": os.path.basename(filepath),
            "timestamp": lines[0].replace("<!-- Message received on ", "").replace(" -->", "") if lines else "",
            "source": lines[1].replace("<!-- Provenienza: ", "").replace(" -->", "") if len(lines) > 1 else "",
            "type": lines[2].replace("<!-- Tipo: ", "").replace(" -->", "") if len(lines) > 2 else "",
            "xml_tag": root.tag,
            "xml_attributes": root.attrib,
            "external_id": None,
            "message_text": None,
            "from_ext": None,
            "to_ext": None,
            "from_name": None,
            "status": None,
            "datetime": None,
            "timestamp_unix": None,
        }

        # Estrai informazioni specifiche dal contenuto XML
        if root.find("./externalid") is not None:
            info["external_id"] = root.find("./externalid").text

        if root.find("./jobdata/messages/messageuui") is not None:
            info["message_text"] = root.find("./jobdata/messages/messageuui").text

        if root.find("./senderdata/address") is not None:
            info["from_ext"] = root.find("./senderdata/address").text

        if root.find("./persondata/address") is not None:
            info["to_ext"] = root.find("./persondata/address").text

        if root.find("./senderdata/name") is not None:
            info["from_name"] = root.find("./senderdata/name").text

        if root.find("./jobdata/status") is not None:
            info["status"] = root.find("./jobdata/status").text

        if root.find("./systemdata/datetime") is not None:
            info["datetime"] = root.find("./systemdata/datetime").text

        if root.find("./systemdata/timestamp") is not None:
            info["timestamp_unix"] = root.find("./systemdata/timestamp").text

        return info

    except Exception as e:
        print(f"Errore nell'analisi di {filepath}: {e}")
        return None


def analyze_logs_directory(logs_dir="logs"):
    """
    Analyzes all XML files in the logs directory.

    Args:
        logs_dir: Directory containing the logs

    Returns:
        List of dictionaries with extracted information
    """
    if not os.path.exists(logs_dir):
        print(f"Directory {logs_dir} not found!")
        return []

    xml_files = glob.glob(os.path.join(logs_dir, "*.xml"))
    xml_files.sort()  # Sort by name (which includes timestamp)

    results = []
    for filepath in xml_files:
        info = analyze_xml_file(filepath)
        if info:
            results.append(info)

    return results


def print_summary(results):
    """
    Prints a summary of the analysis results.
    """
    if not results:
        print("No messages found in logs!")
        return

    print(f"\n📊 LOG ANALYSIS SUMMARY ({len(results)} messages found)")
    print("=" * 60)

    # Group by type
    by_type = {}
    for result in results:
        msg_type = result["type"]
        if msg_type not in by_type:
            by_type[msg_type] = []
        by_type[msg_type].append(result)

    print("\n📋 Messages by type:")
    for msg_type, messages in by_type.items():
        print(f"  • {msg_type}: {len(messages)} messages")

    print("\n📨 Messages with text:")
    text_messages = [r for r in results if r["message_text"] and r["message_text"].strip()]
    for msg in text_messages:
        print(f"  • [{msg['type']}] {msg['from_ext']} → {msg['to_ext']}: '{msg['message_text']}'")

    print("\n🔄 Received statuses:")
    status_messages = [r for r in results if r["status"]]
    for msg in status_messages:
        print(f"  • ID {msg['external_id']}: status {msg['status']}")


def print_detailed_analysis(results):
    """
    Prints a detailed analysis of each message.
    """
    print("\n📝 DETAILED ANALYSIS")
    print("=" * 60)

    for i, result in enumerate(results, 1):
        print(f"\n[{i}] {result['filename']}")
        print(f"    Timestamp: {result['timestamp']}")
        print(f"    Type: {result['type']}")
        print(f"    Source: {result['source']}")
        print(f"    XML Tag: {result['xml_tag']} {result['xml_attributes']}")
        print(f"    External ID: {result['external_id']}")

        if result["message_text"]:
            print(f"    Message: '{result['message_text']}'")
        if result["from_ext"]:
            print(f"    From: {result['from_ext']} ({result['from_name']})")
        if result["to_ext"]:
            print(f"    To: {result['to_ext']}")
        if result["status"]:
            print(f"    Status: {result['status']}")


def compare_message_formats(results):
    """
    Compares formats of different message types.
    """
    print("\n🔍 MESSAGE FORMAT COMPARISON")
    print("=" * 60)

    # Group by tag/type combination
    formats = {}
    for result in results:
        key = f"{result['xml_tag']}-{result['xml_attributes'].get('type', 'unknown')}"
        if key not in formats:
            formats[key] = []
        formats[key].append(result)

    for format_key, messages in formats.items():
        print(f"\n📋 Formato: {format_key} ({len(messages)} messaggi)")

        # Trova un esempio rappresentativo
        example = messages[0]

        print("    Struttura XML comune:")
        if example["external_id"]:
            print("      • externalid: presente")
        if example["message_text"] is not None:
            print(f"      • messageuui: {'presente' if example['message_text'] else 'vuoto'}")
        if example["from_ext"]:
            print("      • senderdata/address: presente")
        if example["to_ext"]:
            print("      • persondata/address: presente")
        if example["status"]:
            print("      • jobdata/status: presente")


def export_to_json(results, output_file="message_analysis.json"):
    """
    Esporta i risultati in formato JSON per ulteriori analisi.
    """
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Risultati esportati in: {output_file}")
    except Exception as e:
        print(f"❌ Export error: {e}")


def main():
    """
    Main function of the analysis script.
    """
    parser = argparse.ArgumentParser(description="Analyze XML messages saved in logs")
    parser.add_argument("--logs-dir", default="logs", help="Directory containing logs (default: logs)")
    parser.add_argument("--detailed", action="store_true", help="Show detailed analysis")
    parser.add_argument("--export", help="Export results to JSON (specify filename)")
    parser.add_argument("--format-compare", action="store_true", help="Compare message formats")

    args = parser.parse_args()

    print("🔍 Snom DECT Message Log Analysis")
    print(f"Log directory: {args.logs_dir}")

    # Analyze files
    results = analyze_logs_directory(args.logs_dir)

    # Show summary
    print_summary(results)

    # Format comparison if requested
    if args.format_compare:
        compare_message_formats(results)

    # Detailed analysis if requested
    if args.detailed:
        print_detailed_analysis(results)

    # Export if requested
    if args.export:
        export_to_json(results, args.export)

    print("\n✅ Analysis completed!")


if __name__ == "__main__":
    main()
