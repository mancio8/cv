---
title: "Instance Segmentation per l’Identificazione di Oggetti in Tempo Reale nei Contesti Automobilistici"
description: "Lo scopo di questa tesi è quello di sviluppare un sistema in grado di effetuare l'istance segmentation"
pubDate: "Sep 10 2022"
heroImage: "/th.jpeg"
---

# Introduzione

Negli ultimi anni uno dei principali sforzi di innovazione nel contesto del settore automobilistico è sicuramente l'automazione della guida. Oltre a questo, sono state proposte e sono in sviluppo svariate tecnologie di assistenza alla guida che aiutano a salvare vite umane, a prevenire incidenti e a migliorare l'esperienza di guida anticipando situazioni di rischio e suggerendo o attuando correttive. Queste tecnologie consentono l'identificazione dei rischi per il veicolo, per i passeggeri del veicolo e per qualsiasi altra persona o animale in strada, oltre a determinare le opportune azioni di mitigazione del rischio.

I moderni approcci basati sull'utilizzo delle reti neurali hanno permesso la creazione di modelli sempre più accurati per risolvere problemi di regressione e classificazione. Tra i compiti particolarmente adatti ad essere risolti dalle reti neurali, in particolare le reti neurali convoluzionali che vengono utilizzate prevalentemente per l'elaborazione di immagini, è possibile citare l'object detection, la semantic segmentation e l'instance segmentation.

Più precisamente, quando abbiamo un'immagine, un problema di instance segmentation consiste nell'identificare ogni istanza di un singolo oggetto, rilevandone la posizione nell'immagine (object detection) ed identificandone la classe di appartenenza. Questo consente di differenziare ogni istanza da una qualsiasi altra istanza (anche appartenente alla medesima classe). Quest'ultimo aspetto è ciò che distingue un problema di semantic segmentation (che associa solo la stessa classe a tutte le istanze predette, essendo incapace di distinguerle) da un problema di instance segmentation (che invece entra nel merito della individualità e dunque dei confini dei singoli oggetti).

Lo scopo di questa tesi è quello di sviluppare un sistema in grado di effettuare l'instance segmentation, ovvero identificare, classificare e tracciare gli ostacoli nella scena stradale, utilizzando un insieme di dataset generati mediante il simulatore Car Learning To ACT (CARLA) per avere diversi scenari di momenti comuni di guida. Per fare ciò, vengono addestrate reti neurali profonde il cui compito è quello di identificare, in immagini e video forniti come input, aspetti utili alla classificazione, al rilevamento di oggetti, alla presenza o assenza di caratteristiche specifiche. Questo consente di realizzare approcci rivolti alla sicurezza stradale o informare algoritmi di guida autonoma che possono quindi tenere conto della presenza di elementi di specifiche classi di appartenenza durante la guida ed in tempo reale.

Gli approcci di instance segmentation basati su vari algoritmi sono stati comparati su alcuni dataset contenenti sessioni di guida (rappresentati come sequenze di immagini raccolte in un video) e per ciascun modello neurale sono state calcolate le prestazioni finali con le metriche tipicamente utilizzate in questo contesto (relative alla classificazione e sovrapposizione delle regioni di interesse).

# Background

## Carla Simulator

![](CarlaImage)

CARLA è un simulatore open source per la ricerca sulla guida autonoma.

È stato sviluppato da zero per supportare lo sviluppo, l'addestramento e la validazione di sistemi di guida autonoma urbana. Oltre al codice e ai protocolli open-source, CARLA fornisce risorse digitali aperte (layout urbano, edifici, veicoli) che sono stati creati a questo scopo e possono essere utilizzati liberamente.

La piattaforma di simulazione supporta una specificazione flessibile di suite di sensori e condizioni ambientali. Uno degli obiettivi principali di CARLA è quello di aiutare a democratizzare la ricerca e lo sviluppo della guida autonoma, fungendo da strumento facilmente accessibile e personalizzabile dagli utenti.

CARLA vanta una serie impressionante di modelli di sensori del mondo reale come telecamere, LIDAR e RADAR. Il simulatore dà anche accesso a informazioni privilegiate come la segmentazione semantica della verità di base e le informazioni sulla profondità.

