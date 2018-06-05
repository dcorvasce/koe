(function IIFE() {
    const parseResponseJSON = (request) => {
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
    const sourceFilter = document.querySelector('.source-filter select');
    const categoryFilter = document.querySelector('.category-filter select');

    if (news && sourceFilter) {
        sourceFilter.addEventListener('change', (ev) => {
            ev.preventDefault();

            const form = ev.target;
            const sourceId = form.querySelector('select[name="source_id"] option:checked').value;
            const category = document.querySelector('select[name="category"] option:checked').value;
            const template = document.querySelector('#article-template').innerHTML;
            const newsContainer = document.querySelector('.news');

            let params = `source_id=${sourceId}`;
            
            if (parseInt(sourceId) === 0) {
                location.href = '/';
                return;
            }

            if (category !== 'all') {
                params += `&category=${category}`;
            }

            fetch(`/news?${params}`, {
                method: 'GET',
                credentials: 'same-origin',
            }).then((response) => {
                response
                    .json()
                    .then((news) => {
                        console.log(news)
                        newsContainer.innerHTML = '';

                        news.forEach((piece) => {
                            const keys = Object.keys(piece);
                            let article = template;

                            keys.forEach((key) => {
                                article = article.replace(new RegExp(`:${key}`, 'g'), piece[key]);
                            });

                            newsContainer.innerHTML += article;
                        });
                    });
            }).catch((error) => {
                console.log(error);
            })
        });
    }

    if (news && categoryFilter) {
        categoryFilter.addEventListener('change', (ev) => {
            ev.preventDefault();

            const form = ev.target;
            const sourceId = document.querySelector('select[name="source_id"] option:checked').value;
            const category = form.querySelector('select[name="category"] option:checked').value;
            const template = document.querySelector('#article-template').innerHTML;
            const newsContainer = document.querySelector('.news');

            let params = `category=${category}`;

            if (category === 'all') {
                location.href = '/';
                return;
            }

            if (parseInt(sourceId) !== 0) {
                params += `&source_id=${sourceId}`;
            }

            fetch(`/news?${params}`, {
                method: 'GET',
                credentials: 'same-origin',
            }).then((response) => {
                response
                    .json()
                    .then((news) => {
                        console.log(news)
                        newsContainer.innerHTML = '';

                        news.forEach((piece) => {
                            const keys = Object.keys(piece);
                            let article = template;

                            keys.forEach((key) => {
                                article = article.replace(new RegExp(`:${key}`, 'g'), piece[key]);
                            });

                            newsContainer.innerHTML += article;
                        });
                    });
            }).catch((error) => {
                console.log(error);
            })
        });
    }
})();