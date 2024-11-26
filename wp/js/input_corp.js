import { getProducts } from "./APIaccessor.js";

window.onload = function () {
    loadCropOptions("cropinput");
    document.getElementById('addCropButton').addEventListener('click', addCropArea);
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
async function addCropArea() {
    const container = document.createElement('div');
    container.className = 'record-container';
    container.innerHTML = `
        <select name="crop" class="dynamic-crop-select">
        </select>
        <input type="number" name="area" placeholder="面積">
        <span class="unit">a(アール)</span>
    `;
    const cropForm = document.getElementById('cropForm');
    cropForm.insertBefore(container, document.querySelector('.labor'));

    // 新しく追加した<select>にオプションをロード
    const newSelect = container.querySelector('.dynamic-crop-select');
    loadCropOptionsToSelect(newSelect);
}

async function loadCropOptionsToSelect(selectElement) {
    try {
        const products = await getProducts();
        console.log(products);
        selectElement.innerHTML = `<option value="None">---</option>`;

        products.body.forEach(product => {
            const option = document.createElement("option");
            option.value = product.name;
            option.textContent = product.name;
            selectElement.appendChild(option);
        });
    } catch (error) {
        console.error("Error loading crop options:", error);
    }
}
