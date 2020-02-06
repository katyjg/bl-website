$(document).ready(function() {
    $('.navbar ul.navbar-nav > .dropdown > a[href]').click(function() {
        var dropdown = $(this).next('.dropdown-menu');
        /*
         * The dropdown can be non-existent
         * The dropdown can be already open by css
         * (for instance display: block from a custom :hover setting)
         * or a "show" class on the element which also sets a display: block;
         */
        if (dropdown.length == 0 || $(dropdown).css('display') !== 'none') {
            if (this.href) {
                location.href = this.href;
            }
        }
    });
});