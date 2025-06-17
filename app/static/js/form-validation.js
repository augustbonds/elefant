// Form validation functionality
class FormValidator {
    constructor() {
        this.bindEvents();
    }
    
    bindEvents() {
        // Add form validation on submit
        const form = document.querySelector('form');
        if (form) {
            form.addEventListener('submit', (e) => {
                if (!this.validateForm()) {
                    e.preventDefault();
                }
            });
        }
        
        // Add real-time validation
        ['title', 'url', 'description'].forEach(fieldName => {
            const field = document.getElementById(fieldName);
            if (field) {
                field.addEventListener('blur', () => this.validateForm());
            }
        });
    }
    
    validateForm() {
        const title = document.getElementById('title').value.trim();
        const url = document.getElementById('url').value.trim();
        const description = document.getElementById('description').value.trim();
        
        // Clear previous errors
        document.querySelectorAll('.client-error').forEach(error => error.remove());
        
        let isValid = true;
        
        // Validate title
        if (!title) {
            this.showClientError('title', 'Title is required');
            isValid = false;
        } else if (title.length > 200) {
            this.showClientError('title', 'Title must be less than 200 characters');
            isValid = false;
        }
        
        // Validate URL
        if (!url) {
            this.showClientError('url', 'URL is required');
            isValid = false;
        } else {
            try {
                new URL(url);
            } catch {
                this.showClientError('url', 'Please enter a valid URL');
                isValid = false;
            }
        }
        
        // Validate description
        if (!description) {
            this.showClientError('description', 'Description is required');
            isValid = false;
        } else if (description.length > 1000) {
            this.showClientError('description', 'Description must be less than 1000 characters');
            isValid = false;
        }
        
        return isValid;
    }
    
    showClientError(fieldName, message) {
        const field = document.getElementById(fieldName);
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-errors';
        errorDiv.innerHTML = `<span class="error client-error">${message}</span>`;
        field.parentNode.appendChild(errorDiv);
    }
}