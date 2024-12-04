import { getProducts, postForm } from "./APIaccessor.js";

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
            option.value = product.id;
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
            option.value = product.id;
            option.textContent = product.name;
            selectElement.appendChild(option);
        });
    } catch (error) {
        console.error("Error loading crop options:", error);
    }
}


async function submitCropForm() {
    // フォーム要素を取得
    const formElement = document.getElementById('cropForm');

    // 作物データを収集
    const crops = Array.from(formElement.querySelectorAll('.record-container'))
        .filter(container => container.querySelector('select') && container.querySelector('input[name="area"]'))
        .map(container => {
            return {
                id: parseInt(container.querySelector('select').value, 10), // 選択した product.id を取得
                amount: parseFloat(container.querySelector('input[name="area"]').value) || 0 // 面積
            };
        });

    // 労働人数を取得
    const manpower = parseInt(formElement.querySelector('input[name="labor"]').value, 10) || 0;

    // 送信データの形式を整える
    const formData = {
        id: null,
        product_array: crops, // 作物リスト
        manpower: manpower // 労働人数
    };

    // データ送信
    try {
        await postForm(formData);
    } catch (error) {
        console.error("Error submitting the form:", error);
    }
    console.log("Form submitted successfully:", formData);
}

// フォームの送信ボタンにイベントリスナーを追加
document.getElementById('cropForm').addEventListener('submit', async (event) => {
    event.preventDefault(); // ページのリロードを防ぐ
    await submitCropForm();
});
