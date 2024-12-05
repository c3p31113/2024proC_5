//@ts-check
/**
 * @typedef {{id: number, name: string, summary: string | null, desc: string | null, product_categories_ID : number, yen_per_kg: number, yen_per_1a : number}} Product
 * @typedef {{id: number, name: string, summary: string}} ProductCategory
 * @typedef {{id: number, manpower: number, product_array : Array<ProductInForm>}} Form
 * @typedef {{id: null, manpower: number, product_array : Array<ProductInForm>}} SendingForm
 * @typedef {{id: number, amount: number}} ProductInForm
 * @typedef {{id: number, email_address: string, form_id: number | null, title : string, content: string}} Contact
 * @typedef {{message: string, body: Array<Product>}} APIResponseProducts
 * @typedef {{message: string, body: Product}} APIResponseProduct
 * @typedef {{message: string, body: Array<ProductCategory>}} APIResponsePProductCategories
 * @typedef {{message: string, body: ProductCategory}} APIResponsePProductCategory
 * @typedef {{id: number, price: number}} ProductInScrape
 * @typedef {{message: string, body: Array<ProductInScrape>}} APIResponseScrape
*/
/**
 * 
 * @returns {Promise<APIResponseProducts>}
 */
export async function getProducts() {
    let products = await get(`/v1/products`)
    console.log(products.status);
    return products.json()
}

/**
 * 
 * @param {number} id 
 * @returns {Promise<APIResponseProduct>} 
 */
export async function getProduct(id = 0) {
    return (await get(`/v1/products/${id}`)).json()
}

/**
 * 
 * @returns {Promise<APIResponsePProductCategories>}
 */
export async function getProductCategories() {
    return (await get(`/v1/productCategories`)).json()
}

/**
 * 
 * @param {number} id 
 * @returns {Promise<APIResponsePProductCategory>}
 */
export async function getProductCategory(id = 0) {
    return (await get(`/v1/productCategories/${id}`)).json()
}
/**
 * 
 * @returns {Promise<APIResponseScrape>}
 */
export async function getScrape() {
    return (await get("/v1/scrape")).json();
}

/**
 * @param {SendingForm} form
 */
export async function postForm(form) {
    if (typeof (form.manpower) != "number" || typeof (form.product_array) != "object") {
        console.error({ "message": "wrong form format", "form": form });
    }
    post(form, "/v1/forms")
}

/**
 * @param {Contact} contact
 */
export async function postContact(contact) {
    if (typeof (contact.email_address) != "string" || typeof (contact.title) != "string" || typeof (contact.content) != "string") {
        console.error({ "message": "wrong form format", "form": contact });
    }
    post(contact, "/v1/contacts")
}

export async function downloadResult() {
    const response = await fetch(getAPIhost() + "/v1/get_file", {
        method: "GET",
        headers: {
            "Content-Type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "Content-Disposition": "attachment;"
        }
    });
    if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "result.docx";
        a.click();
    }
}
function getAPIhost() {
    return `http://${window.location.hostname}:3000`;
}

async function get(path = "/") {
    return await fetch(getAPIhost() + path, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
}

async function post(content, path = getAPIhost()) {
    return await fetch(getAPIhost() + path, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(content)
    })
}
