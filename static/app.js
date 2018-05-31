(function IIFE() {
    const sourceForm = document.querySelector('.source-form');
  
    if (sourceForm) {
        sourceForm.addEventListener('submit', (ev) => {
            ev.preventDefault();

            const form = ev.target;
            const errorContainer = document.querySelector('.error-container');
            const sourceURL = form.querySelector('[name="url"]').value; 

            errorContainer.innerText = '';
            
            fetch(`/source/new?url=${sourceURL}`, {
                method: 'POST',
                credentials: 'same-origin'
            }).then((response) => {
                response
                    .json()
                    .then((body) => {
                        if (body.ok) {
                            return location.reload();
                        }

                        errorContainer.innerText = body.error;
                    });
            }).catch((error) => {
                errorContainer.innerText = error;
            });
        });
    }
})();