// produce-control.js

// Function to prompt for password before deletion
function promptDelete(form) {
    const pw = prompt('Enter your password to confirm deletion:');
    if (!pw) return false; // Cancel if no password entered
    const pwField = form.querySelector('.delete-pw');
    if (pwField) {
        pwField.value = pw;
    } else {
        console.error("No hidden password field found in form:", form);
        return false;
    }
    return true;
}

// Attach event listeners after DOM is ready
document.addEventListener("DOMContentLoaded", function () {
    // Select all forms with the class 'delete-form'
    document.querySelectorAll("form.delete-form").forEach(function (form) {
        form.addEventListener("submit", function (e) {
            if (!promptDelete(form)) {
                e.preventDefault(); // Stop form submission if cancelled
            }
        });
    });
});

