// src/services/motoGPService.ts
import axios from 'axios';

export async function getNextRace() {
    const response = await axios.get('https://api.motogp.com/en/api/season/current');
    const seasonData = response.data;
    const nextRace = seasonData.nextRace; // Assicurati che questo percorso esista nell'API

    // Converti le date in orari locali
    const raceDate = new Date(nextRace.dateTime);
    const options: Intl.DateTimeFormatOptions = { 
        weekday: 'long', hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Rome'
    };
    const raceTimeInItaly = raceDate.toLocaleString('it-IT', options);

    // Recupera i risultati delle qualifiche
    let qualifyingResults = [];
    try {
        const qualResultsResponse = await axios.get(`https://api.motogp.com/en/api/races/${nextRace.id}/qualifying`);
        qualifyingResults = qualResultsResponse.data;
    } catch (error) {
        console.log("Risultati delle qualifiche non disponibili.");
    }

    return {
        ...nextRace,
        raceTimeInItaly,
        qualifyingResults
    };
}

export async function getStandings() {
    const response = await axios.get('https://api.motogp.com/en/api/standings');
    return response.data; // Assicurati di controllare la struttura della risposta
}
