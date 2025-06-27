#!/usr/bin/env python3

"""
Script per monitorare in tempo reale l'attività del server di messaggistica.
Utile per debugging durante i test con telefoni reali.
"""

import os
import subprocess
import time


def monitor_server_logs():
    """
    Monitora i log del server in tempo reale mostrando solo le righe rilevanti.
    """
    print("🔍 Monitoraggio Server Snom DECT")
    print("Premere Ctrl+C per uscire")
    print("=" * 50)

    try:
        # Avvia il server se non è già in esecuzione
        try:
            subprocess.run(["pgrep", "-f", "snom_messaging.py"], check=True, capture_output=True)
            print("✅ Server già in esecuzione")
        except subprocess.CalledProcessError:
            print("🚀 Avvio server...")
            server_process = subprocess.Popen(
                ["python3", "snom_messaging.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
            )
            time.sleep(2)

        # Monitora i file di log se esistono
        log_files = []
        if os.path.exists("logs"):
            print("📁 Monitoraggio cartella logs/")

        print("\n📊 Log Server:")
        print("-" * 30)

        # Per ora monitoriamo semplicemente l'output
        while True:
            time.sleep(1)

            # Qui potresti aggiungere monitoring dei file log
            # o altri controlli specifici

    except KeyboardInterrupt:
        print("\n\n👋 Monitoring interrotto")
    except Exception as e:
        print(f"\n❌ Errore nel monitoring: {e}")


def show_roaming_table():
    """
    Mostra lo stato attuale della roaming table.
    """
    print("\n📋 Per vedere la roaming table corrente:")
    print("   1. Controlla i log del server")
    print("   2. Aspetta il print automatico ogni 2 minuti")
    print("   3. O invia un messaggio per triggerare activity")


def show_test_instructions():
    """
    Mostra le istruzioni per il test con telefoni reali.
    """
    print("\n🧪 ISTRUZIONI TEST TELEFONI REALI")
    print("=" * 40)
    print("1. 📱 Prendi il telefono con estensione 106")
    print("2. 💬 Invia un messaggio all'estensione 122")
    print("3. 👀 Osserva i log per vedere:")
    print("   • Registrazione di 106 nella roaming table")
    print("   • Ricezione del messaggio")
    print("   • Tentativo di invio a 122")
    print("4. 📱 Se 122 non è registrato, prendi anche quel telefono")
    print("5. 💬 Fai il login o invia un messaggio da 122")
    print("6. 🔄 Riprova l'invio da 106 a 122")
    print("\n💡 Suggerimento: Tieni aperto questo monitoring mentre fai i test!")


def main():
    """
    Menu principale per il monitoring.
    """
    while True:
        print("\n🎛️  MONITORING SNOM DECT")
        print("1. 🔍 Monitora server in tempo reale")
        print("2. 📋 Mostra stato roaming table")
        print("3. 🧪 Mostra istruzioni test")
        print("4. 📊 Analizza log esistenti")
        print("5. 🚪 Esci")

        try:
            choice = input("\nScelta (1-5): ").strip()

            if choice == "1":
                monitor_server_logs()
            elif choice == "2":
                show_roaming_table()
            elif choice == "3":
                show_test_instructions()
            elif choice == "4":
                subprocess.run(["python3", "analyze_logs.py", "--detailed"])
            elif choice == "5":
                print("👋 Arrivederci!")
                break
            else:
                print("❌ Scelta non valida!")

        except KeyboardInterrupt:
            print("\n\n👋 Interruzione utente")
            break
        except Exception as e:
            print(f"\n❌ Errore: {e}")


if __name__ == "__main__":
    main()
