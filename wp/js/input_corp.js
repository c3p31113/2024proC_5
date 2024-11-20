import { getProducts } from "./APIaccessor.js";

window.onload = function () {
    loadCropOptions("cropinput");
};

async function loadCropOptions(products) {
    const select = document.getElementById(products);
    try {
        const products = await getProducts();
        console.log(products);
        select.innerHTML = `<option value="None">---</option>`;

        products.body.forEach(product => {
            const option = document.createElement("option");
            option.value = product.name;
            option.textContent = product.name;
            select.appendChild(option);
        });
    } catch (error) {
        console.error("Error loading crop options:", error);
    }
}
