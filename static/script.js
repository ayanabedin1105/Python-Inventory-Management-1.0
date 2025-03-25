document.getElementById("add-form").addEventListener("submit", function(event) {
    event.preventDefault();
    
    let name = document.getElementById("name").value;
    let quantity = document.getElementById("quantity").value;

    fetch("/add", {
        method: "POST",
        body: JSON.stringify({ name: name, quantity: quantity }),
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(() => location.reload());
});

document.querySelectorAll(".delete-btn").forEach(button => {
    button.addEventListener("click", function() {
        let itemId = this.dataset.id;

        fetch(`/delete/${itemId}`, { method: "POST" })
        .then(() => location.reload());
    });
});

document.querySelectorAll(".update-btn").forEach(button => {
    button.addEventListener("click", function() {
        let itemId = this.dataset.id;
        let newQuantity = document.querySelector(`.edit-quantity[data-id='${itemId}']`).value;

        fetch("/update", {
            method: "POST",
            body: JSON.stringify({ id: itemId, quantity: newQuantity }),
            headers: { "Content-Type": "application/json" }
        })
        .then(() => location.reload());
    });
});
