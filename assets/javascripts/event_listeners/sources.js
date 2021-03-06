import { parseJSON } from '../utilities/response';

module.exports = {
    addSourceFormListener: () => {
        const sourceForm = document.querySelector('.source-form');
        const errorContainer = document.querySelector('.error-container');

        if (sourceForm) {
            sourceForm.addEventListener('submit', (ev) => {
                ev.preventDefault();

                const loadingIcon = '<i class="fas fa-spinner"></i>'
                errorContainer.innerHTML = `${loadingIcon} Fetching information about the source..`;
                errorContainer.classList.remove('fade-out');
                errorContainer.classList.add('info');

                const form = ev.target;
                const sourceURL = form.querySelector('[name="url"]').value;

                parseJSON(fetch(`/source/new?url=${sourceURL}`, {
                    method: 'POST',
                    credentials: 'same-origin',
                }));
            });
        }
    },
    addSourceCancelListener: () => {
        const sources = document.querySelectorAll('a[data-action="delete-source"]');

        sources.forEach((source) => {
            source.addEventListener('click', (ev) => {
                ev.preventDefault();
                const sourceId = ev.target.getAttribute('data-source-id');

                fetch(`/subscriptions/${sourceId}`, {
                    method: 'DELETE',
                    credentials: 'same-origin',
                }).then((response) => {
                    location.reload();
                });
            });
        });
    },
};