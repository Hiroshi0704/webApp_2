/**
 * 勤務表作成機能ホーム画面用クラス
 * @extends shiftApp.view.Abstract
 */
shiftApp.view.Home = function() {
    this.VIEW_ID = 'shiftAppHome';
    this.super = shiftApp.view.Abstract.prototype;
    this.shiftListDialog = new shiftApp.dialog.ShiftListDialog();
};
shiftApp.view.Home.prototype = new shiftApp.view.Abstract();

/**
 * 勤務表作成機能ホーム画面初期化
 */
shiftApp.view.Home.prototype.initView = function() {
    this.super.initView.call(this);

    $('#shiftView').draggable();
    $('#shiftDetailView').draggable();

    $('.view').mousedown(function() {
        let views = [];
        let thisIndex;
        const self = this;

        $('.view').each(function(i) {
            views[i] = {
                view: this,
                zIndex: Number($(this).css('z-index')) || 0,
            };

            if (this === self) {
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
    });

    // ----- 小画面の初期化 -----
    this.shiftListDialog.initView();
    shiftApp.dialog.object.shiftListDialog = this.shiftListDialog;

    // ----- イベント設定 -----
    $('#' + this.SIDEBAR_ID.SHIFT).click(this.onClickShift.bind(this));
    $('#' + this.SIDEBAR_ID.WORKER).click(this.onClickWorker.bind(this));
    $('#' + this.SIDEBAR_ID.WORK_PLAN).click(this.onClickWorkPlan.bind(this));
    $('#' + this.SIDEBAR_ID.WORK_STYLE).click(this.onClickWorkStyle.bind(this));
};

/**
 * 勤務表押下時のイベント
 */
shiftApp.view.Home.prototype.onClickShift = function() {
    $('#shiftView').show();
    this.shiftListDialog.shiftListTable.reload();
};

/**
 * 従業員押下時のイベント
 */
shiftApp.view.Home.prototype.onClickWorker = function() {

};

/**
 * 勤務計画押下時のイベント
 */
shiftApp.view.Home.prototype.onClickWorkPlan = function() {

};

/**
 * 勤務形態押下時のイベント
 */
shiftApp.view.Home.prototype.onClickWorkStyle = function() {

};

$(function() {
    shiftApp.view.object.home = new shiftApp.view.Home();
    shiftApp.view.object.home.initView();
});
