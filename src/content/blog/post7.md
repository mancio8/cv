---
title: "Arci Quiz: il backend dietro il quiz interattivo"
description: "In questo progetto ho lavorato sul backend di un quiz interattivo a squadre, utilizzando Django containerizzato con Docker, PostgreSQL e Redis, implementando autenticazione sicura con Authentik e integrando pulsanti fisici tramite ESP32 con WebSocket per aggiornamenti in tempo reale."
pubDate: "Nov 27 2025"
heroImage: "https://res.cloudinary.com/dqh1pnrdx/image/upload/v1764078768/Arci/ArciQuiz_oxzuog.webp"
badge: "Django"
---


# Arci Quiz: il backend dietro il quiz interattivo

**Ruolo:** Backend Developer  
**Tecnologie principali:** Django, Docker, PostgreSQL, Redis, Authentik, WebSocket, ESP32  

---

## La sfida

Quando ho iniziato a lavorare su **Arci Quiz**, l'obiettivo era creare un'esperienza interattiva per eventi e quiz a squadre: non solo domande e punteggi, ma anche la possibilità di prenotare pulsanti fisici e avere aggiornamenti in tempo reale su ogni azione.  

La sfida principale? Integrare un backend robusto con componenti hardware e garantire sicurezza, scalabilità e fluidità nelle interazioni.

---

## Il mio contributo

Mi sono occupato principalmente del **backend**:

- **Architettura containerizzata con Docker**  
  Ho configurato i servizi principali del progetto in container: Django per il backend, PostgreSQL per la gestione dei dati e Redis per il realtime e la gestione dei timer.  
  

- **Autenticazione sicura con Authentik**  
  Ho integrato Authentik per gestire login, permessi e autorizzazioni in modo centralizzato, così da garantire sicurezza e controllo degli accessi.  
  

- **Comunicazione in tempo reale con WebSocket**  
  Per aggiornare punteggi, timer e stato dei pulsanti, ho utilizzato WebSocket, garantendo un flusso dati costante e immediato tra server e client web.  
  

- **Integrazione hardware con ESP32**  
  I pulsanti fisici dei partecipanti erano connessi tramite ESP32. Ho sviluppato le chiamate dal backend verso questi dispositivi, permettendo di prenotare i pulsanti e aggiornare immediatamente l'interfaccia web.  
  

---

## Risultati

- Sistema backend completamente containerizzato, pronto per produzione.  
- Autenticazione centralizzata e sicura.  
- Quiz interattivo in tempo reale, con gestione dei timer e dei punteggi.  
- Integrazione hardware-software funzionante, che ha migliorato l’esperienza degli utenti agli eventi.  

---

Arci Quiz è stata una grande occasione per combinare **backend, realtime e IoT**, imparando a far comunicare servizi diversi e a gestire dati in tempo reale in modo affidabile.  

---


