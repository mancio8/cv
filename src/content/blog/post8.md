---
title: "Dal pub alla web app: come ho costruito DartMaster, il tracker per le mie partite a freccette"
slug: "dartmaster-tracker-freccette-javascript-localstorage"
description: "Come ho sviluppato DartMaster, un tracker per partite di freccette costruito in JavaScript vanilla con salvataggio in localStorage e una seconda versione privata con backend PostgreSQL e API REST per statistiche avanzate."
pubDate: "Apr 7 2026"
heroImage: "https://res.cloudinary.com/dqh1pnrdx/image/upload/v1775565019/Cv/Screenshot_From_2026-04-07_14-29-07_nqilco.png"
badge: "JavaScript"

---



Chi gioca a freccette lo sa: il momento più bello è un **180**.
Tre triple 20 perfette.

O magari un **Big Fish** da 170 per chiudere la partita.

Ma il momento più triste?

> Quando qualcuno chiede:
> **"Qual era il tuo checkout più alto?"**
> e tu devi rispondere:
> **"Non ne ho idea"**

Così, tra una birra e una partita a Cricket, è nato **DartMaster Pro**. 🎯

---

# Il problema: fogli volanti e statistiche perse

Tutto è partito da un bisogno semplice:

* selezionare i giocatori
* scegliere la modalità (X01, Cricket, Shanghai, Halve-It, Around the Clock…)
* tenere traccia dei punteggi in tempo reale

Senza:

* server
* login
* configurazioni

Apri il browser → giochi.

---

# Versione 1: landing page + app dentro un overlay

Il frontend è una **singola pagina Astro** con una landing abbastanza semplice.

La parte interessante è che **l'app vera e propria non è nella pagina principale**, ma viene caricata dentro un **overlay fullscreen** quando l'utente clicca su:

`LANCIA L'APP`

Questo approccio mi ha permesso di separare:

| Parte        | Funzione          |
| ------------ | ----------------- |
| Landing page | presentazione     |
| Overlay      | applicazione vera |

In pratica è come **lanciare un programma dentro il sito**.

---

# JavaScript puro (senza framework)

Il cuore dell'app è un file **JavaScript** che gestisce:

* creazione e selezione giocatori
* avatar personalizzati
* colori dei giocatori
* scelta modalità di gioco
* logica dei punteggi

e naturalmente:

* **bust**
* **double out**
* **checkout**
* **passaggio turno**

Ho anche implementato una **tastiera numerica personalizzata** per inserire i punteggi velocemente durante la partita.

---

# Tutto salvato nel localStorage

Per evitare qualsiasi backend ho deciso di salvare tutto nel browser:

```javascript
localStorage.setItem("dm_players_v3", JSON.stringify(players));
```

e per le rivalità tra giocatori:

```
dm_h2h_<playerA>_<playerB>
```

In questo modo:

* nessun server
* nessun database
* nessuna autenticazione

---

# I limiti del localStorage (e perché va benissimo)

Il **localStorage** è perfetto per questo tipo di app.

### Vantaggi

* nessun backend
* zero costi
* velocissimo
* i dati restano tra una sessione e l'altra

### Limiti

* circa **5–10 MB di spazio**
* **nessuna sincronizzazione tra dispositivi**
* se cancelli i dati del browser, perdi tutto

Ed è proprio da qui che è nata **la seconda versione**.

---

# Versione 2: backend con database

Dopo mesi di partite con gli amici ho iniziato a voler fare cose più avanzate:

* analizzare le statistiche
* confrontare i giocatori
* vedere i miglioramenti nel tempo
* accedere ai dati da più dispositivi

Quindi ho costruito una **seconda versione privata** con backend.

Stack utilizzato:

* **PostgreSQL**
* **Django**
* **API REST**
* autenticazione privata

Ora posso salvare:

* partite
* turni
* checkout
* statistiche avanzate

---

# Query che prima erano impossibili

Ad esempio posso chiedere al database:

```sql
SELECT player_name,
       AVG(ppr) AS media,
       COUNT(*) AS partite
FROM matches
WHERE mode = 'X01'
  AND double_out = true
GROUP BY player_name
ORDER BY media DESC;
```

Oppure analizzare:

* trend nel tempo
* checkout più frequenti
* percentuale di vittorie contro un avversario

---

# Due approcci diversi

| Versione          | localStorage   | Database         |
| ----------------- | -------------- | ---------------- |
| Setup             | Zero           | Richiede backend |
| Persistenza       | Browser locale | Globale          |
| Multi dispositivo | No             | Sì               |
| Analisi           | Base           | SQL avanzato     |
| Privacy           | Locale         | Server           |

La **versione pubblica** è pensata per giocare subito.

La **versione privata** è per il lato **maniaco delle statistiche** che c'è in me.

---

# Prossimi passi

## Versione pubblica

Vorrei aggiungere:

* export/import dati (per il backup)
* effetti sonori per checkout e Shanghai

---

## Versione privata

Sto lavorando a:


* leaderboard stagionali
* notifiche quando qualcuno batte un record

---

# Conclusione

Se volete provare **DartMaster Pro**, è disponibile online [link](https://vincenzomancinelli.it/darts).

* gratis
* nessuna email
* nessun tracking

I dati restano **nel vostro browser**, come una tacca sulla porta di un pub.

---

🎯 **Buone freccette a tutti.**

PS:
Il codice della versione **localStorage** è su GitHub.
Quella con database… resta privata. 😉
