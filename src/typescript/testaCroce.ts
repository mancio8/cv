document.addEventListener("DOMContentLoaded", () => {
    const tossButton: HTMLButtonElement | null = document.getElementById(
      "toss-button"
    ) as HTMLButtonElement;
    const resultDisplay: HTMLElement | null =
      document.getElementById("result");
    const historyList: HTMLElement | null =
      document.getElementById("history-list");

    let history: string[] = [];

    tossButton?.addEventListener("click", () => {
      const result: string = Math.random() < 0.5 ? "Testa" : "Croce";

      if (resultDisplay) {
        resultDisplay.textContent = `Risultato: ${result}`;
      }

      history.push(result);

      // Aggiorna la lista della storia
      const historyItem: HTMLLIElement = document.createElement("li");
      historyItem.textContent = result;
      historyList?.appendChild(historyItem);
    });
  });