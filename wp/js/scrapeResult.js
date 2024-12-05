import { getProducts, getScrape } from "./APIaccessor.js";

window.onload = function () {
    Main();
}

function populateScraperResult(products, scraped) {
    // scraperResult の要素を取得
    const scraperResult = document.getElementById("scraperResult");
    if (!scraperResult) return;

    // テーブルを初期化
    scraperResult.innerHTML = "";

    // 一致するデータを抽出しテーブルに追加
    products.forEach(product => {
        // scraped.id を数値型の ID として扱う場合に調整
        const matchingScraped = scraped.find(item => parseInt(item.id) === product.ID);

        // 「_f」がつくIDを検索
        const matchingFertilizer = scraped.find(item => item.id === `${product.ID}_f`);

        if (matchingScraped) {
            const row = document.createElement("tr");

            // 作物名
            const nameCell = document.createElement("td");
            nameCell.textContent = product.name;

            // 種苗価格
            const seedPriceCell = document.createElement("td");
            seedPriceCell.textContent = matchingScraped.price;

            // 肥料価格
            const fertilizerPriceCell = document.createElement("td");
            fertilizerPriceCell.textContent = matchingFertilizer
                ? matchingFertilizer.price
                : "未設定"; //ないものもあるため

            // 行にセルを追加
            row.appendChild(nameCell);
            row.appendChild(seedPriceCell);
            row.appendChild(fertilizerPriceCell);

            // テーブルに行を追加
            scraperResult.appendChild(row);
        }
    });
}


async function Main() {
    // const products = (await getProducts()).body;
    // const scraped = (await getScrape()).body;
    const products = JSON.parse(`[{"ID":1,"name":"あんぽ柿","summary":"品種は平核無柿、蜂屋柿など","desc":null,"product_categories_ID":1,"yen_per_kg":78,"kg_per_1a":240},{"ID":2,"name":"いちご","summary":"品種はとちおとめ、さちのか、など","desc":null,"product_categories_ID":2,"yen_per_kg":218,"kg_per_1a":1190},{"ID":3,"name":"いんげん","summary":"品種はいちず、鴨川グリーンなど","desc":null,"product_categories_ID":2,"yen_per_kg":72,"kg_per_1a":8678},{"ID":4,"name":"きゅうり","summary":"品種はアンコール10、パイロット2号、南極1号など","desc":null,"product_categories_ID":2,"yen_per_kg":580,"kg_per_1a":233},{"ID":5,"name":"さくらんぼ","summary":"品種は佐藤錦など","desc":null,"product_categories_ID":1,"yen_per_kg":2835,"kg_per_1a":40},{"ID":6,"name":"さやえんどう","summary":"品種は姫みどり、ゆうさやなど","desc":null,"product_categories_ID":2,"yen_per_kg":43,"kg_per_1a":1157},{"ID":7,"name":"しいたけ","summary":null,"desc":null,"product_categories_ID":3,"yen_per_kg":822,"kg_per_1a":928},{"ID":8,"name":"春菊","summary":null,"desc":null,"product_categories_ID":2,"yen_per_kg":119,"kg_per_1a":516},{"ID":9,"name":"西洋なし","summary":"品種はラ・フランス、ル・レクチェ、ゼネラル・レクラークなど","desc":null,"product_categories_ID":1,"yen_per_kg":157,"kg_per_1a":373},{"ID":10,"name":"ニラ","summary":"品種はワンダーグリーン、パワフルグリーンベルトなど","desc":null,"product_categories_ID":2,"yen_per_kg":168,"kg_per_1a":546},{"ID":11,"name":"花わさび","summary":null,"desc":null,"product_categories_ID":2,"yen_per_kg":3039,"kg_per_1a":6000},{"ID":12,"name":"ピーマン","summary":null,"desc":null,"product_categories_ID":2,"yen_per_kg":346,"kg_per_1a":346},{"ID":13,"name":"ぶどう","summary":"品種は巨峰、高尾など","desc":null,"product_categories_ID":1,"yen_per_kg":94,"kg_per_1a":1062},{"ID":14,"name":"桃","summary":"品種はあかつき、川中島白桃、ゆうぞらなど","desc":null,"product_categories_ID":1,"yen_per_kg":158,"kg_per_1a":695},{"ID":15,"name":"りんご","summary":"品種は王林、ふじなど","desc":null,"product_categories_ID":1,"yen_per_kg":159,"kg_per_1a":287}]`);
    const scraped = JSON.parse(`[{"id":"2_f","price":4410},{"id":"2","price":2364.59},{"id":"4_f","price":1797.22},{"id":"4","price":539},{"id":"3","price":256},{"id":"5","price":2268.33},{"id":"8_f","price":4410},{"id":"7","price":319},{"id":"8","price":2798},{"id":"9","price":1113.18},{"id":"1","price":7747.09},{"id":"11","price":1278.1},{"id":"12","price":4740},{"id":"6","price":1467},{"id":"13","price":3515},{"id":"14","price":2741},{"id":"5_f","price":1849.96},{"id":"1_f","price":3639.57},{"id":"3_f","price":1963.64},{"id":"7_f","price":4678.02},{"id":"12_f","price":5610.02},{"id":"10","price":3047.29},{"id":"9_f","price":2992.64},{"id":"11_f","price":1678.38},{"id":"13_f","price":9782.85},{"id":"14_f","price":2080.24}]`)
    console.log(products);
    console.log(scraped);
    populateScraperResult(products, scraped);
}
