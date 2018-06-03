(function IIFE() {
    const parseResponseJSON = (request) => {
        request.then((response) => {
            const errorContainer = document.querySelector('.error-container');
            errorContainer.innerText = '';

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
    };

    const sourceForm = document.querySelector('.source-form');
  
    if (sourceForm) {
        sourceForm.addEventListener('submit', (ev) => {
            ev.preventDefault();

            const form = ev.target;
            const sourceURL = form.querySelector('[name="url"]').value; 

            parseResponseJSON(fetch(`/source/new?url=${sourceURL}`, {
                method: 'POST',
                credentials: 'same-origin',
            }));
        });
    }

    const signForm = document.querySelector('.sign-form');
  
    if (signForm) {
        signForm.addEventListener('submit', (ev) => {
            ev.preventDefault();

            const form = ev.target;
            const url = form.getAttribute('action');
            let body = new FormData();

            form.querySelectorAll('input').forEach((input) => {
                body.append(input.name, input.value);
            });

            parseResponseJSON(fetch(url, {
                method: 'POST',
                credentials: 'same-origin',
                body: body,
            }));
        });
    }

    const news = document.querySelector('.news');
    const sourceFilter = document.querySelector('.source-filter');

    if (news && sourceFilter) {
        sourceFilter.addEventListener('submit', (ev) => {
            ev.preventDefault();

            const form = ev.target;
            const sourceId = form.querySelector('select option:checked').value;

            if (parseInt(sourceId) === 0) {
                location.href = '/';
                return;
            }

            location.href = `/?filter_by=${sourceId}`;
        });
    }
})();