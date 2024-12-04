document.addEventListener('DOMContentLoaded', function () {
    // Handle Friend Button click
    const friendBtn = document.getElementById('friend-btn');
    
    if (friendBtn) {
        friendBtn.addEventListener('click', (event) => {
            event.preventDefault(); // Prevents page reload

            console.log("Friend Button clicked");
            const otherId = friendBtn.getAttribute('data-other-id'); // Get other user's account name from template

            const data = {
                otherId: otherId,
            };

            // Send POST request to Flask server
            fetch('/friend_request', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                console.log("Success:", data);
            })
            .catch((error) => {
                console.error("Error:", error);
            });
        });
    }

    // Handle Accept Button click
    const acceptBtn = document.getElementById('accept_btn');
    
    if (acceptBtn) {
        acceptBtn.addEventListener('click', (event) => {
            event.preventDefault(); // Prevents page reload

            console.log("Accept Button clicked");
            const otherId = acceptBtn.getAttribute('data-other-id'); // Get other user's account name from template

            const data = {
                otherId: otherId,
            };

            // Send POST request to Flask server
            fetch('/accept_friend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                console.log("Success:", data);
            })
            .catch((error) => {
                console.error("Error:", error);
            });
        });
    }

    // Handle Deny Button click
    const denyBtn = document.getElementById('deny_btn');
    
    if (denyBtn) {
        denyBtn.addEventListener('click', (event) => {
            event.preventDefault(); // Prevents page reload

            console.log("Deny Button clicked");
            const otherId = denyBtn.getAttribute('data-other-id'); // Get other user's account name from template

            const data = {
                otherId: otherId,
            };

            // Send POST request to Flask server
            fetch('/deny_friend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                console.log("Success:", data);
            })
            .catch((error) => {
                console.error("Error:", error);
            });
        });
    }
});
