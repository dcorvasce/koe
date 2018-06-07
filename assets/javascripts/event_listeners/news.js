const loadNews = (news, container, template) => {
    container.innerHTML = '';

    news.forEach((piece) => {
        piece['active'] = piece['starred'] == 1 ? 'active' : '';
        piece['fav-label'] = piece['starred'] == 0 ? 'Add to favourites' : 'Starred';

        const keys = Object.keys(piece);
        let article = template;

        keys.forEach((key) => {
            article = article.replace(new RegExp(`:${key}`, 'g'), piece[key]);
        });

        container.innerHTML += article;
    });
};

const attachFavouritesListeners = () => {
    const favourites = document.querySelectorAll('[data-action="add-favourite"]');

    favourites.forEach((favourite) => {
        favourite.addEventListener('click', (ev) => {
            ev.preventDefault();

            const target = ev.target;
            const targetLabel = target.querySelector('span');
            const articleId = target.getAttribute('data-article-id');

            target.classList.toggle('active');

            if (targetLabel.innerText === 'Add to favourites') {
                targetLabel.innerText = 'Starred';
            } else {
                targetLabel.innerText = 'Add to favourites';
            }

            fetch(`/favourites/${articleId}`, {
                method: 'POST',
                credentials: 'same-origin'
            });
        });
    });
};

module.exports = {
    attachFavouritesListeners,
    addSourceFilterListener: (news, sourceFilter, categoryFilter) => {
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
                            loadNews(news, newsContainer, template);
                            attachFavouritesListeners();
                        });
                }).catch((error) => {
                    console.log(error);
                })
            });
        }
    },
    addCategoryFilterListener: (news, sourceFilter, categoryFilter) => {
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
                            loadNews(news, newsContainer, template);
                            attachFavouritesListeners();
                        });
                }).catch((error) => {
                    console.log(error);
                })
            });
        }
    },
};