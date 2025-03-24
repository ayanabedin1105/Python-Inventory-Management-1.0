document.getElementById("add-form").addEventListener("submit", function(event) {
    event.preventDefault();
    
    let name = document.getElementById("name").value;
    let quantity = document.getElementById("quantity").value;

    fetch("/add", {
        // method: "POST",
        // body: new URLSearchParams({ name: name, quantity: quantity }),
        // headers: { "Content-Type": "application/x-www-form-urlencoded" }

        method: "POST",
        body: JSON.stringify({ name: name, quantity: quantity }),
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        let list = document.getElementById("inventory-list");
        let newItem = document.createElement("li");
        newItem.innerHTML = `${data.name} - <span class="quantity">${data.quantity}</span>`;
        list.appendChild(newItem);
    });

    document.getElementById("name").value = "";
    document.getElementById("quantity").value = "";
});

document.querySelectorAll(".delete-btn").forEach(button => {
    button.addEventListener("click", function() {
        let itemId = this.dataset.id;

        fetch(`/delete/${itemId}`, {
            method: "POST"
        })
        .then(() => {
            document.getElementById(`item-${itemId}`).remove();
        });
    });
});

document.querySelectorAll(".update-btn").forEach(button => {
    button.addEventListener("click", function() {
        let itemId = this.dataset.id;
        let newQuantity = document.querySelector(`.edit-quantity[data-id='${itemId}']`).value;

        fetch("/update", {
            method: "POST",
            body: new URLSearchParams({ id: itemId, quantity: newQuantity }),
            headers: { "Content-Type": "application/x-www-form-urlencoded" }
        })
        .then(() => {
            document.querySelector(`#item-${itemId} .quantity`).innerText = newQuantity;
        });
    });
});
