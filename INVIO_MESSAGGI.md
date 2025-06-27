# Script di Invio Messaggi Snom DECT

Questi script permettono di inviare messaggi a estensioni specifiche nel sistema Snom DECT.

## File creati

1. **`send_message.py`** - Script principale per l'invio di messaggi
2. **`send_message_interactive.py`** - Interfaccia interattiva semplificata

## Utilizzo

### 1. Script da riga di comando (`send_message.py`)

#### Uso base:

```bash
python send_message.py <estensione> "<messaggio>"
```

#### Esempi:

```bash
# Invio messaggio semplice
python send_message.py 101 "Ciao, questo è un messaggio di test"

# Invio con parametri personalizzati
python send_message.py 102 "Riunione alle 15:00" --from-name "Segreteria" --from-ext 100

# Invio a server remoto
python send_message.py 103 "Sistema in manutenzione" --server 192.168.1.100 --port 1300

# Debug attivato
python send_message.py 104 "Test debug" --debug
```

#### Opzioni disponibili:

-   `--from-ext`: Estensione mittente (default: "server")
-   `--from-name`: Nome mittente (default: "Sistema")
-   `--from-location`: Posizione mittente (default: "server")
-   `--server`: Indirizzo server (default: "localhost")
-   `--port`: Porta server (default: 1300)
-   `--debug`: Abilita output di debug

#### Aiuto:

```bash
python send_message.py --help
```

### 2. Script interattivo (`send_message_interactive.py`)

Avvia lo script per un'interfaccia guidata:

```bash
python send_message_interactive.py
```

Lo script offre due modalità:

1. **Invio singolo messaggio** - Interfaccia guidata per un messaggio
2. **Invio in batch** - Invio di più messaggi contemporaneamente

## Formato messaggi batch

Per l'invio in batch, usa il formato:

```
estensione,messaggio
```

Esempio:

```
101,Riunione alle 14:00
102,Chiamare il cliente
103,Sistema aggiornato
```

## Prerequisiti

-   Python 3.6+
-   Il server di messaggistica Snom deve essere in esecuzione
-   Connessione di rete al server (default: localhost:1300)

## Come funziona

Gli script creano messaggi XML nel formato richiesto dal sistema Snom DECT e li inviano tramite UDP. Il formato XML segue lo standard del sistema esistente:

-   Genera un ID esterno univoco per ogni messaggio
-   Include timestamp correnti
-   Usa il template XML compatibile con le BaseStations Snom
-   Invia via UDP alla porta 1300 (configurabile)

## Integrazione con il sistema esistente

Questi script sono compatibili con il sistema di messaggistica esistente (`messagesystem.py`) e possono essere utilizzati per:

-   Invio di notifiche automatiche
-   Messaggi di sistema
-   Alert di manutenzione
-   Comunicazioni broadcast
-   Integrazione con altri sistemi

## Logging

Lo script supporta diversi livelli di log:

-   **INFO**: Output normale con conferme di invio
-   **DEBUG**: Output dettagliato con contenuto XML dei messaggi
-   **WARNING**: Solo errori e avvisi

## Esempi di utilizzo pratico

### Notifica di manutenzione programmata

```bash
python send_message.py 101 "Manutenzione sistema dalle 02:00 alle 04:00" --from-name "IT Support"
```

### Alert urgente

```bash
python send_message.py 102 "URGENTE: Evacuazione edificio" --from-name "Sicurezza"
```

### Promemoria riunione

```bash
python send_message.py 103 "Riunione staff ore 15:00 sala conferenze" --from-name "Segreteria"
```

## Risoluzione problemi

### Messaggio non inviato

-   Verifica che il server di messaggistica sia attivo
-   Controlla l'indirizzo IP e la porta del server
-   Assicurati che l'estensione destinatario sia valida
-   Usa `--debug` per vedere i dettagli dell'errore

### Timeout di connessione

-   Verifica la connessione di rete
-   Controlla che la porta 1300 non sia bloccata da firewall
-   Prova con un server diverso se disponibile

### Estensione non trovata

-   Verifica che l'estensione sia registrata nel sistema
-   Controlla che il dispositivo sia online
-   Consulta i log del sistema principale per lo stato delle estensioni
