---
title: "Da Flutter Starter a un'app personale completa: il mio viaggio nell'apprendimento di Flutter"
slug: "app-flutter-rifornimenti-biblioteca-habits-raccolta-differenziata"
description: "Come ho trasformato un template Flutter in un'app personale completa con gestione rifornimenti, biblioteca digitale, habit tracker e raccolta differenziata, imparando Riverpod, SharedPreferences e go_router."
pubDate: "Sep 4 2026"
heroImage: ""
badge: "Flutter"
---

## Il punto di partenza

Ho sempre voluto imparare **Flutter** e creare un'app mobile che potessi usare ogni giorno. Dopo aver studiato la documentazione e alcuni tutorial, ho deciso di partire da un progetto open source chiamato [flutter-starter-app](https://github.com/momentous-developments/flutter-starter-app), un template ben strutturato che include:

- **Riverpod** per la gestione dello stato
- **go_router** per la navigazione
- **SharedPreferences** per la persistenza locale
- **Material 3** per il design
- Supporto per **localizzazione** (inglese, spagnolo, francese)
- Struttura organizzata per **features**

Questo mi ha permesso di concentrarmi sull'imparare i concetti fondamentali senza dover configurare tutto da zero, invece di perdere tempo su boilerplate e configurazioni iniziali.

## Le funzionalità che ho implementato

### ⛽ Rifornimenti

La prima feature che ho creato è stata la gestione dei rifornimenti di carburante. Volevo tracciare:

- **Data** del rifornimento
- **Litri** inseriti
- **Costo totale**
- **Prezzo per litro** (calcolato automaticamente)
- **Chilometraggio** del veicolo
- **Tipo di carburante** (benzina, diesel, GPL, metano, elettrico)

Ho imparato a:

- Creare modelli dati immutabili
- Implementare il pattern **Repository** per separare la logica dei dati
- Usare **AsyncNotifierProvider** per gestire lo stato asincrono
- Salvare e caricare dati con **SharedPreferences**
- Creare form con validazione
- Implementare **CRUD completo** (Create, Read, Update, Delete)

### 📚 Biblioteca digitale

La seconda feature è stata una biblioteca per tracciare i libri che leggo. Ho implementato:

- **Griglia di copertine** con caricamento da URL
- **Ordinamento** per titolo, autore o data
- **Aggiunta/modifica/eliminazione** libri
- **Import/Export JSON** per backup
- **Gestione errori** per immagini non disponibili

La sfida più interessante è stata gestire il caricamento delle immagini da URL esterni. Ho dovuto:

1. Aggiungere i permessi internet nel `AndroidManifest.xml`
2. Abilitare il traffico HTTP per Android 9+
3. Implementare fallback per URL non funzionanti
4. Convertire automaticamente HTTP in HTTPS

### ♻️ Raccolta differenziata

Ho creato una pagina che mostra il calendario della raccolta differenziata del mio paese. Include:

- **Selettore giorni** con pill buttons
- **Indicatore "oggi"** sul giorno corrente
- **Schede colorate** per ogni tipo di rifiuto
- **Orari di conferimento** in evidenza
- **Gestione giorni senza raccolta**

Ogni tipo di rifiuto ha un colore specifico:

| Rifiuto | Colore |
|---|---|
| 🍃 Umido | Marrone |
| 📦 Carta | Blu |
| 🧴 Plastica | Arancione |
| 🍾 Vetro | Verde acqua |

### 🎯 Habit tracker

La feature più recente è un habit tracker per monitorare le mie abitudini quotidiane. Ho implementato:

- **Streak counter** (giorni consecutivi)
- **Obiettivi mensili** con percentuale di completamento
- **Selezione icone** (16 emoji disponibili)
- **Selezione colori** (8 colori personalizzabili)
- **Toggle giornaliero** con animazione
- **Barra di progresso** quotidiana
- **Statistiche complete** (completati oggi, miglior streak, ecc.)

### 📊 Dashboard riepilogo

Ho creato una dashboard che mostra un riepilogo di tutte le funzionalità:

- **Biblioteca**: numero di libri letti
- **Rifornimenti**: totale speso e prezzo medio
- **Raccolta**: cosa si raccoglie oggi e domani
- **Habits**: percentuale di completamento giornaliero

## Le sfide tecniche

### 1. Persistenza dei dati

Ho imparato a usare **SharedPreferences** per salvare i dati in formato JSON:

```dart
Future<void> _saveToStorage() async {
  final prefs = await SharedPreferences.getInstance();
  final String jsonString = json.encode(
    _items.map((i) => i.toJson()).toList(),
  );
  await prefs.setString(_storageKey, jsonString);
}
```

### 2. Import/Export

Ho implementato l'import/export in JSON per tutte le features, permettendo:

- Backup dei dati
- Trasferimento tra dispositivi
- Condivisione con altre app

### 3. Gestione immagini remote

Ho dovuto gestire:

- URL HTTP non sicuri su Android
- Immagini non disponibili
- Loading states
- Placeholder eleganti

### 4. Navigazione con go_router

Ho imparato a usare go_router per:

- Route con parametri
- ShellRoute per layout responsive
- Redirect per autenticazione
- Navigazione programmatica

## Le tecnologie utilizzate

- **Flutter 3.x** - Framework principale
- **Riverpod** - Gestione dello stato
- **go_router** - Navigazione
- **SharedPreferences** - Persistenza locale
- **file_picker** - Selezione file per import
- **share_plus** - Condivisione file
- **path_provider** - Accesso ai file system
- **Material 3** - Design system

## Cosa ho imparato

1. **Architettura a features**: organizzare il codice per funzionalità
2. **Repository pattern**: separare la logica dei dati dall'UI
3. **State management**: usare Riverpod in modo efficace
4. **Persistenza**: salvare e caricare dati localmente
5. **CRUD operations**: implementare operazioni complete
6. **Form validation**: gestire input utente
7. **Error handling**: gestire errori di rete e dati
8. **Responsive design**: adattare l'UI a diverse dimensioni

## Riflessioni finali

Quello che è partito come un semplice esercizio per imparare Flutter è diventato, feature dopo feature, un'app che uso davvero ogni giorno: dal calcolo del prezzo medio della benzina al promemoria di quale bidone portare fuori stasera. È stato anche un buon banco di prova per capire quando un template open source aiuta davvero (mi ha fatto risparmiare ore di setup) e quando invece serve intervenire a fondo per adattarlo alle proprie esigenze, come nel caso della gestione delle immagini remote o della struttura a feature.

## Prossimi passi

- [ ] Aggiungere autenticazione
- [ ] Implementare sincronizzazione cloud
- [ ] Aggiungere notifiche push
- [ ] Creare widget per la home screen
- [ ] Migliorare le animazioni
- [ ] Aggiungere test unitari
- [ ] Ottimizzare le performance

Tags: #flutter #dart #riverpod #mobile #app #personal-project #learning
