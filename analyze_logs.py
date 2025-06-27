#!/usr/bin/env python3

"""
Script per analizzare i messaggi XML salvati nei log.
Questo script aiuta a capire il formato corretto dei messaggi per il sistema Snom.
"""

import argparse
import glob
import json
import os
import xml.etree.ElementTree as ET


def analyze_xml_file(filepath):
    """
    Analizza un singolo file XML e estrae le informazioni chiave.

    Args:
        filepath: Percorso del file XML da analizzare

    Returns:
        Dictionary con le informazioni estratte
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Estrai i commenti di intestazione
        lines = content.split("\n")
        comments = [line for line in lines if line.startswith("<!--")]

        # Trova l'XML (salta i commenti)
        xml_start = None
        for i, line in enumerate(lines):
            if line.startswith("<?xml") or line.startswith("<request") or line.startswith("<response"):
                xml_start = i
                break

        if xml_start is None:
            return None

        xml_content = "\n".join(lines[xml_start:])
        xml_content = xml_content.strip()

        # Rimuovi il carattere null finale se presente
        if xml_content.endswith("\x00"):
            xml_content = xml_content[:-1]

        root = ET.fromstring(xml_content)

        # Estrai informazioni base
        info = {
            "filename": os.path.basename(filepath),
            "timestamp": lines[0].replace("<!-- Messaggio ricevuto il ", "").replace(" -->", "") if lines else "",
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
    Analizza tutti i file XML nella directory dei log.

    Args:
        logs_dir: Directory contenente i log

    Returns:
        Lista di dictionary con le informazioni estratte
    """
    if not os.path.exists(logs_dir):
        print(f"Directory {logs_dir} non trovata!")
        return []

    xml_files = glob.glob(os.path.join(logs_dir, "*.xml"))
    xml_files.sort()  # Ordina per nome (che include timestamp)

    results = []
    for filepath in xml_files:
        info = analyze_xml_file(filepath)
        if info:
            results.append(info)

    return results


def print_summary(results):
    """
    Stampa un riassunto dei risultati dell'analisi.
    """
    if not results:
        print("Nessun messaggio trovato nei log!")
        return

    print(f"\n📊 RIASSUNTO ANALISI LOG ({len(results)} messaggi trovati)")
    print("=" * 60)

    # Raggruppa per tipo
    by_type = {}
    for result in results:
        msg_type = result["type"]
        if msg_type not in by_type:
            by_type[msg_type] = []
        by_type[msg_type].append(result)

    print("\n📋 Messaggi per tipo:")
    for msg_type, messages in by_type.items():
        print(f"  • {msg_type}: {len(messages)} messaggi")

    print("\n📨 Messaggi con testo:")
    text_messages = [r for r in results if r["message_text"] and r["message_text"].strip()]
    for msg in text_messages:
        print(f"  • [{msg['type']}] {msg['from_ext']} → {msg['to_ext']}: '{msg['message_text']}'")

    print("\n🔄 Stati ricevuti:")
    status_messages = [r for r in results if r["status"]]
    for msg in status_messages:
        print(f"  • ID {msg['external_id']}: status {msg['status']}")


def print_detailed_analysis(results):
    """
    Stampa un'analisi dettagliata di ogni messaggio.
    """
    print("\n📝 ANALISI DETTAGLIATA")
    print("=" * 60)

    for i, result in enumerate(results, 1):
        print(f"\n[{i}] {result['filename']}")
        print(f"    Timestamp: {result['timestamp']}")
        print(f"    Tipo: {result['type']}")
        print(f"    Provenienza: {result['source']}")
        print(f"    XML Tag: {result['xml_tag']} {result['xml_attributes']}")
        print(f"    External ID: {result['external_id']}")

        if result["message_text"]:
            print(f"    Messaggio: '{result['message_text']}'")
        if result["from_ext"]:
            print(f"    Da: {result['from_ext']} ({result['from_name']})")
        if result["to_ext"]:
            print(f"    A: {result['to_ext']}")
        if result["status"]:
            print(f"    Status: {result['status']}")


def compare_message_formats(results):
    """
    Confronta i formati dei diversi tipi di messaggio.
    """
    print("\n🔍 CONFRONTO FORMATI MESSAGGI")
    print("=" * 60)

    # Raggruppa per combinazione tag/type
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
        print(f"❌ Errore nell'esportazione: {e}")


def main():
    """
    Funzione principale del script di analisi.
    """
    parser = argparse.ArgumentParser(description="Analizza i messaggi XML salvati nei log")
    parser.add_argument("--logs-dir", default="logs", help="Directory contenente i log (default: logs)")
    parser.add_argument("--detailed", action="store_true", help="Mostra analisi dettagliata")
    parser.add_argument("--export", help="Esporta risultati in JSON (specifica il nome file)")
    parser.add_argument("--format-compare", action="store_true", help="Confronta formati messaggi")

    args = parser.parse_args()

    print("🔍 Analisi Log Messaggi Snom DECT")
    print(f"Directory log: {args.logs_dir}")

    # Analizza i file
    results = analyze_logs_directory(args.logs_dir)

    # Mostra riassunto
    print_summary(results)

    # Confronto formati se richiesto
    if args.format_compare:
        compare_message_formats(results)

    # Analisi dettagliata se richiesta
    if args.detailed:
        print_detailed_analysis(results)

    # Esportazione se richiesta
    if args.export:
        export_to_json(results, args.export)

    print("\n✅ Analisi completata!")


if __name__ == "__main__":
    main()
