document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const loadingSpinner = document.createElement('div');
    loadingSpinner.className = 'spinner';
    loadingSpinner.innerHTML = 'Comparing...';

    form.addEventListener('submit', function (event) {
        const file1 = form.file1.files[0];
        const file2 = form.file2.files[0];

        // File validation
        if (!file1 || !file2) {
            alert('Please upload both documents.');
            event.preventDefault();
            return;
        }

        // Show loading spinner
        form.appendChild(loadingSpinner);
    });
});
