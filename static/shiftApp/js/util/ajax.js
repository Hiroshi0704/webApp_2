shiftApp.util.ajax = {};

shiftApp.util.ajax.AjaxCommand = function(url, type, async, callback, error) {

    this.url_ = url;

    this.type_ = type;

    this.async_ = async;

    this.callback_ = callback;

    this.error_ = error;

};

shiftApp.util.ajax.AjaxCommand.prototype.excecute = function() {

    $.ajax({
        url: this.url_,
        type: this.type_,
        async: this.async_,
        success: this.callback_,
        error: this.error_
    });
};

/**
 * Ajax非同期処理クラス
 */
shiftApp.util.ajax.AjaxAsyncCommand = function(url, callback) {

    this.url_ = url;

    this.callback_ = callback;

};

shiftApp.util.ajax.AjaxAsyncCommand.prototype.executePost = function() {
    let ajaxCommand = new shiftApp.util.ajax.AjaxCommand(
        this.url_,
        'POST',
    );
};

shiftApp.util.ajax.AjaxAsyncCommand.prototype.executeGet = function() {

};

/**
 * Ajax同期処理クラス
 */
shiftApp.util.ajax.AjaxSyncCommand = function() {

};

shiftApp.util.ajax.get = function(url, callback, scope) {
    $.ajax({
        url: url,
        type: 'GET',
    })
        .done(callback.bind(scope))
        .fail(function(jqXHR, textStatus, errorThrown) {
            console.log('jqXHR: ' + jqXHR);
            console.log('textStatus: ' + textStatus);
            console.log('errorThrown: ' + errorThrown);
        });
};


shiftApp.util.ajax.post = function(url, callback, scope) {
    $.ajax({
        url: url,
        type: 'POST',
    })
        .done(callback.bind(scope))
        .fail(function(jqXHR, textStatus, errorThrown) {
            console.log('jqXHR: ' + jqXHR);
            console.log('textStatus: ' + textStatus);
            console.log('errorThrown: ' + errorThrown);
        });
};