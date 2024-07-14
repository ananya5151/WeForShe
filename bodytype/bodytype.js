document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('bodyTypeForm');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        const bust = formData.get('bust');
        const waist = formData.get('waist');
        const hips = formData.get('hips');

        fetch('/predict', {
            method: 'POST',
            body: new URLSearchParams(formData)
        })
        .then(response => response.json())
        .then(data => {
            const predictedBodyType = data.predicted_body_type;
            resultDiv.textContent = `Predicted Body Type: ${predictedBodyType}`;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
