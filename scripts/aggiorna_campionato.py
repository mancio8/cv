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
TIMEOUT = 30
PAUSA_RICHIESTE = 0.3
MAX_TENTATIVI = 3

OUTPUT_FILE = (
    Path(__file__).resolve().parent.parent
    / "public"
    / f"campionato_{STAGIONE}_{CAMPIONATO}_{GIRONE}.json"
)

BASE_PARAMS = {
    "campionato": CAMPIONATO,
    "girone": GIRONE,
    "stagione": STAGIONE,
}

HEADERS_HTML = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml",
}

session = requests.Session()
session.headers.update(HEADERS_HTML)

inertia_version = None


# ============================================================
# PARSER HTML INERTIA
# Il sito LND usa:
# <script data-page="app" type="application/json">...</script>
# Non usa necessariamente un div#app con data-page JSON.
# ============================================================

class InertiaPageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.page = None
        self._capture_json_script = False
        self._script_chunks = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if (
            tag.lower() == "script"
            and attrs.get("data-page") == "app"
            and "json" in attrs.get("type", "").lower()
        ):
            self._capture_json_script = True
            self._script_chunks = []

    def handle_data(self, data):
        if self._capture_json_script:
            self._script_chunks.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "script" and self._capture_json_script:
            raw_json = "".join(self._script_chunks).strip()

            try:
                parsed = json.loads(raw_json)
                if isinstance(parsed, dict):
                    self.page = parsed
            except json.JSONDecodeError:
                self.page = None

            self._capture_json_script = False
            self._script_chunks = []


# ============================================================
# RECUPERA LA VERSIONE INERTIA DALL'HTML
# ============================================================

def recupera_versione_inertia():
    global inertia_version

    params = {
        **BASE_PARAMS,
        "giornata": 1,
        "leg": "first",
    }

    # requests.get separato: evita di inviare accidentalmente
    # gli header X-Inertia già presenti nella sessione.
    response = requests.get(
        BASE_URL,
        params=params,
        headers=HEADERS_HTML,
        timeout=TIMEOUT,
    )
    response.raise_for_status()

    parser = InertiaPageParser()
    parser.feed(response.text)

    if not parser.page:
        snippet = response.text[:1200].replace("\n", " ")
        raise RuntimeError(
            "Impossibile leggere il JSON Inertia dall'HTML LND. "
            "Atteso <script data-page=\"app\" type=\"application/json\">. "
            f"Content-Type: {response.headers.get('Content-Type')}. "
            f"Risposta iniziale: {snippet}"
        )

    inertia_version = parser.page.get("version")

    if not inertia_version:
        raise RuntimeError(
            "Il JSON Inertia è stato trovato, ma non contiene "
            "il campo 'version'. Non è possibile impostare "
            "X-Inertia-Version in modo affidabile."
        )

    print("Versione Inertia recuperata:", inertia_version)
    return inertia_version


# ============================================================
# CONFIGURA GLI HEADER INERTIA
# ============================================================

def configura_header_inertia():
    session.headers.update({
        "X-Inertia": "true",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html, application/xhtml+xml",
        "X-Inertia-Version": inertia_version,
    })

    # Non inviare X-Inertia-Partial-Component:
    # richiediamo l'intera risposta della pagina.


# ============================================================
# RECUPERA UNA GIORNATA
# ============================================================

def get_giornata(giornata, leg):
    params = {
        **BASE_PARAMS,
        "giornata": giornata,
        "leg": leg,
    }

    for tentativo in range(1, MAX_TENTATIVI + 1):
        response = session.get(
            BASE_URL,
            params=params,
            timeout=TIMEOUT,
        )

        if response.status_code == 409:
            location = response.headers.get("X-Inertia-Location")

            print(
                f"HTTP 409 per {leg}, giornata {giornata} "
                f"(tentativo {tentativo}/{MAX_TENTATIVI})."
            )

            if location:
                print("X-Inertia-Location:", location)

            print("Risposta server:", response.text[:500])

            if tentativo < MAX_TENTATIVI:
                # Rileggi l'HTML senza header Inertia e aggiorna
                # la versione prima di ripetere la richiesta.
                recupera_versione_inertia()
                configura_header_inertia()
                time.sleep(1)
                continue

        if not response.ok:
            raise requests.HTTPError(
                f"HTTP {response.status_code} per {leg}, "
                f"giornata {giornata}. URL: {response.url}. "
                f"Risposta: {response.text[:1000]}",
                response=response,
            )

        try:
            data = response.json()
        except ValueError as exc:
            raise RuntimeError(
                f"La risposta per {leg}, giornata {giornata} "
                f"non è JSON valido. Content-Type: "
                f"{response.headers.get('Content-Type')}. "
                f"Risposta: {response.text[:500]}"
            ) from exc

        if not isinstance(data, dict) or "props" not in data:
            raise RuntimeError(
                f"Risposta Inertia non valida per {leg}, "
                f"giornata {giornata}. "
                f"Chiavi ricevute: "
                f"{list(data.keys()) if isinstance(data, dict) else type(data)}"
            )

        return data

    raise RuntimeError(
        f"Richiesta fallita dopo {MAX_TENTATIVI} tentativi: "
        f"{leg}, giornata {giornata}."
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
# SALVATAGGIO ATOMICO DEL JSON
# ============================================================

def salva_json(output):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    file_temporaneo = OUTPUT_FILE.with_suffix(
        OUTPUT_FILE.suffix + ".tmp"
    )

    try:
        with open(file_temporaneo, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
            f.write("\n")

        # Il file esistente viene sostituito solo dopo la scrittura.
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
    recupera_versione_inertia()
    configura_header_inertia()

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

    print(f"Classifica recuperata: {len(standings)} squadre")

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
                data = get_giornata(giornata, leg)
                matches = data["props"].get("matches")

                if not isinstance(matches, list):
                    raise RuntimeError(
                        "La risposta non contiene un elenco "
                        "valido di partite."
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

            except Exception as exc:
                errore = f"{nome_leg} giornata {giornata}: {exc}"
                print(f"  ERRORE: {errore}")
                errori.append(errore)

            time.sleep(PAUSA_RICHIESTE)

    # --------------------------------------------------------
    # NON PUBBLICARE DATI INCOMPLETI
    # --------------------------------------------------------
    if errori:
        print()
        print("=" * 60)
        print("ERRORE: ESTRAZIONE INCOMPLETA")
        print("=" * 60)

        for errore in errori:
            print(f"- {errore}")

        raise RuntimeError(
            f"Estrazione incompleta: {len(errori)} errori. "
            "Il JSON esistente non verrà aggiornato."
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

    print()
    print("=" * 60)
    print("ESTRAZIONE COMPLETATA")
    print("=" * 60)
    print(f"Squadre       : {len(standings)}")
    print(f"Partite       : {len(calendario)}")
    print(f"Giornate      : {NUM_GIORNATE} + {NUM_GIORNATE}")
    print(f"File          : {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
