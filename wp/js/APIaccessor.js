function getAPIhost() {
    return "http://" + window.location.hostname + ":3000"
}
async function getProducts() {
    var apihost = getAPIhost();
    var result = fetch(apihost + "/v1/products")
    return (await result).json()

}
async function getProduct(id = 0) {
    var apihost = getAPIhost();
    return (await fetch(apihost + "/v1/product?id=" + id)).json()
}

window.addEventListener("load", async () => {
    console.log(await getProducts());
    console.log(await getProduct(2));
})