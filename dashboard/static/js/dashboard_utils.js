const activeTogglers = document.querySelectorAll(".toggle-active")
activeTogglers?.forEach(toggler => {
    toggler.addEventListener("click", event => {
        const target_id = toggler.dataset.target
        console.log(target_id)
        const target = document.querySelector(target_id)
        target?.classList.toggle("active")
    })
})

// Form validation
window.addEventListener('load', function () {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function (form) {
        form.addEventListener('submit', function (event) {
            if (form.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
})

// Upload progress
const progressBars = document.querySelectorAll(".progress-container .progress")
window.addEventListener("load", () => {
    progressBars.forEach(bar => {
        const progress = bar.dataset.progress
        bar.style.width = `${progress}%`
    })
})

// Toggle alerts
const alertContainer = document.querySelector(".alert-container")
function hideAlert() {
    alertContainer?.classList.add("hide")
}

// Deletion
const confirmationForms = document.querySelectorAll(".requires-confirmation")
confirmationForms?.forEach(form => {
    const message = form.dataset.message
    form.addEventListener("submit", event => {
        response = confirm(message)
        if (!response) {
            event.preventDefault()
        }
    })
})
