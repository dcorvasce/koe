module.exports = {
    parseJSON: (request) => {
        request.then((response) => {
            const errorContainer = document.querySelector('.error-container');
            errorContainer.innerText = '';
            errorContainer.classList.remove('fade-out');
            errorContainer.classList.remove('info');

            response
                .json()
                .then((body) => {
                    if (body.ok) {
                        location.reload();
                        return;
                    }

                    errorContainer.innerText = body.error;
                    errorContainer.classList.add('fade-out');
                });
        }).catch((error) => {
            errorContainer.innerText = error;
            errorContainer.classList.add('fade-out');
        });
    },
};