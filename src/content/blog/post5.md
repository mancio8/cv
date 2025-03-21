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

### Configurare un disco esterno per l'archiviazione
Se vuoi usare un disco esterno per i tuoi file e container Docker:
1. Collega il disco al tuo OrangePi.
2. Verifica che venga riconosciuto:
   ```sh
   lsblk
   ```
3. Monta il disco (supponiamo sia `/dev/sda1`):
   ```sh
   sudo mkdir /mnt/disco
   sudo mount /dev/sda1 /mnt/disco
   ```
4. Per montarlo automaticamente all'avvio, aggiungi una riga al file `/etc/fstab`:
   ```sh
   /dev/sda1  /mnt/disco  ext4  defaults  0  2
   ```

### Backup automatico delle configurazioni
Per evitare la perdita di dati, puoi impostare un backup automatico della cartella di CasaOS:
```sh
mkdir -p /mnt/disco/backup_casaos
rsync -av --delete /etc/casaos /mnt/disco/backup_casaos/
```
Puoi automatizzare il backup con cron aggiungendo questa riga con `crontab -e`:
```sh
0 3 * * * rsync -av --delete /etc/casaos /mnt/disco/backup_casaos/
```

## 5. Installazione di Docker e container personalizzati
CasaOS utilizza Docker per gestire le app. Puoi installare manualmente un container con:
```sh
docker run -d --name nginx -p 8080:80 nginx
```
Oppure puoi usare l'interfaccia web per aggiungere e gestire container facilmente.

### Esempio: Installare un server Nextcloud
Se vuoi ospitare un'istanza di Nextcloud per la gestione dei file:
```sh
docker run -d --name nextcloud -p 8081:80 -v /mnt/disco/nextcloud:/var/www/html nextcloud
```
Ora Nextcloud sarà disponibile su `http://IP_DEL_TUO_ORANGEPI:8081`.

## Conclusione
CasaOS è un'ottima soluzione per trasformare il tuo OrangePi in un server domestico. Con pochi passaggi puoi installarlo, configurarlo e iniziare a gestire i tuoi servizi personali con una UI semplice e intuitiva.

### Possibili espansioni
- Configurare un server VPN (WireGuard o OpenVPN) per accedere ai tuoi servizi in sicurezza.
- Integrare Home Assistant per la domotica.
- Usare Pi-hole come DNS adblocker per la rete di casa.

Con queste personalizzazioni, il tuo OrangePi diventerà un vero e proprio hub per la gestione dei tuoi servizi digitali! 🚀
