import { getProducts, postForm } from "./APIaccessor.js";

window.onload = function onload() {
    Main();
}
async function Main() {
    let products = await getProducts();
    console.log(products);
    let base = document.getElementById("main");
    let test = document.createElement("a");
    test.textContent = "hogehoge";
    base.appendChild(test);

    products.body.forEach(product => {
        let card = document.createElement("p")
        card.textContent = product.name + " " + product.summary;
        base.appendChild(card);
    });
    // postForm({
    //     "product_array": [

    //     ],
    //     "manpower": 1
    // });
}