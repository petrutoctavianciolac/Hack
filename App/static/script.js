document.addEventListener("DOMContentLoaded", () => {
    // Messages for the avizier
    const messages = [
        {
            title: "Ședință cu părinții",
            description: "Ședința va avea loc în sala mare pe data de 12 Decembrie 2024 la ora 18:00. Vă rugăm să nu lipsiți.",
        },
        {
            title: "Concurs de desen",
            description: "Se organizează un concurs de desen pentru elevii claselor primare. Termen limită: 20 Decembrie 2024.",
        },
        {
            title: "Anunț important",
            description: "Vineri, 15 Decembrie, școala va fi închisă din cauza lucrărilor de mentenanță.",
        },
    ];

    // Select the container where the tickets will be displayed
    const avizierContainer = document.querySelector(".avizier");

    // If the container exists, render the messages as tickets
    if (avizierContainer) {
        messages.forEach((message, index) => {
            // Create a ticket for each message
            const ticket = document.createElement("div");
            ticket.classList.add("ticket");
            ticket.dataset.index = index; // Store the index for the click event

            // Add the title to the ticket
            const title = document.createElement("div");
            title.classList.add("ticket-title");
            title.textContent = message.title;

            ticket.appendChild(title);
            avizierContainer.appendChild(ticket);
        });

        // Add click event listener to tickets
        // Add click event listener to tickets
avizierContainer.addEventListener("click", (event) => {
    const ticket = event.target.closest(".ticket");
    if (ticket) {
        // Preia datele din atributele `data-*` ale ticket-ului
        const message = {
            title: ticket.dataset.title,
            description: ticket.dataset.description,
            status: ticket.dataset.status,
            date: ticket.dataset.date,
        };

        // Deschide modalul cu informațiile preluate
        openModal(message);
    }
});

    }

    // Modal and button functionality
    const messageModal = document.getElementById("messageModal");
    const modalTitle = document.getElementById("modalTitle");
    const modalDescription = document.getElementById("modalDescription");
    const acceptButton = document.getElementById("acceptButton");

    // Function to open the modal and populate it with message details
    function openModal(message) {
        modalTitle.textContent = message.title;
        modalDescription.textContent = message.description;
    
        // Afișează statusul și data, dacă sunt necesare
        const modalStatus = document.getElementById("modalStatus");
        const modalDate = document.getElementById("modalDate");
    
        if (modalStatus) modalStatus.textContent = `Status: ${message.status}`;
        if (modalDate) modalDate.textContent = `Data: ${message.date}`;
    
        // Arată modalul
        messageModal.style.display = "flex";
    }
    

    // Close the modal when clicking outside the modal content
    messageModal.addEventListener("click", (event) => {
        if (event.target === messageModal) {
            messageModal.style.display = "none"; // Close the modal
        }
    });

    // Handle other pages (Formular Cerere Ajutor and Event Creation)
    const ajutorForm = document.getElementById("ajutorForm");
    if (ajutorForm) {
        ajutorForm.addEventListener("submit", (event) => {
            event.preventDefault();

            const titlu = document.getElementById("titlu").value;
            const descriere = document.getElementById("descriere").value;

            alert(`Cererea ta a fost trimisă cu succes!\n\nTitlu: ${titlu}\nDescriere: ${descriere}`);
        });
    }

    const eventForm = document.getElementById("eventForm");
    if (eventForm) {
        eventForm.addEventListener("submit", (event) => {
            event.preventDefault();

            const titlu = document.getElementById("titlu").value;
            const descriere = document.getElementById("descriere").value;
            const data = document.getElementById("data").value;
            const locatie = document.getElementById("locatie").value;

            alert(`Eveniment '${titlu}' creat cu succes!\n\nDescriere: ${descriere}\nData: ${data}\nLocație: ${locatie}`);
        });
    }
});

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

    // Trimite formularul normal, fără a folosi fetch (deoarece formularul trimite date prin POST în mod traditional)
    const formData = new FormData(this); // FormData preia datele din formular

    // Trimiterea formularului se va face automat către backend, fără a utiliza JavaScript
    fetch("/templates/pagina_cerere", {
        method: "POST",
        body: formData  // Folosește FormData pentru a trimite datele
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById("mesaj").innerHTML = "<p style='color:green;'>Cererea a fost trimisă cu succes!</p>";
            document.getElementById("ajutorForm").reset();  // Resetează formularul
        } else {
            document.getElementById("mesaj").innerHTML = "<p style='color:red;'>A apărut o eroare: " + data.error + "</p>";
        }
    })
    .catch(error => {
        console.error("Eroare:", error);
        document.getElementById("mesaj").innerHTML = "<p style='color:red;'>A apărut o eroare la trimiterea cererii.</p>";
    });

});