Inoltre, CARLA offre una scalabilità tramite un'architettura server multi-client: più client nello stesso nodo o in nodi diversi possono controllare attori diversi. Gli attori di CARLA sono entità che interagiscono all'interno della simulazione come veicoli, pedoni e segnali di traffico.

## Machine Learning

Il campo di ricerca che studia algoritmi e sistemi in grado di apprendere dai dati è il **Machine Learning**, apprendendo una nuova conoscenza. Un sistema con queste caratteristiche, analizzando dati come input, è spesso in grado di mostrare in output dati con un livello di accuratezza vicino a quello desiderato.

È facile intuire come lo studio e lo sviluppo dell'apprendimento automatico siano diventati il punto fondamentale della ricerca sull'**Intelligenza Artificiale**, trovando soluzioni a compiti molto lunghi ed elaborati. Gli algoritmi di machine learning sono progettati per individuare schemi, classificare oggetti, prevedere risultati e prendere decisioni sulla base di dati acquisiti non necessariamente strutturati.

Possono essere impiegati uno alla volta o combinati, così da ottenere una maggiore precisione nei casi in cui vengano forniti dati complessi e più imprevedibili. Il processo di Machine Learning inizia con la raccolta e la preparazione dei dati, che possono essere numeri, immagini o testo di ogni tipo e provenienti da diverse fonti. Più dati si hanno, e migliore sarà l'affidabilità del risultato.

Un problema comune del Machine Learning è l'**overfitting**, che si verifica quando un modello di apprendimento automatico si adatta troppo ai dati di addestramento ma risulta poco generalizzabile ad altri casi. L'overfitting può verificarsi per vari motivi, tra cui:

- La dimensione dei dati di addestramento è troppo piccola e non contiene campioni di dati sufficienti per rappresentare in modo accurato tutti i possibili valori dei dati di input.
- I dati di addestramento contengono grandi quantità di informazioni irrilevanti, chiamate **dati rumorosi**.
- Il modello viene addestrato troppo a lungo su un singolo set di dati campione.

Per risolvere l'overfitting, generalmente si eliminano alcune features dal dataset di training e si elabora un nuovo modello predittivo. Il nuovo modello predittivo ottenuto con meno features è meno preciso rispetto al precedente, ma è più generale, cioè il margine di errore è minore quando lo utilizziamo sui dati di test.

Un altro problema comune del Machine Learning è l'**underfitting**, uno scenario in data science in cui un modello di dati non riesce a catturare accuratamente la relazione tra le variabili di input e output, generando un alto tasso di errore sia sul set di addestramento che sui dati non visti. Si verifica quando un modello è troppo semplice, il che può essere il risultato di un modello che ha bisogno di più tempo di addestramento, più caratteristiche di input, o meno regolarizzazione.

Dato che questo comportamento può essere osservato durante l'utilizzo del set di addestramento, i modelli sottodimensionati sono solitamente più facili da identificare rispetto a quelli sovradimensionati.

## Deep Learning

Una branca del Machine Learning è il **Deep Learning**, nata con l'obiettivo di imitare le attività e l'apprendimento del cervello umano in maniera più dettagliata attraverso l'utilizzo di un apprendimento su più livelli di astrazione. È caratterizzato dal fatto che i dati, provenienti da un livello precedente, vengono utilizzati come input di quello successivo, estraendo informazioni più complesse con l'aumentare della profondità.

Le tecniche di Deep Learning si basano sulla definizione di nuove architetture di **reti neurali artificiali** concepite per adattarsi a compiti di elaborazione specifici. Il termine "deep" deriva dal fatto che questi modelli, per eseguire compiti complessi, sono costituiti da un elevato numero di layer concatenati l'uno con l'altro. Questo consente agli strati successivi di analizzare e generare un elevato numero di caratteristiche che, a partire dalle informazioni prodotte dagli strati precedenti, possono essere utilizzate per effettuare compiti di classificazione e regressione.

Uno dei problemi del Deep Learning riguarda la complessità del modello: infatti, man mano che la profondità della rete aumenta, si ha più possibilità di causare **overfitting**.

## Reti neurali

![](reteNeurale)

