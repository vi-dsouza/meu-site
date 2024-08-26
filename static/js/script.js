document.addEventListener('DOMContentLoaded', function() {
    var toggle = document.querySelector('.navbar-toggle');
    var menu = document.querySelector('.navbar-menu');

    toggle.addEventListener('click', function() {
        menu.classList.toggle('active');
    });
});

