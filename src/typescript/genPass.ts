function generatePassword(length: number): string {
    const charset: string =
      "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+";
    let password: string = "";

    for (let i = 0, n = charset.length; i < length; ++i) {
      password += charset.charAt(Math.floor(Math.random() * n));
    }

    return password;
  }

  document.addEventListener("DOMContentLoaded", () => {
    const generateButton: HTMLButtonElement | null = document.getElementById(
      "generate-password"
    ) as HTMLButtonElement;
    const passwordContainer: HTMLElement | null =
      document.getElementById("password-container");
    const copyButton: HTMLButtonElement | null = document.getElementById(
      "copy-password"
    ) as HTMLButtonElement;

    generateButton?.addEventListener("click", () => {
      const length: number =
        parseInt(
          (document.getElementById("password-length") as HTMLInputElement)
            .value,
          10
        ) || 8;
      const password: string = generatePassword(length);

      if (passwordContainer) {
        passwordContainer.textContent = `La tua password sicura: ${password}`;
      }
    });

    copyButton?.addEventListener("click", () => {
      if (passwordContainer) {
        const passwordText: string =
          passwordContainer.textContent?.replace(
            "La tua password sicura: ",
            ""
          ) || "";
        navigator.clipboard
          .writeText(passwordText)
          .then(() => {
            alert("Password copiata negli appunti!");
          })
          .catch((err) => {
            console.error("Errore nella copia della password: ", err);
          });
      }
    });
  });