module.exports = {
    addPreviousPageListener: () => {
        const previousButton = document.querySelector('[data-action="previous-button"]');

        if (previousButton) {
            previousButton.addEventListener('click', (ev) => {
                ev.preventDefault();

            });
        }
    },
    addNextPageListener: () => {
        const nextButton = document.querySelector('[data-action="next-button"]');

        if (nextButton) {
            nextButton.addEventListener('click', (ev) => {
                ev.preventDefault();
            });
        }
    },
};