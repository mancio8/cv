---
title: "Luci di Stranger Things con WS2811 e Arduino Nano"
description: "Ricrea le iconiche luci della serie con LED WS2811 e Arduino Nano! ✨ Controlla ogni pixel per illuminare lettere e creare messaggi personalizzati, proprio come nella serie. 🔴🟢🔵 Scopri il progetto!
pubDate: "Mar 11 2025"
heroImage: "https://res.cloudinary.com/dqh1pnrdx/image/upload/v1741706481/Arci/Progetto_senza_titolo_1_ybpdhq.png"
badge: "Arduino"
---

# Luci di Stranger Things con WS2811 e Arduino Nano

In questo progetto ho ricreato le iconiche luci di *Stranger Things*, quelle che Joyce Byers usa per comunicare con il figlio nel Sottosopra. Per realizzarle, ho utilizzato dei **LED WS2811 IC RGB pixel** controllati da un **Arduino Nano**, permettendo di illuminare lettere e creare effetti personalizzati.

## Materiale Necessario  
- **Arduino Nano**  
- **Striscia LED WS2811 (IC RGB pixel)**  
- **Cavi jumper**  
- **Tavola o parete per il montaggio delle lettere**  
- **Pennarelli o adesivi per scrivere l’alfabeto**  

## Collegamenti Elettrici  
I LED WS2811 funzionano con **5V**, quindi possiamo alimentarli direttamente dall'**Arduino Nano** tramite la porta **5V** senza bisogno di alimentatori esterni.

1. **Collegare GND** della striscia LED a **GND** di Arduino.  
2. **Collegare il filo DATA IN** della striscia LED a un **pin digitale di Arduino (D11)**.  
3. **Collegare il filo 5V** della striscia LED al **5V di Arduino**.  

## Scrittura del Codice  
Per controllare i LED, useremo la libreria **FastLED**, che supporta i WS2811. Installa la libreria da **Arduino IDE** e usa il seguente codice per accendere i LED in sequenza:

```cpp
#include "FastLED.h"/
#define NUM_LEDS 50
#define DATA_PIN    11
#define BRIGHTNESS  255
CRGB leds[NUM_LEDS];
 

String letterIndex = "---IHGFEDCBA---------JKLMNOPQRST---------ZYXWVU--";
String colorLetterIndex = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

// Warm White = 0xFFF0C4
// Blue = 0x0000FF
// Magenta = 0xFF00FF
// Cyan = 0x00FFB9
// Yellow = 0xFCEE21
// Red = 0xFF0000
uint32_t colorIndex[26] = {
                          0xFFF0C4, // A
                          0x0000FF, // B
                          0xFF00FF, // C
                          0x00FFB9, // D
                          0x0000FF, // E
                          0xFCEE21, // F
                          0xFF0000, // G
                          0x00FFB9, // H
                          0x00FFB9, // I
                          0xFF00FF, // J
                          0x0000FF, // K
                          0x00FFB9, // L
                          0xFCEE21, // M
                          0xFF0000, // N
                          0xFF00FF, // O
                          0x00FFB9, // P
                          0xFF00FF, // Q
                          0x00FFB9, // R
                          0xFFF0C4, // S
                          0xFCEE21, // T
                          0x0000FF, // U
                          0xFF0000, // V
                          0x00FFB9, // W
                          0xFCEE21, // X
                          0xFF00FF, // Y
                          0xFF0000, // Z
                          };


void setup() {

      delay(3000);
      FastLED.addLeds<WS2811, DATA_PIN, RGB>(leds, NUM_LEDS);
      FastLED.setBrightness(BRIGHTNESS);
}


void loop() {

  turnOnAll();
  delay(2000);
  fill_solid( leds, NUM_LEDS, CRGB::Black);
  writeWord("MASCHERARCI",1000,300);
  delay(3000);
  turnOnAll();
  flickerLeds(100);
  allToFullBright();
  turnOnAll();
  delay(2000);
}

void turnOnAll()
{
  int stringLen = letterIndex.length()+1;
  char char_array[stringLen];
  letterIndex.toCharArray(char_array,stringLen);
  for(int i=0;i<stringLen-1;i++)
  {
    if ( String(char_array[i]))
    {
      turnOnLetter(String(char_array[i]));
    }
  }
  FastLED.show();
}

void turnOnLetter(String theLetter)
{
    int lightIndex = letterIndex.indexOf(theLetter);
    int colorIndexValue = colorLetterIndex.indexOf(theLetter);
    uint32_t colorValue = colorIndex[colorIndexValue];
    leds[lightIndex] = colorValue;
}

void writeWord(String theword,int letterDuration,int letterSpacing)
{
  int stringLen = theword.length()+1;
  char char_array[stringLen];
  theword.toCharArray(char_array,stringLen);

  for(int i=0;i<stringLen-1;i++)
  {
    displayLetter(String(char_array[i]),letterDuration);
    delay(letterSpacing);
  }
}


void displayLetter(String theLetter,int letterDuration)
{
  int lightIndex = letterIndex.indexOf(theLetter);
  int colorIndexValue = colorLetterIndex.indexOf(theLetter);
  uint32_t colorValue = colorIndex[colorIndexValue];
  lightLED(lightIndex,colorValue,letterDuration);   
}

void lightLED(int ledIndex,uint32_t colorValue,int duration)
{
  leds[ledIndex] = colorValue;
  FastLED.show();
  delay(duration);
  leds[ledIndex] = CRGB::Black;
  FastLED.show();

}

void flickerLeds(int numTimes)

{
  for ( int i=0;i<numTimes;i++)
  {
    flicker();
  }
}
void allToFullBright()
{
  int stringLen = letterIndex.length()+1;
  char char_array[stringLen];
  letterIndex.toCharArray(char_array,stringLen);

  for(int i=0;i<stringLen-1;i++)
  {
    if ( String(char_array[i]) != "-" )
    {
      leds[i].maximizeBrightness();
    }
  }
  FastLED.show();
}

void flicker() {                          //-m9-FLICKER EFFECT

  int random_bright = random(0,255);
  int random_delay = random(10,100);
  int randomFullLight = random(0,2);
  int stringLen = letterIndex.length()+1;
  char char_array[stringLen];
  letterIndex.toCharArray(char_array,stringLen);

  for(int i=0;i<stringLen-1;i++)
  {
    if ( String(char_array[i]) != "-" )
    {
      if ( randomFullLight == 0 )
      {
        leds[i].maximizeBrightness();
      }
      leds[i].fadeLightBy(random_bright);
    }
  }
  FastLED.show();
  delay(random_delay);
}
```

