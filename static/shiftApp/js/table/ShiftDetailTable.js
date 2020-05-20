/**
 * 勤務表詳細テーブル用クラス
 * @extends shiftApp.table.AbstractTable
 */
shiftApp.table.ShiftDetailTable = function(shiftId) {
	this.tableId = 'shiftDetailTable';
	this.shiftId = shiftId;
	this.getDayRangeUrl = '/shiftApp/shift/table/day_range/';
	this.getScheduleUrl = '/shiftApp/shift/table/schedule/';
	this.super = shiftApp.table.AbstractTable.prototype;
	this.columns = null;
	this.dayRange = null;
	this.datatable = null;
	this.workStyles = null;
	this.workPlan = null;
	this.$daysTableHeadTr = null;
	this.$planTableHeadTr = null;
};
shiftApp.table.ShiftDetailTable.prototype = new shiftApp.table.AbstractTable();

/**
 * 勤務表詳細画面初期化
 */
shiftApp.table.ShiftDetailTable.prototype.initTable = function() {
	// 勤務表テーブルを削除
	$('#shiftDetailTableContainer > ').remove();
	// テーブルを再度生成する
	const $table = this.generateTable();
	$('#shiftDetailTableContainer').append($table);
	this.getShiftDetailData().done(this.setShiftDetailDataToTable.bind(this));
	// 画面を表示する
	$('.shiftDetailView').show();
};

shiftApp.table.ShiftDetailTable.prototype.generateTable = function() {
	let $table = $('<table></table>');
	$table.attr({
		id: this.tableId,
		class: 'table table-striped table-bordered',
	});
	return $table;
};

/**
 * 勤務表のテーブルデータを取得する
 */
shiftApp.table.ShiftDetailTable.prototype.getShiftDetailData = function() {

	let response = $.ajax({
		url: this.getDayRangeUrl + this.shiftId,
		type: 'GET',
	});

	return response;
};

/**
 * 勤務表テーブルデータを画面に反映させる
 * @param data 勤務表データ
 */
shiftApp.table.ShiftDetailTable.prototype.setShiftDetailDataToTable = function(data) {
	this.dayRange = data['day_range'];

	// 勤務表の日付を作成
	$thead = $('<thead></thead>');
	$tr = $('<tr></tr>');
	$tr.append('<th></th>');
	for (let day in data['day_range']) {
		$tr.append('<th>' + data['day_range'][day] + '</th>');
	}
	$thead.append($tr);
	this.$daysTableHeadTr = $tr;
	$('#shiftDetailTable').append($thead);

	// 勤務表の内容を作成
	this.columns = [{ 'data': 'worker.worker_detail.username' }];
	for (let day in data['day_range']) {
		this.columns.push({ 'data': data['day_range'][day] + '.work_style.symbol', 'defaultContent': '' });
	}
	this.datatable = $('#shiftDetailTable').DataTable({
		scrollX: true,
		info: false,
		paging: false,
		ordering: false,
		searching: false,
		ajax: {
			'processing': true,
			'url': '/shiftApp/shift/table/schedule/' + this.shiftId + '/',
			'data': function() { },
			'dataSrc': '',
		},
		columns: this.columns,
	});
};

/**
 * 勤務表手動入力画面を表示する
 */
shiftApp.table.ShiftDetailTable.prototype.showShiftInputManuallyTable = function() {

	let self = this;

	if (this.workStyles === null) {
		this.getWorkStyles().done(function(data) {
			self.workStyles = data;
			self.initShiftInputManuallyTable();
		});
	} else {
		this.initShiftInputManuallyTable();
	}

};

/**
 * 勤務形態を取得する
 * @returns レスポンス
 */
shiftApp.table.ShiftDetailTable.prototype.getWorkStyles = function() {

	let response = $.ajax({
		type: 'GET',
		url: '/shiftApp/ajax/work_style/',
	});

	return response;
};

