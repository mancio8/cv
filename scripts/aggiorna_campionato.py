
import json
import time
from html.parser import HTMLParser
from pathlib import Path

import requests


# ============================================================
# CONFIGURAZIONE
# ============================================================

BASE_URL = "https://gare.lnd.it/competizione/campania"

CAMPIONATO = "2C"
GIRONE = "C"
STAGIONE = "2026"

NUM_GIORNATE = 13

OUTPUT_FILE = (
    Path(__file__).resolve().parent.parent
    / "public"
    / f"campionato_{STAGIONE}_{CAMPIONATO}_{GIRONE}.json"
)

TIMEOUT = 30
PAUSA_RICHIESTE = 0.3

BASE_PARAMS = {
    "campionato": CAMPIONATO,
    "girone": GIRONE,
    "stagione": STAGIONE,
}

# Header comuni: niente versione Inertia fissa.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html, application/xhtml+xml",
}


# ============================================================
# PARSER HTML INERTIA
# ============================================================

class InertiaPageParser(HTMLParser):
    """Estrae la pagina iniziale Inertia dall'HTML."""

    def __init__(self):
        super().__init__()
        self.page = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "div" and attrs.get("id") == "app":
            raw_page = attrs.get("data-page")

            if raw_page:
                try:
                    self.page = json.loads(raw_page)
                except json.JSONDecodeError:
                    pass


# ============================================================
# SESSIONE HTTP
# ============================================================

session = requests.Session()
session.headers.update(HEADERS)

inertia_version = None


# ============================================================
# RECUPERA LA VERSIONE INERTIA CORRENTE
# ============================================================

def aggiorna_versione_inertia():
    global inertia_version

    params = {
        **BASE_PARAMS,
        "giornata": 1,
        "leg": "first",
    }

    # Richiesta HTML completa, senza header X-Inertia.
    response = requests.get(
        BASE_URL,
        params=params,
        headers=HEADERS,
        timeout=TIMEOUT,
    )

    response.raise_for_status()

    parser = InertiaPageParser()
    parser.feed(response.text)

    if not parser.page:
        raise RuntimeError(
            "Impossibile trovare il contenitore Inertia "
            "'#app' con attributo 'data-page'. "
            f"Content-Type: {response.headers.get('Content-Type')}. "
            f"Risposta: {response.text[:500]}"
        )

    inertia_version = parser.page.get("version")

    # Evita di inviare un hash obsoleto o una versione vuota.
    session.headers.pop("X-Inertia-Version", None)

    if inertia_version:
        session.headers["X-Inertia-Version"] = inertia_version

    print(
        "Versione Inertia corrente:",
        inertia_version or "(non specificata)",
    )


# ============================================================
# PREPARA GLI HEADER INERTIA
# ============================================================

def abilita_header_inertia():
    session.headers.update({
        "X-Inertia": "true",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html, application/xhtml+xml",
    })

    # Non inviamo X-Inertia-Partial-Component perché
    # non stiamo richiedendo un aggiornamento parziale.


# ============================================================
# RECUPERA UNA GIORNATA
# ============================================================

def get_giornata(giornata, leg):

    params = {
        **BASE_PARAMS,
        "giornata": giornata,
        "leg": leg,
    }

    # Un solo tentativo aggiuntivo se il server restituisce 409.
    for tentativo in range(2):

        response = session.get(
            BASE_URL,
            params=params,
            timeout=TIMEOUT,
        )

        if response.status_code == 409 and tentativo == 0:

            print(
                f"HTTP 409 per {leg}, giornata {giornata}. "
                "Aggiorno la versione Inertia e riprovo..."
            )

            location = response.headers.get(
                "X-Inertia-Location"
            )

            if location:
                print("X-Inertia-Location:", location)

            print("Risposta server:", response.text[:500])

            aggiorna_versione_inertia()
            abilita_header_inertia()

            continue

        if not response.ok:
            raise requests.HTTPError(
                f"HTTP {response.status_code} per "
                f"{leg}, giornata {giornata}. "
                f"URL: {response.url}. "
                f"Risposta: {response.text[:1000]}",
                response=response,
            )

        try:
            data = response.json()
        except ValueError as exc:
            raise RuntimeError(
                f"La risposta per {leg}, giornata {giornata} "
                "non è JSON valido. "
                f"Content-Type: "
                f"{response.headers.get('Content-Type')}. "
                f"Risposta: {response.text[:500]}"
            ) from exc

        if not isinstance(data, dict) or "props" not in data:
            raise RuntimeError(
                f"Risposta Inertia non valida per "
                f"{leg}, giornata {giornata}. "
                f"Chiavi ricevute: "
                f"{list(data.keys()) if isinstance(data, dict) else type(data)}"
            )

        return data

    raise RuntimeError(
        f"Richiesta fallita anche dopo il nuovo tentativo: "
        f"{leg}, giornata {giornata}"
    )


# ============================================================
# NORMALIZZA UNA PARTITA
# ============================================================

