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
