
/* 
document.getElementById("ajutorForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Previne comportamentul implicit al formularului (trimiterea prin POST)

    const titlu = document.getElementById("titlu").value;
    const descriere = document.getElementById("descriere").value;

    // Trimite datele către backend folosind metoda POST prin fetch
    fetch("/templates/pagina_cerere", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            titlu: titlu,
            descriere: descriere
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Cererea a fost trimisă cu succes!");
        } else {
            alert("A apărut o eroare la trimiterea cererii.");
        }
    })
    .catch(error => {
        console.error("Eroare:", error);
        alert("A apărut o eroare.");
    });
});*/

document.getElementById("ajutorForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Previne comportamentul implicit al formularului

    const formData = new FormData(this); // Preia datele din formular

    // Trimite datele prin fetch
    fetch("/templates/pagina_cerere", {
        method: "POST",
        body: formData  // Folosește FormData pentru a trimite datele
    })
    .then(response => response.json())
    .then(data => {
        const mesajDiv = document.getElementById("mesaj");

        if (data.success) {
            mesajDiv.innerHTML = "<p style='color:green;'>Cererea a fost trimisă cu succes!</p>";
            document.getElementById("ajutorForm").reset();  // Resetează formularul
        } else {
            mesajDiv.innerHTML = "<p style='color:red;'>A apărut o eroare: " + data.error + "</p>";
        }
    })
    .catch(error => {
        console.error("Eroare:", error);
        document.getElementById("mesaj").innerHTML = "<p style='color:red;'>A apărut o eroare la trimiterea cererii.</p>";
    });
});


/* -----------------------------AVIZIER-------------------------------*/
// Selectează toate butoanele Accept
const acceptButtons = document.querySelectorAll(".acceptButton");

// Adaugă un eveniment pentru fiecare buton Accept
acceptButtons.forEach(button => {
    button.addEventListener("click", function(event) {
        event.preventDefault(); // Previne trimiterea standard a formularului
        const ticket = button.closest(".ticket");
        const ticketId = ticket.dataset.id;  // Extrage ID-ul cererii din atributul data-id

        // Trimite cererea către server
        fetch('/accept_request', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                ticket_id: ticketId
            })
        })
        .then(response => response.text())
        .then(data => {
            console.log("Cererea a fost acceptată");
            ticket.querySelector(".ticket-status").textContent = "Acceptată"; // Actualizează statusul
        })
        .catch(error => console.error("Eroare la trimiterea cererii:", error));
    });
});
