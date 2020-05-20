/**
 * 勤務表作成機能勤務表詳細小画面用クラス
 * @extends shiftApp.dialog.AbstractDialog
 */
shiftApp.dialog.ShiftDetailDialog = function(shiftId) {
	this.super = shiftApp.dialog.AbstractDialog.prototype;
	this.dialogId = 'shiftDetailView';
	this.shiftId = shiftId;
	this.ajaxUrl = '/shiftApp/shift/' + shiftId + '/';
	this.delegate = null;
	this.shiftDetailTable = null;
};
shiftApp.dialog.ShiftDetailDialog.prototype = new shiftApp.dialog.AbstractDialog();

/**
 * 勤務表詳細小画面を初期化する
 */
shiftApp.dialog.ShiftDetailDialog.prototype.initDialog = function() {
	this.shiftDetailTable = new shiftApp.table.ShiftDetailTable(this.shiftId);
	this.shiftDetailTable.initTable();

	$('#shfitEditBtn').off().click(this.onClickEditBtn.bind(this));
	$('#shiftDeleteBtn').off().click(this.onClickDeleteBtn.bind(this));
	$('#shfitInputPlanBtn').off().click(this.onClickShiftInputPlanBtn.bind(this));
	$('#shfitInputManuallyBtn').off().click(this.onClickShiftInputManuallyBtn.bind(this));
	$('#shiftDetailViewCloseBtn').off().click(this.onClickCloseBtn.bind(this));
	$('#shfitInputAutoBtn').off().click(this.onClickShiftInputAutoBtn.bind(this));
	// this.showDialog();
};

/**
 * 勤務表詳細ダイアログを表示する
 */
shiftApp.dialog.ShiftDetailDialog.prototype.showDialog = function() {
	this.initDialog();
	this.super.displayToFront(this.dialogId);
	$('#' + this.dialogId).show();
};

/**
 * 勤務表詳細ダイアログ編集ボタン押下時の処理
 */
shiftApp.dialog.ShiftDetailDialog.prototype.onClickEditBtn = function() {
	this.shiftEditDialog = new shiftApp.dialog.ShiftEditDialog(this.shiftId);
	const position = $('#shfitEditBtn').offset();
	this.shiftEditDialog.showDialog(position.top, position.left);
};

/**
 * 勤務表詳細小画面の閉じるボタン押下時の処理
 */
shiftApp.dialog.ShiftDetailDialog.prototype.onClickCloseBtn = function() {
	$('#' + this.dialogId).hide();
};

/**
 * 勤務表詳細小画面の削除ボタン押下時の処理
 */
shiftApp.dialog.ShiftDetailDialog.prototype.onClickDeleteBtn = function() {
	let self = this;
	if (window.confirm('Are you sure?')) {
		$.ajax({
			url: this.ajaxUrl,
			type: 'DELETE',
			beforeSend: function(xhr) {
				xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));
			}
		}).done(function() {
			$('#shiftDetailView').hide();
			shiftApp.table.object.shiftListTable.reload();
		}).fail(function(jqXHR, textStatus, errorThrown) {
			console.log('jqXHR: ' + jqXHR);
			console.log('textStatus: ' + textStatus);
			console.log('errorThrown: ' + errorThrown);
		});
	}
};

/**
 * 勤務表手動入力ボタン押下時の処理
 */
shiftApp.dialog.ShiftDetailDialog.prototype.onClickShiftInputManuallyBtn = function() {
	const self = this;
	this.defaultActionBtns = $('#shiftDetailView .actions');

	let $actions = $('<div class="actions"></div>');

	let $saveBtn = $('<button type="button" id="saveBtn" class="btn btn-primary">save</button>').click(function() {
		// TODO
	});

	let $doneBtn = $('<button type="button" id="doneBtn" class="btn btn-success">done</button>').click(function() {
		$('#shiftDetailView .actions').remove();
		$('#shiftDetailTableContainer').before(self.defaultActionBtns);
		self.initDialog();
	});

	$actions.append($saveBtn);
	$actions.append($doneBtn);
	$('#shiftDetailView .actions').remove();
	$('#shiftDetailTableContainer').before($actions);
	$('#shiftDetailView .actions .btn').css('margin-right', '4px');
	this.shiftDetailTable.showShiftInputManuallyTable();
};

/**
 * 勤務表計画入力ボタン押下時の処理
 */
shiftApp.dialog.ShiftDetailDialog.prototype.onClickShiftInputPlanBtn = function() {

	const self = this;

	this.defaultActionBtns = $('#shiftDetailView .actions');

	let $actions = $('<div class="actions"></div>');

	let $saveBtn = $('<button type="button" id="saveBtn" class="btn btn-primary">save</button>').click(function() {
		// TODO
	});

	let $doneBtn = $('<button type="button" id="doneBtn" class="btn btn-success">done</button>').click(function() {
		$('#shiftDetailView .actions').remove();
		$('#shiftDetailTableContainer').before(self.defaultActionBtns);
		self.initDialog();
	});

	$actions.append($saveBtn);
	$actions.append($doneBtn);
	$('#shiftDetailView .actions').remove();
	$('#shiftDetailTableContainer').before($actions);
	$('#shiftDetailView .actions .btn').css('margin-right', '4px');

	this.shiftDetailTable.showShiftInputPlanTable();
};

/**
 * 勤務表自動入力ボタン押下時の処理
 */
shiftApp.dialog.ShiftDetailDialog.prototype.onClickShiftInputAutoBtn = function() {

	const self = this;

	const $progressView = $('<div></div>');
	$progressView.attr({ id: 'progress' });
	$progressView.css({
		width: '100%',
		height: '100%',
		'z-index': '9999',
		'background-color': 'rgb(0,0,0,0.5)',
		position: 'absolute',
		left: 0,
		top: 0,
	});
	$('body').append($progressView);


	$('#shfitEditBtn').prop('disabled', true);
	$('#shiftDeleteBtn').prop('disabled', true);
	$('#shfitInputPlanBtn').prop('disabled', true);
	$('#shfitInputManuallyBtn').prop('disabled', true);
	$('#shiftDetailViewCloseBtn').prop('disabled', true);
	$('#shfitInputAutoBtn').prop('disabled', true);

	$.ajax({
		url: '/shiftApp/shift/input/' + this.shiftId + '/',
		type: 'POST',
		data: { 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val() }
	}).done(function(data) {
		if (data.success) {
			self.shiftDetailTable.datatable.ajax.reload(function() {
				$progressView.remove();
				$('#shfitEditBtn').prop('disabled', false);
				$('#shiftDeleteBtn').prop('disabled', false);
				$('#shfitInputPlanBtn').prop('disabled', false);
				$('#shfitInputManuallyBtn').prop('disabled', false);
				$('#shiftDetailViewCloseBtn').prop('disabled', false);
				$('#shfitInputAutoBtn').prop('disabled', false);
			});
		}
	});
};
