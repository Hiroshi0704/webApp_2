/**
 * 勤務表作成機能設定画面用クラス
 * @extends shiftApp.view.Abstract
 */
shiftApp.view.Setting = function() {
    this.VIEW_ID = 'shiftAppSetting';
    this.super = shiftApp.view.Abstract.prototype;
}
shiftApp.view.Setting.prototype = new shiftApp.view.Abstract();

/**
 * 勤務表作成機能設定画面初期化
 */
shiftApp.view.Setting.prototype.initView = function() {
    this.super.initView.call(this);
    $('#' + this.SIDEBAR_ID.SHIFT).prop('disabled', true);
    $('#' + this.SIDEBAR_ID.WORKER).prop('disabled', true);
    $('#' + this.SIDEBAR_ID.WORK_PLAN).prop('disabled', true);
    $('#' + this.SIDEBAR_ID.WORK_STYLE).prop('disabled', true);
}

$(function() {
    shiftApp.view.object.setting = new shiftApp.view.Setting();
    shiftApp.view.object.setting.initView();
});
