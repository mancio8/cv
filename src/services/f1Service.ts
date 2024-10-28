// src/services/f1Service.ts

export async function getNextRace() {
    const response = await fetch('https://ergast.com/api/f1/current/next.json', { cache: "no-store" });
    const data = await response.json();
    const race = data.MRData.RaceTable.Races[0];

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
        const qualResultsResponse = await fetch(`https://ergast.com/api/f1/current/${race.round}/qualifying.json`, { cache: "no-store" });
        const qualResultsData = await qualResultsResponse.json();
        qualifyingResults = qualResultsData.MRData.RaceTable.Races[0].QualifyingResults;
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
    const response = await fetch('https://ergast.com/api/f1/current/last/results.json', { cache: "no-store" });
    const data = await response.json();
    return data.MRData.RaceTable.Races[0].Results;
}

export async function getDriverStandings() {
    const response = await fetch('https://ergast.com/api/f1/current/driverStandings.json', { cache: "no-store" });
    const data = await response.json();
    return data.MRData.StandingsTable.StandingsLists[0].DriverStandings;
}

export async function getConstructorStandings() {
    const response = await fetch('https://ergast.com/api/f1/current/constructorStandings.json', { cache: "no-store" });
    const data = await response.json();
    return data.MRData.StandingsTable.StandingsLists[0].ConstructorStandings;
}
