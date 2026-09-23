import json
import time
from pathlib import Path

import requests


# ============================================================
# CONFIGURAZIONE
# ============================================================

BASE_URL = "https://gare.lnd.it/competizione/campania"

CAMPIONATO = "EC"
GIRONE = "A"
STAGIONE = "2026"

NUM_GIORNATE = 17

OUTPUT_FILE = (
    Path(__file__).resolve().parent.parent
    / "public"
    / f"campionato_{STAGIONE}_{CAMPIONATO}_{GIRONE}.json"
)


HEADERS = {
    "X-Inertia": "true",
    "X-Inertia-Partial-Component": "QuadroGare/Home",
    "X-Inertia-Version": "403fab3dc930215651901db39d6904cf",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "text/html, application/xhtml+xml",
}


BASE_PARAMS = {
    "campionato": CAMPIONATO,
    "girone": GIRONE,
    "stagione": STAGIONE,
}


# ============================================================
# SESSIONE HTTP
# ============================================================

session = requests.Session()
session.headers.update(HEADERS)


# ============================================================
# RECUPERA GIORNATA
# ============================================================

def get_giornata(giornata, leg):

    params = {
        **BASE_PARAMS,
        "giornata": giornata,
        "leg": leg,
    }

    response = session.get(
        BASE_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if "props" not in data:
        raise RuntimeError(
            f"Risposta Inertia non valida "
            f"per {leg} giornata {giornata}"
        )

    return data


# ============================================================
# ESTRAI PARTITA
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
    # CLASSIFICA
    # --------------------------------------------------------

    print("Recupero classifica...")

    try:
        data = get_giornata(1, "first")

        standings = data["props"].get("standings")

        if standings is None:
            raise RuntimeError(
                "La risposta non contiene 'standings'"
            )

    except Exception as e:

        raise RuntimeError(
            f"Impossibile recuperare la classifica: {e}"
        ) from e

    print(
        f"Classifica recuperata: "
        f"{len(standings)} squadre"
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
                f"Recupero {nome_leg} "
                f"- giornata {giornata}/{NUM_GIORNATE}..."
            )

            try:

                data = get_giornata(
                    giornata,
                    leg,
                )

                matches = data["props"].get(
                    "matches",
                    [],
                )

                print(
                    f"  -> {len(matches)} partite"
                )

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
                    f"{nome_leg} "
                    f"giornata {giornata}: {e}"
                )

                print(f"  ERRORE: {errore}")

                errori.append(errore)

            time.sleep(0.3)

    # --------------------------------------------------------
    # CONTROLLO ERRORI
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
            f"Estrazione incompleta: "
            f"{len(errori)} errori"
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

    # --------------------------------------------------------
    # CREA DIRECTORY
    # --------------------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # SCRITTURA JSON
    # --------------------------------------------------------

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            output,
            f,
            ensure_ascii=False,
            indent=2,
        )

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

    print(
        f"File          : {OUTPUT_FILE}"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()