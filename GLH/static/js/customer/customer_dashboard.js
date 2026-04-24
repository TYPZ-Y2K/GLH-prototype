// customer/customer_dashboard.js
document.addEventListener("DOMContentLoaded", () => {
  const cancelBtn = document.getElementById("myBtn");

  cancelBtn.addEventListener("click", (event) => {
    // Show confirmation dialog
    event.preventDefault();
    
    const userConfirmed = confirm("Are you sure you want to cancel this order?");

    if (userConfirmed) {
      // YES option
      alert("Order has been canceled.");
      // You can also call your cancel API or redirect here
    } else {
      // NO option
      alert("Order was NOT canceled.");
    }
  });
});

