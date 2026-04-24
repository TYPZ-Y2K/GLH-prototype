//auth/register.js
document.addEventListener('DOMContentLoaded', () => {
const form = document.getElementById('register-form');
const passwordInput = document.getElementById('password');
const confirmPasswordInput = document.getElementById('confirm_password');
const errorContainer = document.getElementById('error-container');

form.addEventListener('submit', event => {
if (passwordInput.value !== confirmPasswordInput.value) {
    event.preventDefault();
    errorContainer.textContent = 'Passwords do not match.';
    errorContainer.style.display = 'block';
    confirmPasswordInput.focus();
} else {
    errorContainer.style.display = 'none';
}
});
});

document.addEventListener('DOMContentLoaded', () => {
const passwordInput = document.getElementById('password');
const messageBox = document.getElementById('passwordMessage');

passwordInput.addEventListener('input', () => {
const password = passwordInput.value;
const requirements = {
    length: password.length >= 10,
    uppercase: /[A-Z]/.test(password),
    lowercase: /[a-z]/.test(password),
    number: /\d/.test(password),
    special: /[^A-Za-z0-9]/.test(password),
};

const allValid = Object.values(requirements).every(Boolean);

if (password === '' || allValid) {
    messageBox.innerHTML = '';
} else {
    messageBox.innerHTML = `
    <ul style="list-style-type:none; padding:0; margin:0;">
        ${requirements.length ? '' : '<li style="color:red;">- At least 10 characters</li>'}
        ${requirements.uppercase ? '' : '<li style="color:red;">- At least one uppercase letter</li>'}
        ${requirements.lowercase ? '' : '<li style="color:red;">- At least one lowercase letter</li>'}
        ${requirements.number ? '' : '<li style="color:red;">- At least one number</li>'}
        ${requirements.special ? '' : '<li style="color:red;">- At least one special character</li>'}
    </ul>
    `;
}
});
});