Una **rete neurale artificiale** è un modello matematico ispirato a una rete neurale biologica, con l'obiettivo di riprodurre le funzioni tipiche del cervello umano. Una rete di questo tipo è realizzata, così come quella biologica, da unità semplici chiamate neuroni artificiali, caratterizzati dal fatto di avere molti ingressi e una sola uscita, calcolata dalla somma pesata degli input.

Come già accennato, le reti, applicate al **Deep Learning**, sono strutturate su più livelli, dove il grado di profondità ne determina il grado di complessità del calcolo. Nel corso degli anni, sono state realizzate diverse architetture con compiti ben precisi, dando vita a diverse reti neurali artificiali, tra cui il **MLP (Multi Layer Perceptron)** e la **CNN (Convolutional Neural Network)**.

## CNN

Una **rete neurale convoluzionale** (CNN o ConvNet, dall’inglese _convolutional neural network_) è un tipo di rete neurale di tipo feed-forward ispirata all’organizzazione della corteccia visiva. La CNN funziona, in generale, come tutte le altre reti feed-forward: è costituita da un blocco di input, uno o più blocchi nascosti (_hidden layer_), che effettuano calcoli tramite funzioni di attivazione (ad esempio _RELU_), e un blocco di output che effettua la classificazione vera e propria.

Una rete neurale feed-forward è un tipo di rete neurale artificiale in cui le connessioni tra i nodi non formano cicli. Le informazioni si muovono solo in una direzione, dai nodi d’ingresso, attraverso nodi nascosti (se esistenti), fino ai nodi d’uscita.

La differenza rispetto alle classiche reti feed-forward è rappresentata dalla presenza dei livelli di convoluzione. Le CNN sono costituite da tre tipi principali di livelli:

- **Layer convoluzionale**: l'elemento costitutivo principale di una CNN. È qui che viene calcolata la convoluzione dell'input sulla base dei valori di uno o più filtri, appresi durante la fase di addestramento.
- **Layer di pooling**: riduce la dimensione spaziale delle rappresentazioni correnti (i volumi di uno specifico stadio della rete). Questo serve per ridurre il numero di parametri, il tempo computazionale, e per tenere sotto controllo l'overfitting.
- **Layer completamente connesso**: a ogni livello, la complessità della CNN aumenta, così come la porzione dell’immagine identificata. I primi livelli si concentrano su caratteristiche semplici (ad esempio, colori e contorni), mentre i livelli successivi riconoscono forme più grandi fino all'identificazione finale dell’oggetto.

Le CNN classificano le immagini basandosi su particolari caratteristiche, come i contorni delle figure, le linee orizzontali, verticali, diagonali e altro ancora. Sono uno degli algoritmi di **Deep Learning** più utilizzati nella **computer vision**, applicati in diversi campi: dalle automobili autonome ai droni, dalle diagnosi mediche al supporto per gli ipovedenti.

Le CNN furono introdotte per la prima volta nel 1989, ma solo recentemente, grazie all'aumento della potenza delle GPU e alla disponibilità di grandi quantità di dati per l'addestramento, sono state largamente utilizzate nei compiti di computer vision.

La struttura della CNN si ispira alla corteccia visiva degli animali, in cui gruppi di cellule sono sensibili a piccole sottoregioni dell'immagine in ingresso. L'immagine non viene elaborata come un singolo blocco, ma come una composizione di blocchi più piccoli.

Utilizzeremo il termine **riconoscimento di oggetti** in senso ampio, includendo sia la **classificazione delle immagini** (determinare quali classi di oggetti sono presenti) sia il **rilevamento di oggetti** (localizzare tutti gli oggetti presenti nell’immagine).

## Mask R-CNN

![]()

Nel 2014 fu proposta una rete neurale, la **Region-based Convolutional Neural Network** (R-CNN), che permetteva di risolvere problemi di object detection. Nel corso degli anni, R-CNN venne notevolmente migliorata, con l'introduzione di **Fast R-CNN** e **Faster R-CNN**, che hanno superato la versione originale sia in termini di performance che di accuratezza.

**Mask R-CNN** è un'estensione di Faster R-CNN utilizzata per problemi di **instance segmentation**. Consente di risolvere la segmentazione delle singole istanze ed è la rete neurale impiegata nell'applicazione. Una rete neurale convoluzionale può essere utilizzata per molteplici obiettivi: dalla classificazione alla segmentazione semantica delle istanze.

