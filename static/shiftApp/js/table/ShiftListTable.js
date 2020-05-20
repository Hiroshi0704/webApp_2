/**
 * 勤務表作成機能の勤務表一覧テーブル用クラス
 * @extends shiftApp.table.AbstractTable
 */
shiftApp.table.ShiftListTable = function() {
    this.super = shiftApp.table.AbstractTable.prototype;
    this.tableId = 'shiftTable';
    this.ajaxUrl = '/shiftApp/shift/';
};
shiftApp.table.ShiftListTable.prototype = new shiftApp.table.AbstractTable();

/**
 * 勤務表一覧テーブル初期化
 */
shiftApp.table.ShiftListTable.prototype.initTable = function() {

    const table = $('#' + this.tableId).DataTable({
        ajax: {
            'processing': true,
            'url': this.ajaxUrl,
            'data': function() { },
            'dataSrc': '',
        },
        initComplete: this.setTableEvent.bind(this),
        ordering: false,
        deferRender: true,
        scrollX: true,
        columns: [
            {
                'data': 'title',
                'render': function(data, type, full, meta) {
                    return '<a href="#" class="shiftDetailBtn" dataId="' + full.id + '">' + data + '</a>';
                }
            },
            { 'data': 'start_date' },
            { 'data': 'end_date' },
        ],
    });

    const self = this;

    table.on('draw', function() {
        self.setTableEvent();
    });
}

/**
 * 勤務表一覧テーブルのイベントを設定
 */
shiftApp.table.ShiftListTable.prototype.setTableEvent = function() {
    $('.shiftDetailBtn').off();
    $('.shiftDetailBtn').click(function() {
        shiftApp.dialog.object.shiftDetailDialog = new shiftApp.dialog.ShiftDetailDialog($(this).attr('dataId'));
        const position = $(this).offset();
        shiftApp.dialog.object.shiftDetailDialog.showDialog(position.top, position.left);
        return false;
    });
};

/**
 * 勤務表テーブルのデータを再読み込み
 */
shiftApp.table.ShiftListTable.prototype.reload = function() {
    $('#' + this.tableId).DataTable().ajax.reload(this.setTableEvent.bind(this), true);
};

/**
 * 勤務表削除時に呼ばれる処理
 */
shiftApp.table.ShiftListTable.prototype.shiftDeleted = function() {
    this.reload();
};
