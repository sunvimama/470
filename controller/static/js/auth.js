document.addEventListener('DOMContentLoaded', function() {
    // Form validation for login and register forms
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const password = this.querySelector('input[type="password"]');
            const email = this.querySelector('input[type="email"]');
            let isValid = true;
            
            // Clear previous error styles
            this.querySelectorAll('.is-invalid').forEach(el => {
                el.classList.remove('is-invalid');
            });
            
            // Email validation
            if (email && !validateEmail(email.value)) {
                email.classList.add('is-invalid');
                showError(email, 'Please enter a valid email address');
                isValid = false;
            }
            
            // Password validation (only for register form)
            if (password && this.id === 'registerForm' && password.value.length < 6) {
                password.classList.add('is-invalid');
                showError(password, 'Password must be at least 6 characters');
                isValid = false;
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    });
    
    // Helper function to validate email
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
    
    // Helper function to show error messages
    function showError(input, message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        input.parentNode.appendChild(errorDiv);
        
        // Remove error after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }
    
    // Toggle password visibility (for both login and register pages)
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const passwordInput = this.previousElementSibling;
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            this.querySelector('i').classList.toggle('fa-eye');
            this.querySelector('i').classList.toggle('fa-eye-slash');
        });
    });
});