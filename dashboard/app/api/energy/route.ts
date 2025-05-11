import { NextResponse } from 'next/server';

const API_BASE_URL = 'http://localhost:3001';

// Konfiguriere die Ausführungsumgebung
export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    
    // Versuche die Anfrage an den Express-Server weiterzuleiten
    try {
      const response = await fetch(`${API_BASE_URL}/api/energy?${searchParams.toString()}`, {
        // Setze einen Timeout von 5 Sekunden
        signal: AbortSignal.timeout(5000)
      });
      
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `HTTP Fehler ${response.status}`);
      }

      return NextResponse.json(data);
    } catch (error: unknown) {
      // Spezifische Fehlermeldungen für verschiedene Fehlertypen
      if (error instanceof TypeError && error.message === 'Failed to fetch') {
        throw new Error('Der Datenbankserver ist nicht erreichbar. Bitte starten Sie den Server neu.');
      } else if (error instanceof Error && error.name === 'AbortError') {
        throw new Error('Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es später erneut.');
      }
      throw error;
    }
  } catch (error) {
    console.error('API-Fehler:', error);
    return NextResponse.json(
      { 
        error: error instanceof Error 
          ? error.message 
          : 'Ein unerwarteter Fehler ist aufgetreten'
      },
      { status: 500 }
    );
  }
} 