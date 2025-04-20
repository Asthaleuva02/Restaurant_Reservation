xdocument.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const bookingForm = document.getElementById('booking-form');
    const dateInput = document.getElementById('booking-date');
    const timeInput = document.getElementById('booking-time');
    const guestsInput = document.getElementById('booking-guests');
    
    const checkButton = document.getElementById('check-availability');
    const tableSelect = document.getElementById('table-selection');
    const availabilityMessage = document.getElementById('availability-message');
    const bookingSection = document.getElementById('booking-section');
    const availabilitySection = document.getElementById('availability-section');
    
    // Set min date to today
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    const formattedToday = `${yyyy}-${mm}-${dd}`;
    dateInput.setAttribute('min', formattedToday);
    
    // Handle availability check
    if (checkButton) {
        checkButton.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Form validation
            if (!validateBookingForm()) {
                return;
            }
            
            // Clear previous results
            tableSelect.innerHTML = '';
            availabilityMessage.textContent = '';
            
            // Show loading state
            checkButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Checking...';
            checkButton.disabled = true;
            
            // Get form values
            const date = dateInput.value;
            const time = timeInput.value;
            const guests = parseInt(guestsInput.value);
            
            // Check availability via API
            fetch('/api/check-availability', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ date, time, guests })
            })
            .then(response => response.json())
            .then(data => {
                checkButton.innerHTML = 'Check Availability';
                checkButton.disabled = false;
                
                if (data.available) {
                    availabilityMessage.textContent = 'Tables are available for your party!';
                    availabilityMessage.className = 'text-success mt-3';
                    
                    // Create table options
                    data.tables.forEach(table => {
                        const option = document.createElement('option');
                        option.value = table.id;
                        option.textContent = `${table.name} (Seats ${table.capacity})`;
                        tableSelect.appendChild(option);
                    });
                    
                    // Show booking section
                    availabilitySection.classList.remove('d-none');
                } else {
                    availabilityMessage.textContent = 'Sorry, no tables are available for your selected time and party size.';
                    availabilityMessage.className = 'text-danger mt-3';
                    availabilitySection.classList.add('d-none');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                checkButton.innerHTML = 'Check Availability';
                checkButton.disabled = false;
                availabilityMessage.textContent = 'An error occurred. Please try again.';
                availabilityMessage.className = 'text-danger mt-3';
            });
        });
    }
    
    // Handle booking submission
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Validate all fields
            if (!validateBookingForm() || !validateContactForm()) {
                return;
            }
            
            // Get form values
            const name = document.getElementById('customer-name').value;
            const email = document.getElementById('customer-email').value;
            const phone = document.getElementById('customer-phone').value;
            const date = dateInput.value;
            const time = timeInput.value;
            const guests = parseInt(guestsInput.value);
            const table_id = parseInt(tableSelect.value);
            const special_requests = document.getElementById('special-requests').value;
            
            // Show loading state
            const submitBtn = document.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
            submitBtn.disabled = true;
            
            // Submit booking via API
            fetch('/api/book', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name, email, phone, date, time, guests, table_id, special_requests
                })
            })
            .then(response => response.json())
            .then(data => {
                submitBtn.innerHTML = originalBtnText;
                submitBtn.disabled = false;
                
                if (data.success) {
                    // Redirect to confirmation page
                    window.location.href = `/confirmation/${data.reservation_id}`;
                } else {
                    alert(data.message || 'An error occurred while processing your booking.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                submitBtn.innerHTML = originalBtnText;
                submitBtn.disabled = false;
                alert('An error occurred. Please try again.');
            });
        });
    }
    
    // Form validation functions
    function validateBookingForm() {
        let isValid = true;
        
        // Validate date
        if (!dateInput.value) {
            showError(dateInput, 'Please select a date');
            isValid = false;
        } else {
            clearError(dateInput);
        }
        
        // Validate time
        if (!timeInput.value) {
            showError(timeInput, 'Please select a time');
            isValid = false;
        } else {
            clearError(timeInput);
        }
        
        // Validate guests
        if (!guestsInput.value || guestsInput.value < 1) {
            showError(guestsInput, 'Please enter number of guests');
            isValid = false;
        } else {
            clearError(guestsInput);
        }
        
        return isValid;
    }
    
    function validateContactForm() {
        let isValid = true;
        const nameInput = document.getElementById('customer-name');
        const emailInput = document.getElementById('customer-email');
        const phoneInput = document.getElementById('customer-phone');
        
        // Validate name
        if (!nameInput.value.trim()) {
            showError(nameInput, 'Please enter your name');
            isValid = false;
        } else {
            clearError(nameInput);
        }
        
        // Validate email
        if (!emailInput.value.trim() || !isValidEmail(emailInput.value)) {
            showError(emailInput, 'Please enter a valid email address');
            isValid = false;
        } else {
            clearError(emailInput);
        }
        
        // Validate phone
        if (!phoneInput.value.trim()) {
            showError(phoneInput, 'Please enter your phone number');
            isValid = false;
        } else {
            clearError(phoneInput);
        }
        
        return isValid;
    }
    
    function isValidEmail(email) {
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }
    
    function showError(input, message) {
        const formGroup = input.closest('.mb-3');
        const errorDiv = formGroup.querySelector('.invalid-feedback') || document.createElement('div');
        
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        
        if (!formGroup.querySelector('.invalid-feedback')) {
            formGroup.appendChild(errorDiv);
        }
        
        input.classList.add('is-invalid');
    }
    
    function clearError(input) {
        input.classList.remove('is-invalid');
    }
});
