---
title: "Visualizzatore Statistiche Motorsport"
description: "Questo progetto è un'applicazione web a schede sviluppata per mostrare statistiche aggiornate e storiche della Formula 1."
pubDate: "Oct 29 2024"
heroImage: "/post_img.webp"
badge: "F1"
---

# Visualizzatore Statistiche Motorsport

Questo progetto è un'applicazione web a schede sviluppata per mostrare statistiche aggiornate e storiche della **Formula 1**. Ogni sezione presenta dati dettagliati sulle prossime gare, i risultati dell’ultimo evento e le classifiche attuali di piloti e costruttori. Il progetto è realizzato utilizzando **Astro** e **DaisyUI** per un'interfaccia moderna e minimalista, con **TypeScript** per la gestione dell'integrazione dei dati via API.

## Caratteristiche principali

### 1. **Navigazione a Schede**
   - L’approccio modulare di Astro permette a ogni scheda di caricare e visualizzare dinamicamente informazioni pertinenti senza l'uso di React, migliorando così semplicità e prestazioni.

### 2. **Integrazione dei Dati in Tempo Reale**
   - Utilizzo di API per ottenere dati aggiornati sulle classifiche di piloti e costruttori, i risultati delle ultime gare e i dettagli sul prossimo evento.
   - Aggiustamenti per la conversione di fusi orari, soprattutto per gli orari di gara, garantendo coerenza dei dati in diverse regioni.

### 3. **Personalizzazione UI con DaisyUI**
   - Uso dei componenti di DaisyUI per le schede e i layout a schede, con CSS personalizzato per migliorare l’interfaccia visiva e l’esperienza utente.
   - Colori dei team nelle classifiche, allineati con lo schema colore di ciascun costruttore per una presentazione più immersiva.

### 4. **Prestazioni e Semplicità**
   - Le richieste API vengono gestite senza dipendere da librerie esterne come Axios, utilizzando invece `fetch` nativo per ridurre le dipendenze e migliorare i tempi di caricamento.
   - TypeScript gestisce le risposte delle API con tipi e controlli per dati null o indefiniti, migliorando l'affidabilità dell’esperienza utente.

Questo progetto offre agli appassionati di motorsport un punto di riferimento centralizzato per dati di gara essenziali, arricchito visivamente con lo styling di DaisyUI.
