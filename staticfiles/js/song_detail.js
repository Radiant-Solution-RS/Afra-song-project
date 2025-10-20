document.addEventListener('DOMContentLoaded', function() {
    const menuItems = document.querySelectorAll('.menu-item');
    const contentArea = document.getElementById('contentArea');

    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            menuItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');

            const tab = this.getAttribute('data-tab');
            if (tab === 'description') {
                contentArea.innerHTML = `{% if song.description %}{{ song.description|escapejs }}{% else %}No description available.{% endif %}`;
            } else if (tab === 'changelog') {
                contentArea.innerHTML = `{% if song.changelog %}{{ song.changelog|escapejs }}{% else %}No changelog available.{% endif %}`;
            }
        });
    });
});
