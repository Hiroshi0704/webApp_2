var shiftApp = {};
shiftApp.object = {};

shiftApp.util = {};
shiftApp.util.object = {};

shiftApp.view = {};
shiftApp.view.object = {};

shiftApp.table = {};
shiftApp.table.object = {};

shiftApp.dialog = {};
shiftApp.dialog.object = {};

var inherits = function(childCtor, parentCtor) {
    function tempCtor() { };
    tempCtor.prototype = parentCtor.prototype;
    childCtor.super = parentCtor.prototype;
    childCtor.prototype = new tempCtor();
    childCtor.prototype.constructor = childCtor;
};

$(function() {
    $('#sidebar-toggler').click(function() {
        if ($(this).prop('checked')) {
            $('.sidebar').css('left', '0px');
            $('#main').css('margin-left', '160px');
        } else {
            $('.sidebar').css('left', '-160px');
            $('#main').css('margin-left', '0px');
        }
    });
});
