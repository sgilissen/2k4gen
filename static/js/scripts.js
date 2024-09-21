document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('fetch-uuid');
    const uuidField = document.getElementById('uuid-field');
    const copyButton = document.getElementById('copy-uuid');

    // Event listener for the button click
    button.addEventListener('click', function() {
        fetch('/get-uuid')
            .then(response => response.json())
            .then(data => {
                // Set the UUID value in the text field
                uuidField.value = data.uuid;
            })
            .catch(error => console.error('Error fetching UUID:', error));
    });

    // Function to copy UUID to clipboard
    copyButton.addEventListener('click', function () {
        if (uuidField.value !== "") {
            // Copy the UUID from the input field to clipboard
            uuidField.select();
            document.execCommand("copy");

            // Show confirmation message
            copyButton.innerText = "Copied! :)";
            copyButton.classList.add("copy-btn-green")

            // Optionally hide the confirmation message after 2 seconds
            setTimeout(() => {
                copyButton.innerText = "Copy to Clipboard";
                copyButton.classList.remove("copy-btn-green")
            }, 2000);
        }
    });

});