/* -----------------------------AVIZIER-------------------------------*/
// Messages for the avizier
const messages = [
    {
        title: "Ședință cu părinții",
        description: "Ședința va avea loc în sala mare pe data de 12 Decembrie 2024 la ora 18:00. Vă rugăm să nu lipsiți.",
    },
    {
        title: "Concurs de desen",
        description: "Se organizează un concurs de desen pentru elevii claselor primare. Termen limită: 20 Decembrie 2024.",
    },
    {
        title: "Anunț important",
        description: "Vineri, 15 Decembrie, școala va fi închisă din cauza lucrărilor de mentenanță.",
    },
];

// Select the container where the tickets will be displayed
const avizierContainer = document.querySelector(".avizier");

// If the container exists, render the messages as tickets
if (avizierContainer) {
    messages.forEach((message, index) => {
        // Create a ticket for each message
        const ticket = document.createElement("div");
        ticket.classList.add("ticket");
        ticket.dataset.index = index; // Store the index for the click event

        // Add the title to the ticket
        const title = document.createElement("div");
        title.classList.add("ticket-title");
        title.textContent = message.title;

        ticket.appendChild(title);
        avizierContainer.appendChild(ticket);
    });

    // Add click event listener to tickets
    avizierContainer.addEventListener("click", (event) => {
        const ticket = event.target.closest(".ticket");
        if (ticket) {
            const index = ticket.dataset.index;
            const message = messages[index];

            // Open the modal and display the message details
            openModal(message, index);
        }
    });
}

// Modal and button functionality
const messageModal = document.getElementById("messageModal");
const modalTitle = document.getElementById("modalTitle");
const modalDescription = document.getElementById("modalDescription");
const acceptButton = document.getElementById("acceptButton");

// Function to open the modal and populate it with message details
function openModal(message, index) {
    modalTitle.textContent = message.title;
    modalDescription.textContent = message.description;
    
    // Reset the accept button text and class
    acceptButton.textContent = "Accept";
    acceptButton.classList.remove("accepted");

    messageModal.style.display = "flex"; // Show the modal

    // Update the accept button's behavior for this modal instance
    acceptButton.onclick = function () {
        acceptButton.textContent = "Acceptat"; // Change button text
        acceptButton.classList.add("accepted"); // Add accepted styling
        // You can also hide the modal or keep it open based on your preference
    };
}

// Close the modal when clicking outside the modal content
messageModal.addEventListener("click", (event) => {
    if (event.target === messageModal) {
        messageModal.style.display = "none"; // Close the modal
    }
});

/*----------------SCHIMBARE SCOR ATUNCI CAND DAU ACCEPT */

// Funcția care va fi apelată la click pe butonul Accept
document.getElementById("acceptButton").addEventListener("click", function() {
    // Realizează o cerere AJAX pentru a actualiza scorul
    fetch('/update_score', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ vecin_id: 1, puncte: 100 }) // Trimite vecin_id și punctele de adăugat
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Scorul a fost actualizat!');
            location.reload(); // Reîncarcă pagina pentru a vedea actualizarea scorului
        } else {
            alert('A apărut o eroare: ' + data.error);
        }
    })
    .catch(error => console.error('Error:', error));
});


document.getElementById("acceptButton").addEventListener("click", function() {
    const taskId = 1;
    const userEmail = "petruto57@gmail.com";

    fetch('/accept_task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ task_id: taskId, user_email: userEmail })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Task acceptat și notificare trimisă!');
            location.reload(); // Reîncarcă pagina
        } else {
            alert('A apărut o eroare: ' + data.error);
        }
    })
    .catch(error => console.error('Error:', error));
});
