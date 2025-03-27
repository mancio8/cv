---
title: "Sito Web Dinamico"
description: "sito web dinamico arciguardia.online"
pubDate: "Sep 11 2024"
heroImage: "hhttps://res.cloudinary.com/dqh1pnrdx/image/upload/v1743086976/Cv/Arci_Guardia_ph7ypc.png"
---

## Sito Web Dinamico per ArciGuardia

Ho sviluppato un sito web dinamico per **ArciGuardia**. Il sito include un sistema di gestione di eventi, partite live e iscrizioni. Il backend è realizzato con **Python** e **Django**, con **MariaDB** come database. Il frontend è costruito utilizzando **Bootstrap** per garantire un'interfaccia moderna e responsive.

### Tecnologie utilizzate:
- **Backend**: Python, Django
- **Database**: MariaDB
- **Frontend**: Bootstrap
- **Containerizzazione**: Docker
- **Server WSGI**: Gunicorn
- **Proxy Reverse**: Nginx
- **Altri strumenti**: HTML5, CSS3, JavaScript

### Funzionalità principali:
- Gestione eventi e registrazioni online
- Gestione live delle partite: Gli utenti abilitati possono aggiornare in tempo reale il risultato e altre statistiche delle partite, salvandole nel database.
- Iscrizione dei partecipanti: Il database viene utilizzato anche per gestire l'iscrizione degli utenti agli eventi o alle competizioni.


### Infrastruttura e Hosting:
Il sito è ospitato in un ambiente **Docker**, con il backend **Django** eseguito in un container separato gestito da **Gunicorn** come server WSGI. Per migliorare le prestazioni e la scalabilità, è stato configurato **Nginx** come reverse proxy per gestire le richieste HTTP e servire file statici.

- **Docker**: Per la containerizzazione delle applicazioni e dei servizi, assicurando isolamento e portabilità.
- **Gunicorn**: Per gestire in modo efficiente le richieste HTTP con **Django**.
- **Nginx**: Configurato come reverse proxy per instradare le richieste verso **Gunicorn** e servire file statici.

### Comandi Docker utili:
Ecco alcuni comandi utilizzati per avviare l'ambiente in Docker:
```bash
# Costruire i container
docker-compose up --build

# Avviare i container in background
docker-compose up -d

# Controllare i log
docker-compose logs -f

# Arrestare i container
docker-compose down
