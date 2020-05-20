/**
 * 勤務表作成機能画面共通クラス
 */
shiftApp.view.Abstract = function() { };

/**
 * サイドバーボタンのID
 */
shiftApp.view.Abstract.prototype.SIDEBAR_ID = {
    HOME: 'homeLink',
    SHIFT: 'shiftLink',
    WORKER: 'workerLink',
    WORK_PLAN: 'workPlanLink',
    WORK_STYLE: 'workStyleLink',
    SETTING: 'settingLink',
    APPS: 'appsLink',
};

/**
 * 画面初期化
 */
shiftApp.view.Abstract.prototype.initView = function() {
    $('#' + this.SIDEBAR_ID.HOME).click(this.onClickHome.bind(this));
    $('#' + this.SIDEBAR_ID.SETTING).click(this.onClickSetting.bind(this));
    $('#' + this.SIDEBAR_ID.APPS).click(this.onClickApps.bind(this));
};

/**
 * ホームボタン押下時のイベント
 */
shiftApp.view.Abstract.prototype.onClickHome = function() {
    window.location.href = '/shiftApp/';
};

/**
 * 設定ボタン押下時のイベント
 */
shiftApp.view.Abstract.prototype.onClickSetting = function() {
    window.location.href = '/shiftApp/setting/';
};

shiftApp.view.Abstract.prototype.onClickApps = function() {
    window.location.href = '/pages/app/list/';
};

