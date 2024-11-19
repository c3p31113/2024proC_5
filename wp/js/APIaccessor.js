export function getAPIhost() {
    return "http://" + window.location.hostname + ":3000"
}
export async function getProducts() {
    var apihost = getAPIhost();
    var result = fetch(apihost + "/v1/products")
    return (await result).json()

}
export async function getProduct(id = 0) {
    var apihost = getAPIhost();
    return (await fetch(apihost + "/v1/product?id=" + id)).json()
}
export async function getProductCategories() {
    var apihost = getAPIhost();
    var result = fetch(apihost + "/v1/productCategories")
    return (await result).json()

}
export async function getProductCategory(id = 0) {
    var apihost = getAPIhost();
    return (await fetch(apihost + "/v1/productCategory?id=" + id)).json()
}