export interface WeatherCondition {
    text: string;
    icon: string;
  }
  
  export interface CurrentWeather {
    last_updated_epoch: number;
    last_updated: string;
    temp_c: number; // This is the current temperature
    condition: WeatherCondition;
  }
  
  export interface ForecastDay {
    date: string;
    day: {
      maxtemp_c: number;
      mintemp_c: number;
      condition: WeatherCondition;
    };
  }
  
  export interface Weather {
    current: CurrentWeather;
    forecast: {
      forecastday: ForecastDay[];
    };
  }
  

  export async function fetchWeatherForSpecificDate(lat: number, lon: number, date: string): Promise<Weather | null> {
    try {
        const apiKey = 'bcafe71c00ed4e1081e142910243010'; // Sostituisci con la tua chiave API
        const response = await fetch(`https://api.weatherapi.com/v1/forecast.json?key=${apiKey}&q=${lat},${lon}&days=14`);
    
      const data = await response.json();
  
      // Check if the expected data structure exists
      if (data.current && data.forecast.forecastday.length > 0) {
        const giorni = giorniMancanti(date);
       
        const forecastData = data.forecast.forecastday[giorni]; // Get the first day's forecast
  
        const weather: Weather = {
          current: {
            last_updated_epoch: data.current.last_updated_epoch,
            last_updated: data.current.last_updated,
            temp_c: data.current.temp_c,
            condition: {
              text: data.current.condition.text,
              icon: data.current.condition.icon,
            },
          },
          forecast: {
            forecastday: [
              {
                date: forecastData.date,
                day: {
                  maxtemp_c: forecastData.day.maxtemp_c,
                  mintemp_c: forecastData.day.mintemp_c,
                  condition: {
                    text: forecastData.day.condition.text,
                    icon: forecastData.day.condition.icon,
                  },
                },
              },
            ],
          },
        };
  
        return weather;
      } else {
        return null; // Handle the case where data is not available
      }
    } catch (error) {
      console.error('Error fetching weather data:', error);
      return null; // Handle errors appropriately
    }
  }

  export async function fetchWeatherForSpecificDateF1(lat: number, lon: number, date: string): Promise<Weather | null> {
    try {
        const apiKey = 'bcafe71c00ed4e1081e142910243010'; // Sostituisci con la tua chiave API
        const response = await fetch(`https://api.weatherapi.com/v1/forecast.json?key=${apiKey}&q=${lat},${lon}&days=14`);
    
      const data = await response.json();
  
      // Check if the expected data structure exists
      if (data.current && data.forecast.forecastday.length > 0) {
        const giorni = giorniMancantiF1(date);
       
        const forecastData = data.forecast.forecastday[giorni]; // Get the first day's forecast
  
        const weather: Weather = {
          current: {
            last_updated_epoch: data.current.last_updated_epoch,
            last_updated: data.current.last_updated,
            temp_c: data.current.temp_c,
            condition: {
              text: data.current.condition.text,
              icon: data.current.condition.icon,
            },
          },
          forecast: {
            forecastday: [
              {
                date: forecastData.date,
                day: {
                  maxtemp_c: forecastData.day.maxtemp_c,
                  mintemp_c: forecastData.day.mintemp_c,
                  condition: {
                    text: forecastData.day.condition.text,
                    icon: forecastData.day.condition.icon,
                  },
                },
              },
            ],
          },
        };
  
        return weather;
      } else {
        return null; // Handle the case where data is not available
      }
    } catch (error) {
      console.error('Error fetching weather data:', error);
      return null; // Handle errors appropriately
    }
  }
  

  function giorniMancanti(dataString: string): number {
    // Ottieni la data odierna
    const oggi = new Date();

    // Estrai il giorno, il mese, l'anno e l'ora dalla stringa
    const [data, ora] = dataString.split(' ');
    const [giorno, mese, anno] = data.split('/').map(Number);
    const [ore, minuti] = ora ? ora.split(':').map(Number) : [0, 0];

    const annoCompleto = 2000 + anno; // Assumiamo che l'anno sia del 2000

    // Crea un oggetto Date per la data fornita
    const dataFornita = new Date(annoCompleto, mese - 1, giorno, ore, minuti);

    // Calcola la differenza in millisecondi
    const differenzaMillisecondi = dataFornita.getTime() - oggi.getTime();

    // Calcola il numero di giorni rimanenti
    const giorniRimanenti = Math.ceil(differenzaMillisecondi / (1000 * 3600 * 24));

    return giorniRimanenti; // Restituisci il numero di giorni
}

function giorniMancantiF1(dataString: string): number {
    // Ottieni la data odierna
    const oggi = new Date();

    // Estrai il giorno, il mese, l'anno e l'ora dalla stringa
    const [data] = dataString.split(' ');
    const [anno, mese, giorno] = data.split('-').map(Number);
    

    

    // Crea un oggetto Date per la data fornita
    const dataFornita = new Date(anno, mese - 1, giorno);

    // Calcola la differenza in millisecondi
    const differenzaMillisecondi = dataFornita.getTime() - oggi.getTime();

    // Calcola il numero di giorni rimanenti
    const giorniRimanenti = Math.ceil(differenzaMillisecondi / (1000 * 3600 * 24));

    return giorniRimanenti; // Restituisci il numero di giorni
}





