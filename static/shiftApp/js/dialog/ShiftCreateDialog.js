/**
 * 勤務表作成機能　勤務表作成ダイアログ用クラス
 */
shiftApp.dialog.ShiftCreateDialog = function() {
    this.super = shiftApp.dialog.AbstractDialog.prototype;
    this.dialogId = 'shiftCreateView';
    this.$form = $('#shiftCreateForm');
};
shiftApp.dialog.ShiftCreateDialog.prototype = new shiftApp.dialog.AbstractDialog();

/**
 * 勤務表作成ダイアログ初期化処理
 */
shiftApp.dialog.ShiftCreateDialog.prototype.initDialog = function() {

    $('#shiftCreateSaveBtn').off().click(this.onClickSaveBtn.bind(this));
    $('#shiftCreateCancelBtn').off().click(this.onClickCancelBtn.bind(this));
    $('#shiftCreateViewCloseBtn').off().click(this.onClickCloseBtn.bind(this));

    this.initForm();
};

/**
 * 勤務表入力フォーム初期化
 */
shiftApp.dialog.ShiftCreateDialog.prototype.initForm = function() {

    const self = this;

    this.$form.find('.form-group > input, select').val(null);
    this.$form.find('input[type=checkbox]').prop('checked', false);

    // 選択可能な従業員を取得
    this.getWorkers().done(function(workers) {
        // 従業員を初期化
        $('#' + self.dialogId + ' select[name=worker] > ').remove();
        workers.map(worker => {
            let $option = $('<option></option>');
            $option.val(worker.id);
            $option.text(worker.worker_detail.username);
            $('#' + self.dialogId + ' select[name=worker]').append($option);
        });
    });

};

shiftApp.dialog.ShiftCreateDialog.prototype.showDialog = function(top, left) {

    this.initDialog();

    const $dialog = $('#' + this.dialogId);

    $dialog.draggable();
    $dialog.show();

    const centerX = ($(window).width() - $dialog.width()) / 2;
    const centerY = ($(window).height() - $dialog.height()) / 2 + 56;

    $dialog.offset({
        left: left || centerX,
        top: top || centerY,
    });

    this.super.displayToFront(this.dialogId);
};

shiftApp.dialog.ShiftCreateDialog.prototype.hideDialog = function() {
    $('#' + this.dialogId).hide();
};

shiftApp.dialog.ShiftCreateDialog.prototype.onClickCancelBtn = function() {
    this.hideDialog();
};

shiftApp.dialog.ShiftCreateDialog.prototype.onClickCloseBtn = function() {
    this.hideDialog();
};

shiftApp.dialog.ShiftCreateDialog.prototype.onClickSaveBtn = function() {

    const self = this;

    this.$form.find('.helpBlock').text('');
    this.$form.find('.fieldError').removeClass('fieldError');

    let param = new FormData(this.$form[0]);

    $.ajax({
        type: 'POST',
        url: '/shiftApp/shift/',
        dataType: 'json',
        contentType: false,
        processData: false,
        data: param,
    })
        .done(this.onPostShiftFormDone.bind(this))
        .fail(this.onPostShiftFormFail.bind(this));

};

shiftApp.dialog.ShiftCreateDialog.prototype.getWorkers = function() {

    const response = $.ajax({
        type: 'GET',
        url: '/shiftApp/ajax/worker/'
    });

    return response;
};

shiftApp.dialog.ShiftCreateDialog.prototype.onPostShiftFormDone = function(response) {
    console.log(response);
    this.$form.find('.form-group > input, select').val(null);
    this.$form.find('input[type=checkbox]').prop('checked', false);
    shiftApp.table.object.shiftListTable && shiftApp.table.object.shiftListTable.reload();
    this.hideDialog();
};

shiftApp.dialog.ShiftCreateDialog.prototype.onPostShiftFormFail = function(response) {
    console.log(response);
    if (response.status === 400) {
        const data = response.responseJSON;
        for (let key in data) {
            let $field = this.$form.find('[name=' + key + ']');
            $field.addClass('fieldError');

            let $helpBlock = $field.next('.helpBlock');
            let message = data[key];
            $helpBlock.text(message);
        }
    } else {
        // TODO
    }
};