/**
 * 勤務表手動入力表初期化処理
 */
shiftApp.table.ShiftDetailTable.prototype.initShiftInputManuallyTable = function() {

	let self = this;

	let columns = [];
	columns.push(this.columns[0]);

	for (let day in this.dayRange) {
		columns.push({
			'data': this.dayRange[day] + '.work_style.id',
			'defaultContent': '',
			'render': function(data, type, row, meta) {
				let workerId = row['worker'].id;
				let scheId = row[self.dayRange[meta.col - 1]].id;
				let $select = $('<select name="' + workerId + '-' + scheId + '" class="form-control" style="width: auto;"></select>');
				$select.append('<option value=""></option>');
				for (let key in self.workStyles) {
					let style = self.workStyles[key];
					let $option = $('<option value="' + key + '">' + style.symbol + '</option>');
					if (style.id == data) {
						$option.attr('selected', 'selected');
					}
					$select.append($option);
				}
				return $select[0].outerHTML;
			}
		});
	}

	this.datatable.destroy();

	// テーブルを再度生成する
	$('#shiftDetailTableContainer > ').remove();
	const $table = this.generateTable();
	$('#shiftDetailTableContainer').append($table);

	// テーブルヘッド
	const $thead = $('<thead></thead>');
	$thead.append(this.$daysTableHeadTr);
	$table.append($thead);

	this.datatable = $('#shiftDetailTable').DataTable({
		scrollX: true,
		info: false,
		paging: false,
		ordering: false,
		searching: false,
		ajax: {
			'processing': true,
			'url': '/shiftApp/shift/table/schedule/' + this.shiftId + '/',
			'data': function() { },
			'dataSrc': '',
		},
		columns: columns
	});
};

/**
 * 勤務計画入力表表示処理
 */
shiftApp.table.ShiftDetailTable.prototype.showShiftInputPlanTable = function() {

	const self = this;

	if (this.workStyles === null) {
		this.getWorkPlan().done(function(data) {
			self.workPlan = data;
			self.initShiftInputPlanTable();
		});
	} else {
		this.initShiftInputPlanTable();
	}
};

/**
 * 勤務計画を取得する
 */
shiftApp.table.ShiftDetailTable.prototype.getWorkPlan = function() {

	let response = $.ajax({
		type: 'GET',
		url: '/shiftApp/ajax/work_plan/',
	});

	return response;
};

/**
 * 勤務計画入力表初期化処理
 */
shiftApp.table.ShiftDetailTable.prototype.initShiftInputPlanTable = function() {

	const self = this;

	// テーブルを再度生成する
	$('#shiftDetailTableContainer > ').remove();
	const $table = this.generateTable();
	$('#shiftDetailTableContainer').append($table);

	// テーブルヘッド
	const $thead = $('<thead></thead>');

	// 勤務計画選択行
	const $workPlanTr = $('<tr></tr>');
	$workPlanTr.append('<th></th>');
	this.getWorkPlan().done(function(workPlans) {
		for (let day in self.dayRange) {
			let $th = $('<th></th>');
			let $select = $('<select></select>');
			$select.attr({
				name: day,
				class: 'form-control',
				style: 'width: auto;'
			});
			for (let i in workPlans) {
				let $option = $('<option></option>');
				$option.text(workPlans[i].title);
				$option.attr({ value: workPlans[i].id });
				$select.append($option);
			}
			$th.append($select);
			$workPlanTr.append($th);
		}
	});

	$thead.append($workPlanTr);
	$thead.append(this.$daysTableHeadTr);
	$table.append($thead);

	this.datatable = $('#shiftDetailTable').DataTable({
		scrollX: true,
		info: false,
		paging: false,
		ordering: false,
		searching: false,
		ajax: {
			'processing': true,
			'url': '/shiftApp/shift/table/schedule/' + this.shiftId + '/',
			'data': function() { },
			'dataSrc': '',
		},
		columns: this.columns
	});
};


