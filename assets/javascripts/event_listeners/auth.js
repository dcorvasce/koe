import { parseJSON } from '../utilities/response';

module.exports = {
    addSignFormListener: () => {
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
    
                parseJSON(fetch(url, {
                    method: 'POST',
                    credentials: 'same-origin',
                    body: body,
                }));
            });
        }
    },
    addSignOutListener: () => {
        const signOut = document.querySelector('a[data-action="sign-out"]');

        if (signOut) {
            signOut.addEventListener('click', (ev) => {
                ev.preventDefault();
                const confirmation = confirm('Do you really want to sign out?');
    
                if (confirmation) {
                    fetch('/signout', {
                        method: 'POST',
                        credentials: 'same-origin',
                    }).then(() => {
                        location.reload();
                    });
                }
            });
        }
    },
};