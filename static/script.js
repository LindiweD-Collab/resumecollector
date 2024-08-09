const form = document.getElementById('resumeForm');
const successMessage = document.getElementById('successMessage');

form.addEventListener('submit', function(event) {
    event.preventDefault();
    if (form.checkValidity()) {
        // Simulate form submission (replace with actual submission logic)
        setTimeout(() => {
            form.reset();
            successMessage.style.display = 'block';
            setTimeout(() => {
                successMessage.style.display = 'none';
            }, 3000); // Hide success message after 3 seconds
        }, 1000); // Simulate 1 second delay for submission
    } else {
        form.reportValidity();
    }
});
