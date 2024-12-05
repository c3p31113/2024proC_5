import { getProducts, getScrape } from "./APIaccessor.js";

window.onload = function () {
    Main();
}

async function Main() {
    const products = (await getProducts()).body;
    const scraped = (await getScrape()).body;
    console.log(products);
    console.log(scraped);
}
