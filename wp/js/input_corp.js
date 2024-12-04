import { getProducts, postForm } from "./APIaccessor.js";

window.onload = function () {
    loadCropOptions("cropinput");
    document.getElementById('add-button').addEventListener('click', addCropArea);
};

async function loadCropOptions(products) {
    const select = document.getElementById(products);
    try {
        const products = await getProducts();
        console.log(products);
        select.innerHTML = `<option value="None">---</option>`;

        products.body.forEach(product => {
            console.log(product.ID);
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
    const containers = Array.from(formElement.querySelectorAll('.record-container'));
    console.log(containers); // まず、取得した .record-container を確認
    const validContainers = containers.filter(container => {
        const selectExists = container.querySelector('select');
        const inputExists = container.querySelector('input[name="area"]');
        console.log(selectExists, inputExists); // select と input が存在するか確認
        return selectExists && inputExists;
    });

    console.log(validContainers); // フィルタリング後の validContainers を確認

    const crops = validContainers.map(container => {
        const selectValue = container.querySelector('select').value;
        const areaValue = container.querySelector('input[name="area"]').value;
        console.log(selectValue, areaValue); // 値を確認
        return {
            id: parseInt(selectValue, 10), // 選択した product.id を取得
            amount: parseFloat(areaValue) || 0 // 面積
        };
    });

    console.log(crops); // 最終的に作成された crops を確認

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
        // フォーム内のデータを処理
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
        const manpower = parseInt(formElement.querySelector('input[name="labor"]').value, 10);

        // 送信データの形式を整える
        const formData = {
            id: null, // IDは常に null
            product_array: crops, // 作物リスト
            manpower: manpower // 労働人数
        };

        // データ送信
        await postForm(formData);
        console.log("Form submitted successfully:", formData);
    } catch (error) {
        console.error("Error submitting the form:", error);
    }
}


// フォームの送信ボタンにイベントリスナーを追加
document.getElementById('cropForm').addEventListener('submit', async (event) => {
    event.preventDefault(); // ページのリロードを防ぐ
    await submitCropForm();
});
