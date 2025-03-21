---
title: "Installazione e Configurazione di CasaOS su OrangePi"
description: "CasaOS è un sistema operativo leggero progettato per l'hosting di servizi personali su dispositivi come Raspberry Pi, OrangePi e mini-PC. In questa guida vedremo come installarlo e configurarlo su un OrangePi."
pubDate: "Mar 21 2025"
heroImage: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9T_cQQWJD5VTM5RX7qDrakwbbqsoGOrM3FA&s"
badge: "Server"
---
# Installazione e Configurazione di CasaOS su OrangePi

## Introduzione
CasaOS è un sistema operativo leggero progettato per l'hosting di servizi personali su dispositivi come Raspberry Pi, OrangePi e mini-PC. In questa guida vedremo come installarlo e configurarlo su un OrangePi.

## Requisiti
- Un dispositivo **OrangePi** (es. OrangePi 5, OrangePi Zero 2, etc.)
- Una scheda microSD (consigliato almeno **16GB**)
- Un alimentatore compatibile
- Accesso SSH al dispositivo
- Connessione a internet

## 1. Preparazione della microSD
1. Scarica **Armbian** o un'altra distribuzione Linux compatibile con il tuo modello di OrangePi da [https://www.armbian.com](https://www.armbian.com).
2. Utilizza **Balena Etcher** o **Raspberry Pi Imager** per scrivere l'immagine sulla microSD.
3. Inserisci la microSD nel tuo OrangePi e accendilo.
4. Trova l'indirizzo IP del dispositivo (puoi controllarlo nel router o usare `arp -a` da terminale).
5. Connettiti via SSH:
   ```sh
   ssh user@IP_DEL_TUO_ORANGEPI
   ```
   (Le credenziali di default per Armbian sono `root` e `1234`, dovrai cambiarle al primo accesso.)

## 2. Installazione di CasaOS
CasaOS fornisce uno script di installazione automatizzato. Per eseguirlo:
```sh
curl -fsSL https://get.casaos.io | bash
```
L'installazione durerà alcuni minuti e al termine potrai accedere all'interfaccia web.

## 3. Accesso a CasaOS
Apri un browser e vai all'indirizzo:
```
http://IP_DEL_TUO_ORANGEPI:80
```
Qui potrai completare la configurazione iniziale e iniziare a installare le app disponibili.

## 4. Configurazione avanzata
### Cambio porta di accesso
Se vuoi modificare la porta di accesso di CasaOS:
```sh
nano /etc/casaos/gateway.ini
```
Trova la riga con `port=80` e cambiala (es. `port=8080`). Poi riavvia CasaOS:
```sh
systemctl restart casaos
```
Ora CasaOS sarà accessibile su `http://IP_DEL_TUO_ORANGEPI:8080`.

### Abilitare HTTPS con un certificato SSL
Per aggiungere un certificato SSL con Let's Encrypt:
```sh
sudo apt install certbot
sudo certbot certonly --standalone -d tuodominio.com
```
Dopo aver ottenuto il certificato, configuralo con un reverse proxy come Nginx o Caddy.

## 5. Installazione di Docker e container personalizzati
CasaOS utilizza Docker per gestire le app. Puoi installare manualmente un container con:
```sh
docker run -d --name nginx -p 8080:80 nginx
```
Oppure puoi usare l'interfaccia web per aggiungere e gestire container facilmente.

## Conclusione
CasaOS è un'ottima soluzione per trasformare il tuo OrangePi in un server domestico. Con pochi passaggi puoi installarlo, configurarlo e iniziare a gestire i tuoi servizi personali con una UI semplice e intuitiva.