La **segmentazione semantica** consiste nel dividere un'immagine in insiemi di pixel opportunamente etichettati e classificati. Quando è necessario segmentare ogni singola istanza (**instance segmentation**), l'obiettivo diventa differenziare ogni oggetto identificato (object detection) e classificato, determinandone l'esatta posizione e distinguendolo da qualsiasi altro oggetto, anche appartenente alla stessa classe.

---

## Segmentazione

![]()

La segmentazione delle immagini è una parte fondamentale per i sistemi di **Computer Vision** e consiste nel partizionare un'immagine in diverse regioni, rappresentanti diversi oggetti. Questo processo si basa sull'estrazione, dal dominio dell'immagine, di regioni connesse tra loro.

La segmentazione riveste un ruolo importante in molte applicazioni, come immagini mediche e realtà aumentata. Sono stati sviluppati numerosi algoritmi di segmentazione, dai semplici algoritmi basati su soglie o istogrammi a quelli più avanzati. Si parla di **semantic segmentation** quando l'algoritmo stabilisce anche la classe di ogni regione individuata.

Negli ultimi anni, le reti di **Deep Learning** hanno prodotto una nuova generazione di modelli di segmentazione semantica con miglioramenti significativi nelle prestazioni, raggiungendo un'elevata accuratezza.

### Proprietà di una buona segmentazione:

- Tutti i pixel devono appartenere ad almeno una regione della partizione.
- I pixel di una regione devono essere connessi.
- Le regioni devono essere separate tra loro.

### Tipi di segmentazione:

- **Semantic Segmentation**: divide l'immagine in blocchi di pixel classificati ed etichettati in una classe specifica.
- **Instance Segmentation**: identifica, classifica e differenzia ogni singolo oggetto, anche se appartenente alla stessa classe.
- **Panoptic Segmentation**: combina la segmentazione semantica e l'instance segmentation.

## Instance Segmentazione

L'**Instance Segmentation** è impegnativa perché richiede il rilevamento corretto di tutti gli oggetti in un'immagine e la loro segmentazione. Essa combina elementi classici di visione artificiale come l'**Object Detection**, in cui l'obiettivo è classificare singoli oggetti e localizzarli utilizzando un **bounding box**, e la **semantic segmentation**, in cui l'obiettivo è classificare ciascun pixel in un insieme fisso di categorie senza differenziare le istanze dell'oggetto.

Nonostante la classificazione delle immagini e l'Object Detection possano sembrare molto simili, in realtà sono due tecniche diverse. Mentre la classificazione si occupa di classificare un'immagine in una determinata categoria, l'Object Detection identifica la posizione degli oggetti all'interno di un'immagine. Le due tecniche non sono contrapposte; infatti, si utilizza la classificazione per generare informazioni sull'intera immagine e, successivamente, l'Object Detection riduce progressivamente la regione dell'immagine fino a ottenere un riquadro ben specifico al quale viene associata un'etichetta.

La **Precision-Recall curve (PR)** è una metrica utilizzata per valutare le prestazioni dei modelli di classificazione, compresi quelli utilizzati in Mask R-CNN, un tipo di modello di segmentazione e rilevamento oggetti. Per comprendere la curva Precision-Recall in Mask R-CNN, è necessario avere una comprensione di base dei seguenti concetti:

- **Precision**: La precisione misura la frazione di istanze positive (oggetti rilevati) che sono state correttamente identificate dal modello rispetto al totale delle istanze identificate come positive. In altre parole, indica quanti degli oggetti identificati come positivi dal modello sono effettivamente oggetti veri positivi.


\[Prec = \frac{Tp}{Tp+Fp}\]



    - **TP (True Positives)**: Oggetti veri positivi (oggetti rilevati correttamente).
    - **FP (False Positives)**: Oggetti falsi positivi (oggetti identificati erroneamente come positivi).

- **Recall**: La recall, nota anche come sensibilità o tasso di vera positività, misura la frazione di istanze positive che sono state correttamente identificate dal modello rispetto al totale delle istanze positive effettive. In altre parole, indica quanti degli oggetti positivi veri sono stati rilevati dal modello.

$$
\text{Recall} = \frac{TP}{TP + FN}
$$

    - **FN (False Negatives)**: Oggetti falsi negativi (oggetti non rilevati).

