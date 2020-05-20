/**
 * 勤務表作成機能小画面用共通クラス
 */
shiftApp.dialog.AbstractDialog = function() { };

shiftApp.dialog.AbstractDialog.prototype.displayToFront = function(dialogId) {

    let views = [];
    let thisIndex;

    $('.view').each(function(i) {
        const view = $(this);
        views[i] = {
            view: view,
            zIndex: view.css('z-index') || 0
        }

        if (view.attr('id') === dialogId) {
            thisIndex = i;
        }
    });

    views[thisIndex].zIndex = views.length + 1;
    views.sort(function(a, b) {
        if (a.zIndex < b.zIndex) { return -1; }
        if (a.zIndex > b.zIndex) { return 1; }
        return 0;
    });

    views.forEach(function(item, i) {
        $(item.view).css('z-index', i + 1);
    });


};