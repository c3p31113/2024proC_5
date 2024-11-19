export function getAPIhost() {
    return "http://" + window.location.hostname + ":3000"
}
export async function getProducts() {
    const apihost = getAPIhost();
    var result = fetch(apihost + "/v1/products")
    return (await result).json()

}
export async function getProduct(id = 0) {
    const apihost = getAPIhost();
    return (await fetch(apihost + "/v1/product?id=" + id)).json()
}
export async function getProductCategories() {
    const apihost = getAPIhost();
    var result = fetch(apihost + "/v1/productCategories")
    return (await result).json()

}
export async function getProductCategory(id = 0) {
    const apihost = getAPIhost();
    return (await fetch(apihost + "/v1/productCategory?id=" + id)).json()
}
async function post(path, content) {
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
    post("/v1/form", form)
}

export async function postContact(contact) {
    if (typeof (contact.email_address) != "string" || typeof (contact.title) != "string" || typeof (contact.content) != "string") {
        console.error({ "message": "wrong form format", "form": form });
    }
    post("/v1/contact", contact)
}