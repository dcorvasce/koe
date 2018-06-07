module.exports = {
    parseJSON: (request) => {
        request.then((response) => {
            const errorContainer = document.querySelector('.error-container');
            errorContainer.innerText = '';
            errorContainer.classList.remove('fade-out');

            response
                .json()
                .then((body) => {
                    if (body.ok) {
                        return location.reload();
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