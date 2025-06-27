#!/usr/bin/env python3

"""
Esempio di utilizzo programmatico del MessageSender.
Questo script mostra come integrare l'invio di messaggi in altre applicazioni.
"""

import logging
import time

from send_message import MessageSender


def esempio_notifiche_sistema():
    """
    Esempio: Invio di notifiche di sistema automatiche.
    """
    print("=== Esempio: Notifiche di Sistema ===")

    # Configura logging
    logging.basicConfig(level=logging.INFO)

    # Crea il sender
    sender = MessageSender("localhost", 1300)

    # Lista di estensioni da notificare
    estensioni = ["101", "102", "103"]

    # Messaggio di manutenzione programmata
    messaggio = "Manutenzione server programmata per le 02:00. Durata stimata: 2 ore."

    print(f"Invio notifica a {len(estensioni)} estensioni...")

    successi = 0
    for ext in estensioni:
        success, msg_id, error = sender.send_message(
            to_ext=ext, message_text=messaggio, from_name="Sistema IT", from_ext="support", from_location="server"
        )

        if success:
            print(f"✅ Notifica inviata a {ext} (ID: {msg_id})")
            successi += 1
        else:
            print(f"❌ Errore invio a {ext}: {error}")

        # Pausa tra invii per non sovraccaricare il sistema
        time.sleep(0.5)

    print(f"\nRisultato: {successi}/{len(estensioni)} notifiche inviate")
    return successi == len(estensioni)


def esempio_alert_urgente():
    """
    Esempio: Invio di un alert urgente a tutte le estensioni.
    """
    print("\n=== Esempio: Alert Urgente ===")

    sender = MessageSender()

    # Alert di emergenza
    alert_msg = "ATTENZIONE: Evacuazione immediata dell'edificio. Seguire le procedure di sicurezza."

    # Lista delle estensioni di emergenza
    estensioni_emergenza = ["100", "101", "102", "103", "104", "105"]

    print("🚨 Invio alert di emergenza...")

    for ext in estensioni_emergenza:
        success, msg_id, error = sender.send_message(
            to_ext=ext, message_text=alert_msg, from_name="SICUREZZA", from_ext="911", from_location="centrale"
        )

        if success:
            print(f"🚨 Alert inviato a {ext}")
        else:
            print(f"❌ ERRORE CRITICO: impossibile inviare alert a {ext}")


def esempio_promemoria_personalizzati():
    """
    Esempio: Invio di promemoria personalizzati.
    """
    print("\n=== Esempio: Promemoria Personalizzati ===")

    sender = MessageSender()

    # Dizionario con promemoria personalizzati
    promemoria = {
        "101": "Riunione con cliente ore 14:30 - Sala A",
        "102": "Scadenza report entro oggi alle 17:00",
        "103": "Chiamare fornitore per ordine materiali",
        "104": "Controllo sicurezza impianti ore 16:00",
    }

    print("📅 Invio promemoria personalizzati...")

    for ext, messaggio in promemoria.items():
        success, msg_id, error = sender.send_message(to_ext=ext, message_text=f"PROMEMORIA: {messaggio}", from_name="Segreteria", from_ext="200")

        if success:
            print(f"📅 Promemoria inviato a {ext}")
        else:
            print(f"❌ Errore invio promemoria a {ext}: {error}")

        time.sleep(0.3)


def esempio_stato_sistema():
    """
    Esempio: Notifica dello stato del sistema.
    """
    print("\n=== Esempio: Stato Sistema ===")

    sender = MessageSender()

    # Simula controllo stato sistema
    import random

    cpu_usage = random.randint(20, 80)
    disk_space = random.randint(60, 95)

    if cpu_usage > 75 or disk_space > 90:
        # Alert amministratori
        admin_exts = ["100", "101"]
        alert_msg = f"ATTENZIONE SISTEMA: CPU {cpu_usage}%, Disco {disk_space}% pieno"

        for ext in admin_exts:
            success, msg_id, error = sender.send_message(to_ext=ext, message_text=alert_msg, from_name="Monitor Sistema", from_ext="system")

            if success:
                print(f"⚠️  Alert sistema inviato a admin {ext}")
    else:
        # Notifica stato normale
        success, msg_id, error = sender.send_message(
            to_ext="100", message_text=f"Sistema OK: CPU {cpu_usage}%, Disco {disk_space}%", from_name="Monitor Sistema", from_ext="system"
        )

        if success:
            print("✅ Stato sistema normale notificato")


def main():
    """
    Esegue tutti gli esempi.
    """
    print("🚀 Esempi di utilizzo del MessageSender\n")

    try:
        # Esegui gli esempi
        esempio_notifiche_sistema()
        esempio_alert_urgente()
        esempio_promemoria_personalizzati()
        esempio_stato_sistema()

        print("\n✅ Tutti gli esempi completati!")

    except KeyboardInterrupt:
        print("\n\n👋 Interruzione utente")
    except Exception as e:
        print(f"\n❌ Errore durante l'esecuzione: {e}")


if __name__ == "__main__":
    main()
