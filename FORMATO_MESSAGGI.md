# Analisi dei Messaggi Snom DECT - Formato XML

Basato sull'analisi dei log reali del sistema, ecco i formati XML utilizzati dal sistema Snom DECT.

## Messaggi di Tipo `request` (Messaggi in arrivo/uscita)

### Struttura Base

```xml
<?xml version="1.0" encoding="UTF-8"?>
<request version="19.11.12.1403" type="job">
<externalid>1234567890</externalid>
<systemdata>
<name>server</name>
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
<messageuui>Testo del messaggio qui</messageuui>
</messages>
<status>0</status>
<statusinfo></statusinfo>
</jobdata>
<senderdata>
<address>estensione_mittente</address>
<name>Nome Mittente</name>
<location>location_mittente</location>
</senderdata>
<persondata>
<address>estensione_destinatario</address>
</persondata>
</request>
```

### Campi Chiave

#### `<externalid>`

-   ID univoco del messaggio (10 cifre)
-   Usato per tracking e conferme

#### `<systemdata>`

-   `<name>`: Sempre "server"
-   `<datetime>`: Formato DD.MM.YYYY HH:MM:SS
-   `<timestamp>`: Unix timestamp
-   `<status>`: Sempre "1" (sistema attivo)

#### `<jobdata>`

-   `<priority>`: Sempre "0"
-   `<messageuui>`: **Contenuto del messaggio di testo**
-   `<status>`:
    -   "0" = messaggio in attesa/non inviato
    -   "1" = messaggio consegnato

#### `<senderdata>` (Mittente)

-   `<address>`: Estensione mittente
-   `<name>`: Nome del mittente
-   `<location>`: Posizione del mittente

#### `<persondata>` (Destinatario)

-   `<address>`: Estensione destinatario

## Messaggi di Tipo `response` (Conferme di ricezione)

### Struttura Base

```xml
<?xml version="1.0" encoding="UTF-8"?>
<response version="19.11.12.1403" type="job">
<externalid>1234567890</externalid>
<systemdata>
<name>server</name>
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
<address>estensione_che_conferma</address>
<name>name</name>
<location>server</location>
</senderdata>
<persondata>
<address>estensione_originale</address>
<name>Nome Originale</name>
<location>location_originale</location>
</persondata>
</response>
```

### Caratteristiche delle Response

1. **`<messageuui>` è vuoto** - Le conferme non contengono testo
2. **`<status>` in jobdata** = "1" (messaggio ricevuto)
3. **Senderdata e persondata sono scambiati** rispetto al messaggio originale

## Tipi di Messaggio Osservati

### 1. Messaggi dal nostro Script → Sistema

-   **Tag**: `request`
-   **Type**: `job`
-   **Status jobdata**: `0` (in attesa di invio)
-   **Sender**: `server` / `Sistema`
-   **Caratteristiche**: Messaggi che inviamo tramite il nostro script

### 2. Messaggi da Dispositivi Reali → Sistema

-   **Tag**: `request`
-   **Type**: `job`
-   **Status jobdata**: `0` (ricevuto, in attesa di inoltro)
-   **Sender**: Estensione reale (es. `106`)
-   **Caratteristiche**: Messaggi da telefoni fisici

### 3. Conferme di Ricezione (Sistema → Mittente)

-   **Tag**: `response`
-   **Type**: `job`
-   **Status jobdata**: `1` (confermato)
-   **Caratteristiche**: Conferme automatiche inviate dal sistema

## Problemi Identificati

### 1. Roaming Table Vuota

**Problema**: `extension not found in roaming table`
**Causa**: Le estensioni non sono registrate nel sistema di roaming
**Soluzione**: I dispositivi devono registrarsi inviando messaggi di sistema o login

### 2. Formato Nome Tag

**Osservazione**: I tag `<name>` a volte appaiono come `<n>` nei log
**Causa**: Possibile truncation o parsing del sistema
**Impatto**: Non sembra influire sulla funzionalità

## Raccomandazioni per l'Invio

### Script send_message.py

Il nostro script genera il formato corretto, ma per un invio efficace:

1. **Estensioni Target**: Assicurarsi che esistano nel sistema
2. **Roaming**: I dispositivi devono essere online e registrati
3. **Monitoring**: Usare i log per verificare l'invio

### Formato Template Ottimale

Basato sui log reali, il template nel nostro script è corretto:

-   Versione XML: `19.11.12.1403`
-   Type: `job`
-   Status systemdata: `1`
-   Status jobdata: `0` (per nuovi messaggi)
-   Priority: `0`

## Debugging

### Controllo Log

```bash
# Analisi completa
python3 analyze_logs.py --detailed --format-compare

# Solo sommario
python3 analyze_logs.py

# Esporta in JSON
python3 analyze_logs.py --export results.json
```

### Verifica Roaming Table

I dispositivi devono apparire nei log con messaggi di tipo:

-   `systeminfo` - Aggiornamenti di posizione
-   `login` - Eventi di login/logout

### Test di Invio

```bash
# Test base
python3 send_message.py 106 "Test message"

# Con debug
python3 send_message.py 106 "Test message" --debug

# Verifica log dopo invio
ls -la logs/
python3 analyze_logs.py
```