def normalizza_partita(match, giornata, leg, nome_leg):

    return {
        "fase": nome_leg,
        "leg": leg,
        "giornata": giornata,

        "id": match.get("id"),

        "data": match.get("date"),
        "ora": match.get("time"),

        "casa": match.get("home"),
        "trasferta": match.get("away"),

        "gol_casa": match.get("homeGoals"),
        "gol_trasferta": match.get("awayGoals"),

        "campo": match.get("field"),
        "indirizzo": match.get("fieldAddress"),

        "logo_casa": match.get("homeLogo"),
        "logo_trasferta": match.get("awayLogo"),

        "giocata": match.get("isPlayed"),
        "rinviata": match.get("isRescheduled"),

        "esito": match.get("outcome"),
        "winner": match.get("winner"),

        "live_url": match.get("liveUrl"),

        "is_live": match.get("isLive"),
        "is_rest": match.get("isRest"),

        "is_inverted": match.get("isInverted"),

        "result_state": match.get("resultState"),
    }


# ============================================================
# SCRITTURA ATOMICA DEL JSON
# ============================================================

def salva_json(output):

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_temporaneo = OUTPUT_FILE.with_suffix(
        OUTPUT_FILE.suffix + ".tmp"
    )

    try:
        with open(
            file_temporaneo,
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                output,
                f,
                ensure_ascii=False,
                indent=2,
            )
            f.write("\n")

        # Sostituisce il file precedente solo dopo
        # aver completato correttamente la scrittura.
        file_temporaneo.replace(OUTPUT_FILE)

    finally:
        if file_temporaneo.exists():
            file_temporaneo.unlink()


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("AGGIORNAMENTO CAMPIONATO")
    print("=" * 60)

    print(f"Campionato : {CAMPIONATO}")
    print(f"Girone     : {GIRONE}")
    print(f"Stagione   : {STAGIONE}")
    print()

    # --------------------------------------------------------
    # VERSIONE INERTIA
    # --------------------------------------------------------

    print("Recupero versione Inertia...")

    aggiorna_versione_inertia()
    abilita_header_inertia()

    # --------------------------------------------------------
    # CLASSIFICA
    # --------------------------------------------------------

    print()
    print("Recupero classifica...")

    data = get_giornata(1, "first")

    standings = data["props"].get("standings")

    if not isinstance(standings, (list, dict)) or not standings:
        raise RuntimeError(
            "La risposta non contiene una classifica valida."
        )

    print(
        f"Classifica recuperata: {len(standings)} squadre"
    )

    # --------------------------------------------------------
    # CALENDARIO
    # --------------------------------------------------------

    calendario = []
    errori = []

    for leg, nome_leg in [
        ("first", "andata"),
        ("second", "ritorno"),
    ]:

        print()
        print("=" * 40)
        print(nome_leg.upper())
        print("=" * 40)

        for giornata in range(1, NUM_GIORNATE + 1):

            print(
                f"Recupero {nome_leg} - "
                f"giornata {giornata}/{NUM_GIORNATE}..."
            )

            try:
                data = get_giornata(
                    giornata,
                    leg,
                )

                matches = data["props"].get("matches")

                if not isinstance(matches, list):
                    raise RuntimeError(
                        "La risposta non contiene "
                        "un elenco valido di partite."
                    )

                print(f"  -> {len(matches)} partite")

                for match in matches:
                    calendario.append(
                        normalizza_partita(
                            match,
                            giornata,
                            leg,
                            nome_leg,
                        )
                    )

            except Exception as e:
                errore = (
                    f"{nome_leg} giornata {giornata}: {e}"
                )

                print(f"  ERRORE: {errore}")
                errori.append(errore)

            time.sleep(PAUSA_RICHIESTE)

    # --------------------------------------------------------
    # CONTROLLO COMPLETEZZA
    # --------------------------------------------------------

    print()

    if errori:

        print("=" * 60)
        print("ERRORE: ESTRAZIONE INCOMPLETA")
        print("=" * 60)

        for errore in errori:
            print(f"- {errore}")

        print()
        print(
            "Il JSON NON verrà aggiornato "
            "per evitare di pubblicare dati incompleti."
        )

        raise RuntimeError(
            f"Estrazione incompleta: {len(errori)} errori"
        )

    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------

    output = {
        "campionato": CAMPIONATO,
        "girone": GIRONE,
        "stagione": int(STAGIONE),

        "giornate_andata": NUM_GIORNATE,
        "giornate_ritorno": NUM_GIORNATE,

        "classifica": standings,
        "calendario": calendario,
    }

    salva_json(output)

    # --------------------------------------------------------
    # RISULTATO
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("ESTRAZIONE COMPLETATA")
    print("=" * 60)

    print(f"Squadre       : {len(standings)}")
    print(f"Partite       : {len(calendario)}")
    print(
        f"Giornate      : "
        f"{NUM_GIORNATE} + {NUM_GIORNATE}"
    )
    print(f"File          : {OUTPUT_FILE}")

    print("=" * 60)


if __name__ == "__main__":
    main()
