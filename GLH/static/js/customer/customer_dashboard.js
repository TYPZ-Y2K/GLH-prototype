// customer/customer_dashboard.js
document.addEventListener("DOMContentLoaded", function () {
    // Event delegation — one listener on the document catches ALL cancel buttons
    document.addEventListener("click", function (event) {
        // Only act on buttons with the cancel class
        if (!event.target.classList.contains("btn-cancel")) return;

        event.preventDefault();

        var confirmed = confirm("Are you sure you want to cancel this order?");

        if (confirmed) {
            // Submit the parent form
            event.target.closest("form").submit();
        }
    });
});


