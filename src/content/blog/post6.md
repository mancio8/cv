---
title: "Creazione di una Pagina per Podcast con DaisyUI e Astro"
description: "In questo progetto, ho sviluppato una pagina per la visualizzazione e l'ascolto di podcast, utilizzando Astro e DaisyUI. L'idea di base era creare una soluzione automatica per caricare i podcast da un feed RSS e generare dinamicamente delle card per ogni episodio, consentendo agli utenti di ascoltarli facilmente."
pubDate: "Mar 30 2025"
heroImage: "https://res.cloudinary.com/dqh1pnrdx/image/upload/v1743363800/Cv/podcast_rhzwas.png"
badge: "Astro"
---
# Creazione di una Pagina per Podcast con DaisyUI e Astro

In questo progetto, ho sviluppato una pagina per la visualizzazione e l'ascolto di podcast, utilizzando **Astro** e **DaisyUI**. L'idea di base era creare una soluzione automatica per caricare i podcast da un feed RSS e generare dinamicamente delle card per ogni episodio, consentendo agli utenti di ascoltarli facilmente.

### Obiettivo

L'obiettivo principale era creare una pagina che caricasse e visualizzasse gli episodi di un podcast partendo direttamente da un feed RSS. L'interfaccia doveva essere semplice e user-friendly, utilizzando DaisyUI per i componenti e Astro per il rendering.

### Funzionamento

1. **RSS Feed**: Ho integrato un feed RSS da una fonte esterna (nel mio caso, il podcast di Spreaker). Il feed contiene informazioni cruciali come titolo, data di pubblicazione, descrizione, immagine dell'episodio e URL dell'audio.

2. **Estrazione dei Dati**: Utilizzando il pacchetto `xml2js`, ho fatto il parsing del feed RSS per estrarre i dati relativi a ciascun episodio, inclusi il titolo, la descrizione e l'URL dell'audio. Ho incluso anche un'immagine associata a ciascun episodio.

3. **Generazione Dinamica delle Card**: Una volta ottenuti i dati, li ho usati per generare dinamicamente delle card. Ogni card contiene:
   - **Titolo dell'episodio**
   - **Data di pubblicazione**
   - **Descrizione dell'episodio** (visibile con un limite di caratteri)
   - **Un pulsante "Play"** per ascoltare il podcast, che carica il file audio in modo dinamico
   - **Immagine** associata all'episodio

4. **Design con DaisyUI**: Ho usato DaisyUI per creare una UI elegante e responsiva, con effetti hover per migliorare l'interazione dell'utente. La pagina è progettata per essere visualizzata correttamente sia su desktop che su dispositivi mobili.

5. **Funzionalità "Play"**: Un aspetto importante era la possibilità di ascoltare i podcast direttamente dalla pagina. Ho implementato una funzione JavaScript per caricare e controllare il file audio quando l'utente clicca sul pulsante "Play".

### Codice

Il codice che ho sviluppato per realizzare questa pagina è semplice e modulare, ecco un esempio del flusso:

```astro
---
import { parseStringPromise } from "xml2js";
import HorizontalCard from "../components/HorizontalCard.astro";
import BaseLayout from "../layouts/BaseLayout.astro";
import { Image } from "@astrojs/image/components";

const RSS_FEED = "https://www.spreaker.com/show/4070003/episodes/feed"; // Sostituisci con il feed corretto
const response = await fetch(RSS_FEED);
const text = await response.text();
const data = await parseStringPromise(text);

// Estrarre episodi dall'RSS
const episodes = data.rss.channel[0].item.map((ep) => ({
  title: ep.title[0],
  date: new Date(ep.pubDate[0]).toLocaleDateString(),
  audioUrl: ep.enclosure[0].$.url,
  description: ep.description[0],
  imageUrl: ep["itunes:image"][0].$.href,
}));

const podcastImage = data.rss.channel[0].image[0].url[0];
---

<BaseLayout sideBarActiveItemID="home">
  <script>
    window.loadAudio = function loadAudio(button, audioUrl) {
      const container = button.parentElement;
      button.style.display = "none";
      const audio = document.createElement("audio");
      audio.controls = true;
      audio.preload = "metadata";
      audio.className = "mt-2 w-full";
      const source = document.createElement("source");
      source.src = audioUrl;
      source.type = "audio/mpeg";
      audio.appendChild(source);
      container.appendChild(audio);
    };
  </script>

  <h1 class="text-3xl font-bold text-center mb-6">🎙 Podcast</h1>

  <div class="flex justify-center mb-6">
    <img src={podcastImage} alt="Podcast Image" class="rounded-lg shadow-lg w-1/3 max-w-xs" />
  </div>

  <div class="rounded-lg bg-base-100">
    {episodes.length > 0 ? (
      episodes.map((ep, index) => (
        <div class="hero-content flex-col md:flex-row">
          <Image src={ep.imageUrl} class="rounded-lg shadow-md mb-4" aspectRatio="16:9" width={750} format="webp" alt={`Immagine per ${ep.title}`} class="max-w-full md:max-w-[13rem] rounded-lg" />
          <div class="grow w-full">
            <h1 class="text-xl font-bold">{ep.title}</h1>
            <p class="text-gray-500 text-sm">{ep.date}</p>
            <p class="py-1 text-1xl line-clamp-4" set:html={ep.description}></p>
            <div id={`audio-container-${index}`} class="mt-4">
              <button class="btn btn-primary w-full" onclick={`loadAudio(this, '${ep.audioUrl}')`}>Play</button>
            </div>
          </div>
        </div>
      ))
    ) : (
      <p class="col-span-full text-center">Nessun episodio disponibile.</p>
    )}
  </div>
</BaseLayout>
```

### Risultato Finale

La pagina risultante è una piattaforma di ascolto podcast semplice ma funzionale, che si adatta automaticamente ai nuovi episodi ogni volta che viene aggiornato il feed RSS. Gli utenti possono visualizzare i dettagli degli episodi, ascoltare l'audio direttamente dalla pagina e navigare facilmente tra le card.

### Conclusioni

Questo progetto è stato una grande opportunità per esplorare l'integrazione tra Astro e DaisyUI. La capacità di Astro di generare contenuti dinamici e la semplicità di DaisyUI hanno reso l'intero processo di sviluppo molto rapido ed efficiente. Questo tipo di approccio permette di costruire pagine reattive e moderne in modo semplice, utilizzando i feed RSS per caricare contenuti in tempo reale.

### Demo

Puoi vedere una demo funzionante del progetto al seguente [link](https://vincenzomancinelli.it/podcast).

