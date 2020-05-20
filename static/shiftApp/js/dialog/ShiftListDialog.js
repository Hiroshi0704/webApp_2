/**
 * 勤務表作成機能勤務表一覧小画面用クラス
 * @extends shiftApp.dialog.AbstractDialog
 */
shiftApp.dialog.ShiftListDialog = function() {
	this.super = shiftApp.dialog.AbstractDialog.prototype;
	this.dialogId = 'shiftView';
};
shiftApp.dialog.ShiftListDialog.prototype = new shiftApp.dialog.AbstractDialog();

/**
 * 勤務表一覧小画面を初期化する
 */
shiftApp.dialog.ShiftListDialog.prototype.initView = function() {

	// 勤務表一覧テーブル初期化
	shiftApp.table.object.shiftListTable = new shiftApp.table.ShiftListTable();
	shiftApp.table.object.shiftListTable.initTable();

	// 閉じるボタン押下時
	$('#shiftViewCloseBtn').click(this.onClickCloseBtn.bind(this));
	$('#createShiftBtn').click(this.onClickCreateShiftBtn.bind(this));
};

/**
 * 勤務表一覧小画面の閉じるボタン押下時の処理
 */
shiftApp.dialog.ShiftListDialog.prototype.onClickCloseBtn = function() {
	$('#' + this.dialogId).hide();
};

/**
 * 勤務表一覧小画面を生成する
 */
shiftApp.dialog.ShiftListDialog.prototype.createView = function() {

};

/**
 * 勤務表一覧小画面を削除する
 */
shiftApp.dialog.ShiftListDialog.prototype.deleteView = function() {

};

shiftApp.dialog.ShiftListDialog.prototype.onClickCreateShiftBtn = function() {
	shiftApp.dialog.object.createShiftDialog = new shiftApp.dialog.ShiftCreateDialog();

	const top = $('#createShiftBtn').offset().top;
	const left = $('#createShiftBtn').offset().left;
	shiftApp.dialog.object.createShiftDialog.showDialog(top, left);

};