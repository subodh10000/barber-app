// static/script.js

document.addEventListener('DOMContentLoaded', () => {
    const servicesList = document.getElementById('services-list');
    const serviceSelect = document.getElementById('service-select');
    const bookingForm = document.getElementById('booking-form');
    const successMessage = document.getElementById('success-message');

    // 1. Fetch services and populate the page
    fetch('/api/services')
        .then(response => response.json())
        .then(services => {
            services.forEach(service => {
                // Add to the list display
                const li = document.createElement('li');
                li.textContent = `${service.name} - $${service.price}`;
                servicesList.appendChild(li);

                // Add to the form dropdown
                const option = document.createElement('option');
                option.value = service.name;
                option.textContent = `${service.name} ($${service.price})`;
                serviceSelect.appendChild(option);
            });
        });

    // 2. Handle the booking form submission
    bookingForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent the default form submission (page reload)

        // Collect form data
        const formData = new FormData(bookingForm);
        const bookingDetails = {
            name: formData.get('name'),
            service: formData.get('service'),
            date: formData.get('date'),
            time: formData.get('time')
        };
        
        // Send data to the backend
        fetch('/api/book', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bookingDetails)
        })
        .then(response => response.json())
        .then(data => {
            // Show success message and reset the form
            successMessage.textContent = data.message;
            successMessage.classList.remove('hidden');
            bookingForm.reset();

            // Hide the message after a few seconds
            setTimeout(() => {
                successMessage.classList.add('hidden');
            }, 5000);
        })
        .catch(error => {
            console.error('Error:', error);
            successMessage.textContent = 'Something went wrong. Please try again.';
            successMessage.classList.remove('hidden');
        });
    });
});