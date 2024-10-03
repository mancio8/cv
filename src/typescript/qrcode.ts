import QRCode from "qrcode";
document.addEventListener("DOMContentLoaded", function () {
    const generateButton = document.getElementById("generate");
    const qrCodeContainer = document.getElementById("qrcode-container");
    const inputField = document.getElementById(
        "input-text"
    ) as HTMLInputElement; // Cast a HTMLInputElement

    if (generateButton && qrCodeContainer && inputField) {
        generateButton.addEventListener("click", async function () {
            const inputValue = inputField.value; // Ora `value` esiste su HTMLInputElement
            if (inputValue) {
                try {
                    const qrCodeUrl = await QRCode.toDataURL(inputValue);
                    qrCodeContainer.innerHTML = `<img src="${qrCodeUrl}" alt="QR Code">`;
                } catch (error) {
                    console.error(
                        "Errore durante la generazione del QR Code:",
                        error
                    );
                }
            }
        });
    }
});