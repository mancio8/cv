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
    
    // Estrai le informazioni sui piloti e i team
    const standings = data.MRData.StandingsTable.StandingsLists[0].DriverStandings;

    // Aggiungi il nome del team a ciascun pilota
    const driverStandingsWithTeams = standings.map(standing => {
        return {
            position: standing.position,
            driver: standing.Driver,
            constructor: standing.Constructors[0], // Prendi il primo team (costruttore)
            points: standing.points
        };
    });
    
    return driverStandingsWithTeams;
}


export async function getConstructorStandings() {
    const response = await fetch('https://ergast.com/api/f1/current/constructorStandings.json', { cache: "no-store" });
    const data = await response.json();
    return data.MRData.StandingsTable.StandingsLists[0].ConstructorStandings;
}

export async function getAllRacesInSeason(season) {
    const response = await fetch(`https://ergast.com/api/f1/${season}.json`, { cache: "no-store" });
    const data = await response.json();
    return data.MRData.RaceTable.Races;
}

export async function getConstructorInfo(constructorId) {
    const response = await fetch(`https://ergast.com/api/f1/constructors/${constructorId}.json`, { cache: "no-store" });
    const data = await response.json();
    return data.MRData.ConstructorTable.Constructors[0];
}

export async function getDriverInfo(driverId) {
    const response = await fetch(`https://ergast.com/api/f1/drivers/${driverId}.json`, { cache: "no-store" });
    const data = await response.json();
    return data.MRData.DriverTable.Drivers[0];
}

export async function getCircuitInfo(circuitId) {
    const response = await fetch(`https://ergast.com/api/f1/circuits/${circuitId}.json`, { cache: "no-store" });
    const data = await response.json();
    return data.MRData.CircuitTable.Circuits[0];
}

export async function getRaceDetails(season, round) {
    const response = await fetch(`https://ergast.com/api/f1/${season}/${round}.json`, { cache: "no-store" });
    const data = await response.json();
    return data.MRData.RaceTable.Races[0];
}

export async function getDriverStatsAll(driverId: string) {
    let wins = 0;
    let podiums = 0;
    let poles = 0;
    let championships = 0;

    // 1. Ottieni le stagioni in cui il pilota ha gareggiato
    const seasonsResponse = await fetch(`https://ergast.com/api/f1/drivers/${driverId}/seasons.json?limit=100`);
    const seasonsData = await seasonsResponse.json();
    const seasons = seasonsData.MRData.SeasonTable.Seasons.map((season) => season.season);

    for (const season of seasons) {
        // 2. Ottieni i risultati per la stagione
        const seasonResponse = await fetch(`https://ergast.com/api/f1/${season}/drivers/${driverId}/results.json`);
        const seasonData = await seasonResponse.json();
        const races = seasonData.MRData.RaceTable.Races;

        for (const race of races) {
            // Ignora le gare sprint
            if (race.raceName.toLowerCase().includes('sprint')) continue;

            const position = parseInt(race.Results[0].position, 10);
            const qualifyingPosition = parseInt(race.Results[0].grid, 10);

            // Conteggia vittorie, podi e pole position solo per le gare non sprint
            if (position === 1) wins++;
            if (position >= 1 && position <= 3) podiums++;
            if (qualifyingPosition === 1) poles++;
        }

        // 3. Verifica se il pilota ha vinto il campionato in quella stagione
        const standingsResponse = await fetch(`https://ergast.com/api/f1/${season}/drivers/${driverId}/driverStandings.json`);
        const standingsData = await standingsResponse.json();
        const standingsList = standingsData.MRData.StandingsTable.StandingsLists;

        if (standingsList.length > 0 && standingsList[0].DriverStandings[0].position === '1') {
            championships++;
        }
    }

    return {
        wins,
        podiums,
        poles,
        championships
    };
}

export async function getDriverStats(driverId: string) {
    let wins = 0;
    let podiums = 0;
    let poles = 0;
    let championships = 0;

    // Ottieni i risultati per la stagione 2024
    const seasonResponse = await fetch(`https://ergast.com/api/f1/2024/drivers/${driverId}/results.json`);
    const seasonData = await seasonResponse.json();
    const races = seasonData.MRData.RaceTable.Races;

    for (const race of races) {
        // Ignora le gare sprint
        if (race.raceName.toLowerCase().includes('sprint')) continue;

        const position = parseInt(race.Results[0].position, 10);
        const qualifyingPosition = parseInt(race.Results[0].grid, 10);

        // Conteggia vittorie, podi e pole position solo per le gare non sprint
        if (position === 1) wins++;
        if (position >= 1 && position <= 3) podiums++;
        if (qualifyingPosition === 1) poles++;
    }

    // Verifica se il pilota ha vinto il campionato nella stagione 2024
    const standingsResponse = await fetch(`https://ergast.com/api/f1/2024/drivers/${driverId}/driverStandings.json`);
    const standingsData = await standingsResponse.json();
    const standingsList = standingsData.MRData.StandingsTable.StandingsLists;

    if (standingsList.length > 0 && standingsList[0].DriverStandings[0].position === '1') {
        championships = 1;
    }

    return {
        wins,
        podiums,
        poles,
        championships
    };
}

