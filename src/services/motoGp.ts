// Interfaccia per i dati ricevuti dall'API
interface Country {
    iso: string;
    name: string;
    region_iso: string;
  }
  
  interface Circuit {
    id: string;
    name: string;
    legacy_id: number;
    place: string;
    nation: string;
  }
  
  interface Event {
    country: Country;
    circuit: Circuit;
    date_start: string;
    date_end: string;
    name: string; // Nome dell'evento
  }
  
  // Funzione per recuperare e stampare i dati
  async function fetchMotoGpEvents() {
    const response = await fetch('https://api.motogp.pulselive.com/motogp/v1/results/events/?seasonUuid=dd12382e-1d9f-46ee-a5f7-c5104db28e43&isFinished=false');
    const data: { events: Event[] } = await response.json();
  
    // Iterare attraverso gli eventi e stampare i dettagli desiderati
    data.events.forEach(event => {
      const countryName = event.country.name;
      const circuitName = event.circuit.name;
      const dateStart = event.date_start;
      const dateEnd = event.date_end;
      const place = event.circuit.place;
  
      console.log(`Evento: ${event.name}`);
      console.log(`Paese: ${countryName}`);
      console.log(`Circuito: ${circuitName}`);
      console.log(`Luogo: ${place}`);
      console.log(`Data di inizio: ${dateStart}`);
      console.log(`Data di fine: ${dateEnd}`);
      console.log('------------------------');
    });
  }
  

  // https://api.motogp.pulselive.com/motogp/v1/results/seasons per vedere l'id della stagione