## Come funziona?

### Definizione dei parametri principali

Qui si impostano i parametri principali:

- **NUM_LEDS** → Numero di LED collegati (in questo caso, 50).
- **DATA_PIN** → Il pin digitale di Arduino a cui è collegata la striscia LED.
- **BRIGHTNESS** → Imposta la luminosità massima dei LED (255 = massimo).

```cpp
#define NUM_LEDS 50  
#define DATA_PIN 11  
#define BRIGHTNESS 255
```

### Dichiarazione della striscia LED

Si crea un array per memorizzare i colori di ogni LED:

```cpp
CRGB leds[NUM_LEDS];
```

### Mappatura delle lettere e dei colori

Il codice usa due stringhe:

   - letterIndex → Indica la posizione di ogni lettera sulla striscia LED.
   - colorLetterIndex → Contiene l'alfabeto dalla A alla Z.

Poi definisce un array di colori per ogni lettera:

```cpp
uint32_t colorIndex[26] = {  
    0xFFF0C4, // A (bianco caldo)  
    0x0000FF, // B (blu)  
    0xFF00FF, // C (magenta)  
    0x00FFB9, // D (ciano)  
    0xFCEE21, // F (giallo)  
    0xFF0000  // G (rosso)  
    // ... altri colori per tutte le lettere  
};

```
ogni lettera dell'alfabeto ha un colore specifico.

### Configurazione iniziale di Arduino

Nel setup(), si inizializza la striscia LED e si imposta la luminosità:


```ccp
void setup() {
    FastLED.addLeds<WS2811, DATA_PIN, GRB>(leds, NUM_LEDS);
    FastLED.setBrightness(BRIGHTNESS);
}
```

Questo dice ad Arduino che i LED usano il protocollo WS2811 e che i colori sono nel formato GRB (verde, rosso, blu).

### Loop principale: Illuminazione dei messaggi

Il codice accende le lettere secondo un messaggio predefinito, per esempio "RUN":

```cpp
void mostraMessaggio(String messaggio) {
    for (int i = 0; i < messaggio.length(); i++) {
        char lettera = messaggio[i];
        int pos = colorLetterIndex.indexOf(lettera); // Trova la posizione della lettera
        if (pos != -1) {
            leds[pos] = colorIndex[pos]; // Assegna il colore alla lettera
        }
    }
    FastLED.show();
    delay(1000); // Tempo di visualizzazione
}
```
Il codice cerca ogni lettera del messaggio nella mappatura e accende il LED corrispondente con il colore assegnato.

### Loop infinito per far lampeggiare le lettere

```cpp
void loop() {
    mostraMessaggio("RUN");
    delay(2000);
}
```



In questo caso, la parola "RUN" si illumina ogni 2 secondi, simulando l'effetto del messaggio di Stranger Things.

## Conclusione

Ora puoi caricare questo codice su Arduino e vedere i LED accendersi in base ai messaggi! Per cambiare parola, basta modificare la stringa nel loop().

🔴🟢🔵

