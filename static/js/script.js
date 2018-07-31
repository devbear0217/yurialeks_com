(function($) {

    'use strict';

    function initMetisMenu() {
        $("#side-menu").metisMenu();
    }

    function initLeftMenuCollapse() {
        $('.button-menu-mobile').click(function (event) {
            event.preventDefault();
            $("body").toggleClass("enlarged");
        });
    }

    function init() {
        initMetisMenu();
        initLeftMenuCollapse();
    }
    init();

})(jQuery)