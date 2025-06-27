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
    Classe per inviare messaggi a estensioni specifiche tramite il sistema Snom DECT.
    """

    def __init__(self, server_host="localhost", server_port=1300):
        """
        Inizializza il sender con l'indirizzo del server UDP.

        Args:
            server_host: Indirizzo IP del server messaggi (default: localhost)
            server_port: Porta del server messaggi (default: 1300)
        """
        self.server_host = server_host
        self.server_port = server_port
        self.sock = None

    def create_message_xml(self, to_ext, message_text, from_ext="server", from_name="Sistema", from_location="server"):
        """
        Crea l'XML del messaggio nel formato richiesto dal sistema Snom.

        Args:
            to_ext: Estensione destinatario
            message_text: Testo del messaggio
            from_ext: Estensione mittente (default: "server")
            from_name: Nome mittente (default: "Sistema")
            from_location: Posizione mittente (default: "server")

        Returns:
            String XML formattata per l'invio
        """
        # Genera un ID esterno univoco di 10 cifre
        external_id = f"{random.randrange(9999999999):010d}"

        # Ottieni timestamp corrente
        now = datetime.now()
        datetime_str = now.strftime("%d.%m.%Y %H:%M:%S")
        timestamp_str = str(int(time.time()))

        # Template XML per il messaggio
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

        # Sostituisci i placeholder con i valori effettivi
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

    def send_message(self, to_ext, message_text, from_ext="server", from_name="Sistema", from_location="server"):
        """
        Invia un messaggio a un'estensione specifica.

        Args:
            to_ext: Estensione destinatario
            message_text: Testo del messaggio
            from_ext: Estensione mittente (default: "server")
            from_name: Nome mittente (default: "Sistema")
            from_location: Posizione mittente (default: "server")

        Returns:
            Tuple (success: bool, external_id: str, error_msg: str)
        """
        try:
            # Crea il socket UDP
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.settimeout(10)  # Timeout di 10 secondi

            # Crea il messaggio XML
            xml_message, external_id = self.create_message_xml(to_ext, message_text, from_ext, from_name, from_location)

            logger.info(f"Invio messaggio a estensione {to_ext} con ID {external_id}")
            logger.debug(f"Contenuto messaggio:\n{xml_message}")

            # Invia il messaggio
            self.sock.sendto(xml_message.encode("utf-8"), (self.server_host, self.server_port))

            # Attendi una risposta (opzionale, il sistema potrebbe non rispondere immediatamente)
            try:
                response, addr = self.sock.recvfrom(4096)
                logger.debug(f"Ricevuta risposta da {addr}: {response.decode('utf-8', errors='ignore')}")
            except socket.timeout:
                logger.debug("Nessuna risposta immediata dal server (normale)")

            return True, external_id, None

        except Exception as e:
            error_msg = f"Errore nell'invio del messaggio: {e}"
            logger.error(error_msg)
            return False, None, error_msg

        finally:
            if self.sock:
                self.sock.close()


def main():
    """
    Funzione principale per l'utilizzo da riga di comando.
    """
    parser = argparse.ArgumentParser(description="Invia un messaggio a un'estensione Snom DECT")
    parser.add_argument("to_ext", help="Estensione destinatario")
    parser.add_argument("message", help="Testo del messaggio da inviare")
    parser.add_argument("--from-ext", default="server", help="Estensione mittente (default: server)")
    parser.add_argument("--from-name", default="Sistema", help="Nome mittente (default: Sistema)")
    parser.add_argument("--from-location", default="server", help="Posizione mittente (default: server)")
    parser.add_argument("--server", default="localhost", help="Indirizzo server (default: localhost)")
    parser.add_argument("--port", type=int, default=1300, help="Porta server (default: 1300)")
    parser.add_argument("--debug", action="store_true", help="Abilita output di debug")

    args = parser.parse_args()

    # Configura logging
    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Crea il sender e invia il messaggio
    sender = MessageSender(args.server, args.port)
    success, external_id, error = sender.send_message(args.to_ext, args.message, args.from_ext, args.from_name, args.from_location)

    if success:
        print("✅ Messaggio inviato con successo!")
        print(f"   Destinatario: {args.to_ext}")
        print(f"   ID Messaggio: {external_id}")
        print(f"   Testo: {args.message}")
        sys.exit(0)
    else:
        print(f"❌ Errore nell'invio del messaggio: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
