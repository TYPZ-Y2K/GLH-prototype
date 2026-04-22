// Toggle delivery address field
document.querySelectorAll('input[name="order_type"]').forEach(function(radio) {
    radio.addEventListener('change', function() {
        var fields = document.getElementById('delivery-fields');
        fields.style.display = this.value === 'delivery' ? 'block' : 'none';
    });
});

// Basic client-side validation for simulated payment
document.getElementById('checkout-form').addEventListener('submit', function(e) {
    var card = document.getElementById('card_number').value.replace(/\s/g, '');
    var expiry = document.getElementById('expiry').value;
    var cvc = document.getElementById('cvc').value;
    var errors = [];

    if (card.length < 13 || card.length > 19 || !/^\d+$/.test(card)) {
        errors.push('Please enter a valid card number.');
    }
    if (!/^\d{2}\/\d{2}$/.test(expiry)) {
        errors.push('Please enter expiry as MM/YY.');
    }
    if (!/^\d{3,4}$/.test(cvc)) {
        errors.push('Please enter a valid CVC.');
    }

    if (errors.length) {
        e.preventDefault();
        alert(errors.join('\n'));
    }
});