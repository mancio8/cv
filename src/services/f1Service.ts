// src/services/f1Service.ts
import axios from 'axios';

export async function getNextRace() {
    const response = await axios.get('https://ergast.com/api/f1/current/next.json');
    const race = response.data.MRData.RaceTable.Races[0];

    // Conversione delle date per la gara e le qualifiche
    const raceDate = new Date(`${race.date}T${race.time}`);
    const qualDate = new Date(`${race.Qualifying.date}T${race.Qualifying.time}`);

    // Converte in ora locale italiana
    const options: Intl.DateTimeFormatOptions = { 
        weekday: 'long', hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Rome'
    };
    const raceTimeInItaly = raceDate.toLocaleString('it-IT', options);
    const qualTimeInItaly = qualDate.toLocaleString('it-IT', options);

    // Controllo per i risultati delle qualifiche
    let qualifyingResults = [];
    try {
        const qualResultsResponse = await axios.get(`https://ergast.com/api/f1/current/${race.round}/qualifying.json`);
        qualifyingResults = qualResultsResponse.data.MRData.RaceTable.Races[0].QualifyingResults;
    } catch (error) {
        console.log("Risultati delle qualifiche non ancora disponibili.");
    }

   

    return {
        ...race,
        raceTimeInItaly,
        qualTimeInItaly,
        qualifyingResults
    };
}

export async function getLastRaceResults() {
    const response = await axios.get('https://ergast.com/api/f1/current/last/results.json');
    return response.data.MRData.RaceTable.Races[0].Results;
}

export async function getDriverStandings() {
    const response = await axios.get('https://ergast.com/api/f1/current/driverStandings.json');
    return response.data.MRData.StandingsTable.StandingsLists[0].DriverStandings;
}

export async function getConstructorStandings() {
    const response = await axios.get('https://ergast.com/api/f1/current/constructorStandings.json');
    return response.data.MRData.StandingsTable.StandingsLists[0].ConstructorStandings;
}
