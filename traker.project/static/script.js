// Function to validate form inputs
const logBtn = document.getElementById("loginBtn")
const switchAdmin = document.getElementById("switchToAdmin")
const username = document.getElementById("username")
const password = document.getElementById("password")



logBtn.addEventListener("click",async()=>{// Prevent the default form submission
    
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
    
        const data = { username: username, password: password };
    
        fetch('/login', {
            method: 'POST',   // or 'PUT'
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            if (data.success) {
                window.location.href = '/dashboard';  // Redirect to a new page if login is successful
            } else {
                alert('Login failed: ' + data.message);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
})

switchAdmin.addEventListener("click", ()=>{
    window.location.href = "/admin"
})
function validateForm(formId) {
    const form = document.getElementById(formId);
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], select[required]');

    inputs.forEach(input => {
        if (input.value.trim() === '') {
            isValid = false;
            input.classList.add('invalid');  // Add 'invalid' class that you can style with CSS
            alert(`Please fill out the ${input.name} field.`);
        } else {
            input.classList.remove('invalid');
        }
    });

    return isValid;
}

// Attach submit event listeners to forms with validation
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!validateForm(this.id)) {
                event.preventDefault();  
                event.stopPropagation(); 
            }
        });
    });
});

document.getElementById('switchToAdmin').addEventListener('click', function() {
    var adminPassword = prompt("Please enter the ADMIN password:", "");
    if (adminPassword != null && adminPassword != "") {
        if (adminPassword === "admin") {  
            window.location.href = '/admin';  // Redirect to admin panel 
        } else {
            alert("Incorrect password!");
        }
    }
});
