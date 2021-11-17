window.onload = main;

function main() {
    Promise.all([
        fetch('https://threefoldfoundation.github.io/tft-price/tftprice.json'),
        fetch('https://api.coinbase.com/v2/prices/spot?currency=USD'),
        fetch('/gettft/prices/date/')
    ])
        .then(results => Promise.all(results.map(res => res.json())))
        .then(([{ btc }, { data: { amount } }, { date }]) => {
            const tftPrice = +amount / btc;
            document.getElementById("tft-price").textContent = " = " + tftPrice.toFixed(6);

            document.getElementById('price').innerHTML = `
                <p>
                1 TFT = ${(+amount / btc).toFixed(9)} USD <br />
                    <span class="validity">These prices will be valid till ${date} 16:00 CET.</span>
                </p>
            `;
        })
        .catch(err => {
            console.log("Error", err)
            document.getElementById('price').innerHTML = `
                <p>
                    Failed to get prices.
                </p>
            `;
        })
}

const btn = document.querySelector("button.mobile-menu-button");
const menu = document.querySelector(".mobile-menu");

btn.addEventListener("click", () => {
    menu.classList.toggle("hidden");
});