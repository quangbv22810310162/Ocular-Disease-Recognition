document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('imageUpload');
    const fileNameDisplay = document.getElementById('file-name');
    const imagePreview = document.getElementById('imagePreview');
    const uploadForm = document.getElementById('upload-form');

    fileInput.addEventListener('change', function(e) {
        const fileName = e.target.files[0].name;
        fileNameDisplay.textContent = fileName;

        const reader = new FileReader();
        reader.onload = function(event) {
            imagePreview.src = event.target.result;
            imagePreview.style.display = 'block';
        }
        reader.readAsDataURL(e.target.files[0]);
    });

    uploadForm.addEventListener('submit', function(e) {
        if (!fileInput.files.length) {
            e.preventDefault();
            alert('Please select a file before submitting.');
        }
    });
});

function closeError() {
    const errorModal = document.querySelector('.error-modal');
    if (errorModal) {
        errorModal.style.display = 'none';
    }
}
