setTimeout(() => {
    const message = document.getElementById('backendmessages');
    message.classList.add('opacity-0'); // Apply fade-out effect
    setTimeout(() => {
        message.style.display = 'none'; // Completely hide the element
    }, 1000); // Wait for transition duration to complete
}, 2000);

function toggleCollapsible() {
    const clickedButton = event.target;
    const content = clickedButton.nextElementSibling;
    // Toggle visibility
    content.classList.toggle('hidden');
    content.classList.toggle('block');
    // Update button text
    clickedButton.children[1].classList.toggle('fa-chevron-down');
    clickedButton.children[1].classList.toggle('fa-chevron-right');
}
const footer = document.querySelector('footer');
gsap.to(footer, {
    scrollTrigger: {
        trigger: footer,
        start: "top bottom",
        onEnter: () => gsap.fromTo(footer, {
            backgroundColor: "initial",
            color: "initial"
        }, {
            backgroundColor: "#303337",
            color: "#ffffff",
            duration: 2
        }),
    }
});

function fetchMessages() {
    fetch('/ajax-messages/')
        .then(response => response.json())
        .then(data => {
            console.log(data)
            const messages = data.messages;
            const messageContainer = document.getElementById('backendmessages');
            messageContainer.style.display = 'block';
            messageContainer.classList.remove('opacity-0');
            // Clear existing messages
            messageContainer.innerHTML = '';
            // Display new messages
            messages.forEach(msg => {
                const div = document.createElement('div');
                div.className =
                    `bg-green-100 border border-green-400 text-green-700 p-2 mb-2 rounded relative`;
                div.textContent = msg.message;
                messageContainer.appendChild(div);
            });
            setTimeout(() => {
                messageContainer.classList.add('opacity-0'); // Apply fade-out effect
                setTimeout(() => {
                    messageContainer.style.display = 'none'; // Completely hide the element
                }, 2000); // Wait for transition duration to complete
            }, 3000);
        })
        .catch(error => console.error('Error fetching messages:', error));
}
