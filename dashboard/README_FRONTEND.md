# Balkonsolar Dashboard - Frontend-Dokumentation

## 🌟 Übersicht
Dieses Dashboard visualisiert Energiedaten aus einer SQLite-Datenbank in Echtzeit. Es zeigt vier verschiedene Metriken an:
- 🌞 Solarproduktion
- 🔋 Batteriestatus
- 🔌 Netznutzung
- 🤖 Algorithmus-Output

## 📋 Voraussetzungen
- Node.js v20.17.0 oder höher
- pnpm (neueste Version)
- Ein laufender Backend-Server (siehe Backend-Setup)

## 🚀 Installation & Setup

### 1. Backend-Server einrichten
```bash
# Navigieren Sie zum Backend-Verzeichnis
cd balkonsolar/database_shenanigans

# Installieren Sie die Abhängigkeiten
npm install express sqlite3 cors

# Starten Sie den Server
node server.js
```

Der Backend-Server sollte nun auf Port 3001 laufen mit der Meldung:
```
Server läuft auf http://localhost:3001
```

### 2. Frontend-Anwendung einrichten
```bash
# Navigieren Sie zum Frontend-Verzeichnis
cd dashboard

# Installieren Sie die Abhängigkeiten
pnpm install

# Starten Sie den Entwicklungsserver
pnpm dev
```

Die Anwendung ist nun unter http://localhost:3000 verfügbar.

## 🔍 Systemarchitektur

```
Frontend (Next.js, Port 3000)
         ↓
Next.js API Route (/api/energy)
         ↓
Backend (Express, Port 3001)
         ↓
SQLite Datenbank (energy_data.db)
```

## 📊 Features

### Datenvisualisierung
- Echtzeitanzeige von Energiedaten
- Automatische Aktualisierung alle 5 Minuten
- Interaktive Liniendiagramme
- Deutsche Datums- und Zeitformatierung

### Fehlerbehandlung
- Automatische Wiederholungsversuche (max. 3)
- 5 Sekunden Timeout pro Anfrage
- Benutzerfreundliche Fehlermeldungen
- "Erneut versuchen" Button bei Fehlern

### Responsive Design
- Anpassung an verschiedene Bildschirmgrößen
- 2 Spalten auf Desktop
- 1 Spalte auf mobilen Geräten

## 🛠 Entwicklung

### Projektstruktur
```
dashboard/
├── components/
│   └── EnergyDashboard.tsx    # Hauptkomponente
├── app/
│   └── api/
│       └── energy/
│           └── route.ts       # API-Route
└── package.json
```

### Wichtige Dateien
- `EnergyDashboard.tsx`: Hauptkomponente für die Datenvisualisierung
- `route.ts`: API-Route für die Kommunikation mit dem Backend

## 🐛 Fehlerbehebung

### Backend nicht erreichbar
1. Überprüfen Sie, ob der Backend-Server läuft
2. Terminal öffnen und navigieren zu `balkonsolar/database_shenanigans`
3. Server neu starten: `node server.js`

### Frontend-Fehler
1. Browser-Entwicklertools öffnen (F12)
2. Konsole auf Fehlermeldungen prüfen
3. Im Netzwerk-Tab API-Aufrufe überprüfen

### Server-Neustart
```bash
# Alle Node-Prozesse beenden
Stop-Process -Name "node" -Force

# Backend neu starten
cd balkonsolar/database_shenanigans
node server.js

# Frontend neu starten (neues Terminal)
cd dashboard
pnpm dev
```

## ⚙️ Konfiguration

### Anpassbare Parameter
- Aktualisierungsintervall: `5 * 60 * 1000` (5 Minuten)
- Maximale Wiederholungsversuche: `MAX_RETRIES = 3`
- Verzögerung zwischen Versuchen: `RETRY_DELAY = 5000` (5 Sekunden)

Diese Parameter können in `EnergyDashboard.tsx` angepasst werden.

## 📝 API-Endpunkte

### GET /api/energy
Parameter:
- `table`: Name der Datentabelle (solar_output, battery_storage_status, grid_usage, output_algorithm)
- `limit`: Maximale Anzahl der Datenpunkte (Standard: 50)
- `startTime`: Optionaler Startzeitpunkt (ISO-Format)
- `endTime`: Optionaler Endzeitpunkt (ISO-Format)

Beispiel:
```
/api/energy?table=solar_output&limit=50
```

## 🤝 Support

Bei Problemen oder Fragen:
1. Überprüfen Sie die Konsolenausgaben
2. Stellen Sie sicher, dass beide Server laufen
3. Prüfen Sie die Netzwerkverbindung
4. Kontaktieren Sie das Entwicklerteam

## 🔄 Updates & Wartung

- Regelmäßig `pnpm install` ausführen
- Backend-Abhängigkeiten mit `npm install` aktualisieren
- Codeänderungen erfordern Neustart der Server 