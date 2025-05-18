const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');
const path = require('path');

const app = express();
const port = 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Datenbankpfad - jetzt relativ zum aktuellen Verzeichnis
const DB_PATH = path.join(__dirname, 'energy_data.db');

// Hilfsfunktion für Datenbankabfragen
function queryDatabase(query, params) {
  return new Promise((resolve, reject) => {
    const db = new sqlite3.Database(DB_PATH, (err) => {
      if (err) {
        reject(err);
        return;
      }
    });

    db.all(query, params, (err, rows) => {
      if (err) {
        db.close();
        reject(err);
        return;
      }
      db.close();
      resolve(rows);
    });
  });
}

// API-Endpunkt für Energiedaten
app.get('/api/energy', async (req, res) => {
  try {
    const { table, limit = 100, startTime, endTime } = req.query;
    
    // Validiere Tabellennamen
    const validTables = ['solar_output', 'battery_storage_status', 'grid_usage', 'output_algorithm', 'irradiation_data', 'grid_usage_forecast'];
    if (!table || !validTables.includes(table)) {
      return res.status(400).json({ error: 'Ungültiger Tabellenparameter' });
    }

    // Baue Query
    let query;
    if (table === 'output_algorithm') {
      query = `SELECT timestamp, suggested_state as suggested_state, grid_state as value, usage as usage FROM ${table}`;
    } else {
      query = `SELECT tstamp as timestamp, value FROM ${table}`;
    }
    const params = [];

    if (startTime || endTime) {
      query += ' WHERE';
      if (startTime) {
        query += table === 'output_algorithm' ? ' timestamp >= ?' : ' tstamp >= ?';
        params.push(startTime);
      }
      if (endTime) {
        if (startTime) query += ' AND';
        query += table === 'output_algorithm' ? ' timestamp <= ?' : ' tstamp <= ?';
        params.push(endTime);
      }
    }

    query += table === 'output_algorithm' ? ' ORDER BY timestamp DESC LIMIT ?' : ' ORDER BY tstamp DESC LIMIT ?';
    params.push(parseInt(limit));

    const data = await queryDatabase(query, params);
    res.json(data);

  } catch (error) {
    console.error('API-Fehler:', error);
    res.status(500).json({ error: error.message });
  }
});

app.listen(port, () => {
  console.log(`Server läuft auf http://localhost:${port}`);
  console.log(`Verbunden mit Datenbank: ${DB_PATH}`);
}); 