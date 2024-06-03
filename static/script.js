document.addEventListener("DOMContentLoaded", function() {
    // Add event listener to the Upload button
    document.getElementById("upload").addEventListener("click", function() {
        // Show the progress bar
        var progressBar = document.createElement("div");
        progressBar.classList.add("progress-bar");
        progressBar.style.transition = "width 10s linear";
        document.body.appendChild(progressBar);

        // Start the progress animation
        setTimeout(function() {
            progressBar.style.width = "100%";
        }, 100);

        // Get the file inputs
        var fingerprintFile = document.getElementById("fingerprintInput").files[0];
        var irisFile = document.getElementById("irisInput").files[0];

        // Create image elements for fingerprint and iris
        var fingerprintImg = document.createElement("img");
        var irisImg = document.createElement("img");

        // Set the src attribute of the image elements to the selected files
        fingerprintImg.src = URL.createObjectURL(fingerprintFile);
        irisImg.src = URL.createObjectURL(irisFile);

        // Set the width and height of the images
        fingerprintImg.style.width = "100px"; // Adjust the width as needed
        fingerprintImg.style.height = "auto"; // Maintain aspect ratio
        irisImg.style.width = "100px"; // Adjust the width as needed
        irisImg.style.height = "auto"; // Maintain aspect ratio

        // Append the image elements to the imageDisplay div
        var imageDisplay = document.getElementById("imageDisplay");
        imageDisplay.innerHTML = ""; // Clear previous content

        // Add heading for uploaded images
        var uploadedImagesHeading = document.createElement("h4");
        uploadedImagesHeading.textContent = "UPLOADED IMAGES";
        uploadedImagesHeading.style.fontSize = "20px"; // Adjust the font size
        uploadedImagesHeading.style.fontFamily = "Georgia, sans-serif"; // Specify font family
        uploadedImagesHeading.style.color = "#26e9f7"; // Specify color
        imageDisplay.appendChild(uploadedImagesHeading);

        // Append the images to the imageDisplay div
        imageDisplay.appendChild(fingerprintImg);
        imageDisplay.appendChild(document.createElement("br")); // Add line break
        imageDisplay.appendChild(irisImg);

        // Send the files to the server using XMLHttpRequest or fetch
        var xhr = new XMLHttpRequest();
        var formData = new FormData();

        // Append the files to the FormData object
        formData.append("fingerprint", fingerprintFile);
        formData.append("iris", irisFile);

        // Send the files to the server using XMLHttpRequest or fetch
        xhr.open("POST", "/upload");
        xhr.send(formData);

        // You can handle the response here if needed
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                // Handle the response
                console.log(xhr.responseText);
            }
        };

        // Hide the progress bar after 10 seconds
        setTimeout(function() {
            progressBar.style.width = "0";
            setTimeout(function() {
                progressBar.remove();
            }, 500); // Delay removal to ensure smooth transition
        }, 10000);
    });

    // Add event listener to the Authenticate button
    document.getElementById("authenticate").addEventListener("click", function() {
        // Your authentication logic goes here
    });
});
