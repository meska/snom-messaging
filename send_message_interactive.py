#!/usr/bin/env python3

"""
Script di esempio per inviare messaggi tramite il sistema Snom DECT.
Questo script fornisce un'interfaccia semplice per l'invio di messaggi.
"""

import logging
import os
import sys

from send_message import MessageSender

# Aggiungi il percorso del modulo send_message
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def send_simple_message():
    """
    Interfaccia semplice per inviare un messaggio.
    """
    print("=== Sistema di Invio Messaggi Snom DECT ===\n")

    # Chiedi i parametri all'utente
    to_ext = input("Inserisci l'estensione destinatario: ").strip()
    if not to_ext:
        print("❌ Estensione destinatario obbligatoria!")
        return False

    message = input("Inserisci il messaggio da inviare: ").strip()
    if not message:
        print("❌ Il messaggio non può essere vuoto!")
        return False

    # Parametri opzionali
    from_name = input("Nome mittente (premi Invio per 'Sistema'): ").strip() or "Sistema"
    server = input("Indirizzo server (premi Invio per 'localhost'): ").strip() or "localhost"

    print("\n📤 Invio messaggio...")
    print(f"   Da: {from_name}")
    print(f"   A: {to_ext}")
    print(f"   Server: {server}")
    print(f"   Messaggio: {message}\n")

    # Configura logging minimale
    logging.basicConfig(level=logging.WARNING)

    # Invia il messaggio
    sender = MessageSender(server)
    success, external_id, error = sender.send_message(to_ext, message, from_name=from_name)

    if success:
        print("✅ Messaggio inviato con successo!")
        print(f"   ID Messaggio: {external_id}")
        return True
    else:
        print(f"❌ Errore nell'invio: {error}")
        return False


def send_batch_messages():
    """
    Invia più messaggi in batch.
    """
    print("=== Invio Messaggi in Batch ===\n")

    server = input("Indirizzo server (premi Invio per 'localhost'): ").strip() or "localhost"
    from_name = input("Nome mittente (premi Invio per 'Sistema'): ").strip() or "Sistema"

    print("\nInserisci i messaggi nel formato: estensione,messaggio")
    print("Premi Invio con una riga vuota per terminare\n")

    messages = []
    while True:
        line = input("Messaggio (ext,testo): ").strip()
        if not line:
            break

        if "," not in line:
            print("❌ Formato non valido. Usa: estensione,messaggio")
            continue

        ext, msg = line.split(",", 1)
        messages.append((ext.strip(), msg.strip()))

    if not messages:
        print("❌ Nessun messaggio da inviare!")
        return False

    print(f"\n📤 Invio {len(messages)} messaggi...")

    # Configura logging minimale
    logging.basicConfig(level=logging.WARNING)

    sender = MessageSender(server)
    success_count = 0

    for ext, msg in messages:
        print(f"   Invio a {ext}: {msg[:50]}{'...' if len(msg) > 50 else ''}")
        success, external_id, error = sender.send_message(ext, msg, from_name=from_name)

        if success:
            print(f"   ✅ Inviato (ID: {external_id})")
            success_count += 1
        else:
            print(f"   ❌ Errore: {error}")

    print(f"\n📊 Risultato: {success_count}/{len(messages)} messaggi inviati con successo")
    return success_count == len(messages)


def main():
    """
    Menu principale.
    """
    try:
        print("Seleziona un'opzione:")
        print("1. Invia un singolo messaggio")
        print("2. Invia messaggi in batch")
        print("3. Esci")

        choice = input("\nScelta (1-3): ").strip()

        if choice == "1":
            send_simple_message()
        elif choice == "2":
            send_batch_messages()
        elif choice == "3":
            print("👋 Arrivederci!")
            return
        else:
            print("❌ Scelta non valida!")

    except KeyboardInterrupt:
        print("\n\n👋 Interruzione utente. Arrivederci!")
    except Exception as e:
        print(f"\n❌ Errore inaspettato: {e}")


if __name__ == "__main__":
    main()
