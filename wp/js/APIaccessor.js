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
    const apihost = getAPIhost();
    if (typeof (form.manpower) != "number" || typeof (form.product_array) != "object") {
        console.error({ "wrong form format": form })
    }
    post("/v1/form", form)
}