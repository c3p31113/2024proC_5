import getProducts from "./APIaccessor.js";

window.onload = function onload() {
    Main();
}
async function Main() {
    console.log(await getProducts());
}