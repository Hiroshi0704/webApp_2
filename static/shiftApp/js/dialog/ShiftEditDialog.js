/**
 * 勤務表作成機能勤務表編集ダイアログ用クラス
 * @extends shiftApp.dialog.AbstractDialog
 */
shiftApp.dialog.ShiftEditDialog = function(shiftId) {
    this.super = shiftApp.dialog.AbstractDialog.prototype;
    this.dialogId = 'shiftEditView';
    this.shiftId = shiftId;
};
shiftApp.dialog.ShiftEditDialog.prototype = new shiftApp.dialog.AbstractDialog();

/**
 * 勤務表編集ダイアログ初期化処理
 */
shiftApp.dialog.ShiftEditDialog.prototype.initDialog = function() {
    this.getShift(this.initForm.bind(this));

    $('#shiftEditViewCloseBtn').click(this.onClickCloseBtn.bind(this));
};

/**
 * 勤務表入力フォーム初期化
 * @param shift 勤務表情報
 */
shiftApp.dialog.ShiftEditDialog.prototype.initForm = function(shift) {
    $('#' + this.dialogId + ' input[name=title]').val(shift.title);
    $('#' + this.dialogId + ' input[name=start_date]').val(shift.start_date);
    $('#' + this.dialogId + ' input[name=end_date]').val(shift.end_date);
    $('#' + this.dialogId + ' input[name=is_public]').prop('checked', shift.is_public);

    $('#' + this.dialogId + ' select[name=worker] >').remove();
    shift.worker_info.map(worker => {
        let $option = $('<option></option>');
        $option.val(worker.id);
        $option.text(worker.worker_detail.username);
        $('#' + this.dialogId + ' select[name=worker]').append($option);
    });
};

/**
 * 勤務表編集ダイアログを表示する処理
 */
shiftApp.dialog.ShiftEditDialog.prototype.showDialog = function(top, left) {

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

/**
 * 勤務表編集ダイアログを隠す処理
 */
shiftApp.dialog.ShiftEditDialog.prototype.hideDialog = function() {
    $('#' + this.dialogId).hide();
};

/**
 * 勤務表情報を取得する処理
 */
shiftApp.dialog.ShiftEditDialog.prototype.getShift = function(callback) {
    const url = '/shiftApp/shift/' + this.shiftId;
    $.ajax({
        url: url,
        type: 'GET',
        async: true,
    }).done(callback);
};

/**
 * 保存ボタン押下時の処理
 */
shiftApp.dialog.ShiftEditDialog.prototype.onClickSaveBtn = function() {

};

/**
 * 取り消しボタン押下時の処理
 */
shiftApp.dialog.ShiftEditDialog.prototype.onClickCancelBtn = function() {

};

/**
 * 閉じるボタン押下時の処理
 */
shiftApp.dialog.ShiftEditDialog.prototype.onClickCloseBtn = function() {
    this.hideDialog();
};
