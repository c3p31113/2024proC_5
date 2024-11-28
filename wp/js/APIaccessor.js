//@ts-check
export function getAPIhost() {
    return `http://${window.location.hostname}:3000`;
}
export async function getProducts() {
    let products = await get(`/v1/products`)
    console.log(products.status);
    return products.json()

}
export async function getProduct(id = 0) {
    return (await get(`/v1/products/${id}`)).json()
}
export async function getProductCategories() {
    return (await get(`/v1/productCategories`)).json()

}
export async function getProductCategory(id = 0) {
    return (await get(`/v1/productCategories?${id}`)).json()
}
async function get(path = getAPIhost()) {
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
export async function postForm(form) {
    if (typeof (form.manpower) != "number" || typeof (form.product_array) != "object") {
        console.error({ "message": "wrong form format", "form": form });
    }
    post("/v1/forms", form)
}

export async function postContact(contact) {
    if (typeof (contact.email_address) != "string" || typeof (contact.title) != "string" || typeof (contact.content) != "string") {
        console.error({ "message": "wrong form format", "form": contact });
    }
    post("/v1/contacts", contact)
}