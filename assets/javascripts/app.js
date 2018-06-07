const sourcesListeners = require('./event_listeners/sources');
const authListeners = require('./event_listeners/auth');
const newsListeners = require('./event_listeners/news');

(function IIFE() {
    const news = document.querySelector('.news');
    const sourceFilter = document.querySelector('.source-filter select');
    const categoryFilter = document.querySelector('.category-filter select');

    newsListeners.addSourceFilterListener(news, sourceFilter, categoryFilter);
    newsListeners.addCategoryFilterListener(news, sourceFilter, categoryFilter);

    sourcesListeners.addSourceFormListener();
    sourcesListeners.addSourceCancelListener();

    authListeners.addSignFormListener();
    authListeners.addSignOutListener();

    newsListeners.attachFavouritesListeners();
})();