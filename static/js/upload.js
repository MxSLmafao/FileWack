document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const uploadProgress = document.getElementById('upload-progress');
    const uploadStatus = document.getElementById('upload-status');

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        dropZone.classList.add('border-primary');
    }

    function unhighlight(e) {
        dropZone.classList.remove('border-primary');
    }

    dropZone.addEventListener('drop', handleDrop, false);
    fileInput.addEventListener('change', handleFiles, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles({ target: { files: files } });
    }

    function handleFiles(e) {
        const files = e.target.files;
        uploadFile(files[0]);
    }

    function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        uploadProgress.style.width = '0%';
        uploadProgress.parentElement.classList.remove('d-none');
        uploadStatus.textContent = 'Uploading...';

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            uploadProgress.style.width = '100%';
            uploadStatus.innerHTML = `Upload complete! Your file is available at: <a href="${data.url}" class="text-info">${window.location.origin}${data.url}</a>`;
        })
        .catch(error => {
            uploadStatus.textContent = `Error: ${error.message}`;
            uploadProgress.parentElement.classList.add('d-none');
        });
    }
});
