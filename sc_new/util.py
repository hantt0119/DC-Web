import traceback
from io import *
from decimal import Decimal
from datetime import date, datetime
from django.http import HttpResponse

from xlwt import Workbook


def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(obj, date):
        return obj.strftime("%Y-%m-%d")
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)


def validTLanuch(timeStr):
    try:
        if timeStr is not None and len(timeStr) == 6:
            return [int(timeStr[0:2]), int(timeStr[2:4]), int(timeStr[4:6])]
    except ValueError:
        print(traceback.format_exc())
        return None


def export_excel(data):
    """
    导出excel表格
    """
    # 创建工作薄
    ws = Workbook(encoding='utf-8')
    w = ws.add_sheet(u"数据")
    # 写入数据
    excel_row = 1
    for obj in data:
        index = len(obj)
        for i in range(index):
            w.write(excel_row, i, obj[i])
        excel_row += 1
    sio = BytesIO()
    ws.save(sio)
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=export.xls'
    response.write(sio.getvalue())
    return response