La Precision-Recall curve è creata variando la soglia di confidenza del modello per la classificazione degli oggetti. Per ogni valore della soglia, il modello può produrre un diverso set di predizioni positive e quindi calcolare la precisione e il richiamo corrispondenti. Si effettua il plot di questi punti per varie soglie e così si crea la curva PR. Questa curva fornisce una rappresentazione della trade-off tra la precisione e il richiamo del modello a diverse soglie di confidenza.


## Average Precision


L'AP è una metrica che misura la precisione media delle previsioni di istanze. È spesso calcolato a diverse soglie di IOU e quindi aggregato per ottenere un valore complessivo. Viene utilizzato per valutare la precisione delle previsioni a varie soglie di sovrapposizione. L'Average Precision è stata calcolata con un IOU del 50%.

L'indice di sovrapposizione (IoU) viene calcolato utilizzando la formula:

$$
IOU= \frac{\text{Area di Sovrapposizione}}{\text{Area di Unione}}
$$

L'IoU restituisce un valore compreso tra 0 e 1, dove 1 indica una perfetta sovrapposizione tra le maschere previste e di riferimento, mentre 0 indica nessuna sovrapposizione.

## Confusion Matrix


La matrice di confusione è una metrica comunemente utilizzata per valutare le prestazioni dei modelli di classificazione, ma può anche essere adattata per valutare i modelli di instance segmentation in modo più generale. Tuttavia, la segmentazione di istanze è una sfida più complessa rispetto alla classificazione, poiché coinvolge la previsione delle maschere pixel per pixel per diverse istanze di oggetti all'interno di un'immagine. Pertanto, la matrice di confusione può essere meno diretta in questo contesto, ma può ancora fornire informazioni utili.

La confusion matrix è composta da classi di oggetto e background, in cui distinguerà le diverse classi di oggetti (come automobili, persone, animali, ecc.) e adatterà la matrice di confusione per considerare le diverse classi. La matrice conterà il numero di pixel previsti correttamente ed erroneamente per ciascuna classe e per lo sfondo (background).


## Mean Average Precision e Mean Average Recall


Il mean Average Precision è una metrica più completa che tiene conto sia della precisione che del recall del modello. Calcola la precisione media per diverse fasce di recall (punti di taglio) e quindi calcola la media di queste precisioni. La precisione misura la proporzione di istanze rilevate che sono vere (cioè la proporzione di istanze segmentate correttamente) rispetto al totale delle istanze rilevate.

Il mean Average Recall è una metrica che valuta la capacità di un modello di segmentazione delle istanze di recuperare correttamente tutte le istanze degli oggetti in una scena. Per calcolare il mAR, si calcola prima il recall per ogni classe di oggetti e quindi si calcola la media di questi recall. Misura la capacità del modello di trovare tutte le istanze di una classe.

In breve, il mAR valuta la capacità di rilevare correttamente tutte le istanze, mentre il mAP considera sia la capacità di rilevare tutte le istanze che la precisione delle rilevazioni. Entrambe le metriche sono importanti per valutare le prestazioni dei modelli di segmentazione delle istanze, e i valori ideali variano a seconda del contesto dell'applicazione.

## F-Score


L'F-score, o punteggio F, è una metrica di valutazione comunemente utilizzata per misurare la precisione e il richiamo di un modello di instance segmentation. Questa metrica è particolarmente utile quando si tratta di problemi di segmentazione di istanze, in cui l'obiettivo è individuare e distinguere diverse istanze di oggetti all'interno di un'immagine.

L'F-score è una combinazione di due metriche principali:
1. Precision
2. Recall

L'F-score combina queste due metriche per ottenere un singolo punteggio che tiene conto sia della precisione che del richiamo. È definito come la media armonica tra precisione e richiamo: 

$$
F= \frac{2 \cdot Precision \cdot Recall}{Precision + Recall}
$$

L'uso dell'F-score è utile perché bilancia la precisione e il richiamo, fornendo una valutazione complessiva delle prestazioni del modello di instance segmentation. Un punteggio F elevato indica una buona capacità del modello di identificare e distinguere le istanze di oggetti, mentre un punteggio basso può indicare problemi di sovrapposizione, sotto-segmentazione o sovra-segmentazione delle istanze.
