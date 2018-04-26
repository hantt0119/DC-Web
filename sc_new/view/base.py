import json
import traceback

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from sc_new.models import DefnTable, DefnTableDtl, DefnView, DefnDType, DefnType, DefnError
from django.db.models import Q
from django.db import connection,connections
from django.forms import model_to_dict
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from sc_new.util import default, export_excel


def table_view(request):
    return render(request, './base/base_table.html', {})


def dtype_type_error(request):
    return render(request, './base/dtype_type_error.html', {})


@csrf_exempt
def table_list(request):
    get = request.GET
    search = get.get("searchText")
    page_size = get.get("pageSize")
    page_number = get.get("pageNumber", 1)
    list = DefnTable.objects.all()
    if search is not None:
        list = list.filter(Q(id__icontains=search) | Q(code_new__icontains=search) | Q(code_nuser__icontains=search))
    # 计算搜索之后的总数
    total = list.count()
    rows = []
    list = list.order_by("-id")
    # 分页
    paginator = Paginator(list, page_size)
    try:
        list = paginator.page(page_number)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    for m in list:
        dic = model_to_dict(m)
        rows.append(dic)
    result = {
        "total": total,
        "rows": rows
    }
    return HttpResponse(json.dumps(result, default=default), content_type="application_json")


@csrf_exempt
def table_edit(request):
    try:
        cursor = connection.cursor()
        id = request.POST.get('id')
        if id is not None:
            m = DefnTable.objects.get(id=id)
            names = request.POST.get('name')
            vals = request.POST.get('value')
            name_arr = names.split(";")
            val_arr = vals.split(";")
            # 设置Field值
            for i in range(len(name_arr)):
                name = name_arr[i]
                _val = val_arr[i]
                # 设置Field值
                m.__setattr__(name, _val)
            m.save(update_fields=name_arr)
        else:
            _m = DefnTable.objects.filter(id__isnull=False).latest('id')
            if _m is not None:
                _id = _m.id + 1
            else:
                _id = 1
            cursor.execute("insert into defn_table(id) values (%s)", [_id])
        flag = True
    except:
        print(traceback.format_exc())
        flag = False
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def table_del(request):
    try:
        id = request.POST.get('id')
        DefnTable.objects.extra(where=['id IN (' + id + ')']).delete()
        # 删除对应的明细
        DefnTableDtl.objects.extra(where=['id_table IN (' + id + ')']).delete()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def table_copy(request):
    try:
        id = request.POST.get('id')
        list = DefnTable.objects.extra(where=['id IN (' + id + ')']).all()
        for m in list:
            table_dtl_list = DefnTableDtl.objects.filter(id_table=m.id)
            m.id = None
            m.save()
            _m = DefnTable.objects.latest('id')
            for m_dtl in table_dtl_list:
                m_dtl.id = None
                m_dtl.id_table = _m.id
                m_dtl.save()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def table_create(request):
    try:
        cursor = connection.cursor()  # 获得一个游标(cursor)对象
        cursor.execute('select fnc_table()')
        result = cursor.fetchone()
        flag = result[0]
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def table_dtl_list(request):
    get = request.GET
    search = get.get("searchText")
    page_size = get.get("pageSize")
    page_number = get.get("pageNumber", 1)
    id_table = get.get("id_table")
    list = DefnTableDtl.objects.filter(id_table=id_table)
    if search is not None:
        list = list.filter(Q(id__icontains=search) | Q(code_new__icontains=search) | Q(name__icontains=search))
    # 计算搜索之后的总数
    total = list.count()
    rows = []
    list = list.order_by("sn")
    # 分页
    paginator = Paginator(list, page_size)
    try:
        list = paginator.page(page_number)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    for m in list:
        dic = model_to_dict(m)
        rows.append(dic)
    result = {
        "total": total,
        "rows": rows
    }
    return HttpResponse(json.dumps(result, default=default), content_type="application_json")


@csrf_exempt
def table_dtl_edit(request):
    try:
        cursor = connection.cursor()
        id = request.POST.get('id')
        if id is not None:
            m = DefnTableDtl.objects.get(id=id)
            names = request.POST.get('name')
            vals = request.POST.get('value')
            name_arr = names.split(";")
            val_arr = vals.split(";")
            # 设置Field值
            for i in range(len(name_arr)):
                name = name_arr[i]
                _val = val_arr[i]
                # 设置Field值
                m.__setattr__(name, _val)
            m.save(update_fields=name_arr)
        else:
            val = request.POST.get('value')
            _m = DefnTableDtl.objects.latest('id')
            if _m is not None:
                _id = _m.id + 1
            else:
                _id = 1
            _m = DefnTableDtl.objects.filter(Q(id_table=val)).latest('sn')
            if _m is not None:
                sn = _m.sn + 1
            else:
                sn = 1
            cursor.execute("insert into defn_table_dtl(id,id_table,sn) values (%s,%s,%s)", [_id, val, sn])
        flag = True
    except:
        print(traceback.format_exc())
        flag = False
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def table_dtl_del(request):
    try:
        id = request.POST.get('id')
        DefnTableDtl.objects.extra(where=['id IN (' + id + ')']).delete()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def table_dtl_copy(request):
    try:
        id = request.POST.get('id')
        list = DefnTableDtl.objects.extra(where=['id IN (' + id + ')']).all()
        for m in list:
            m.id = None
            m.save()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def view_list(request):
    get = request.GET
    search = get.get("searchText")
    page_size = get.get("pageSize")
    page_number = get.get("pageNumber", 1)
    list = DefnView.objects.all()
    if search is not None:
        list = list.filter(Q(id__icontains=search) | Q(code_new__icontains=search) | Q(code_nuser__icontains=search))
    # 计算搜索之后的总数
    total = list.count()
    rows = []
    list = list.order_by("-id")
    # 分页
    paginator = Paginator(list, page_size)
    try:
        list = paginator.page(page_number)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    for m in list:
        dic = model_to_dict(m)
        rows.append(dic)
    result = {
        "total": total,
        "rows": rows
    }
    return HttpResponse(json.dumps(result, default=default), content_type="application_json")


@csrf_exempt
def view_edit(request):
    try:
        cursor = connection.cursor()
        id = request.POST.get('id')
        if id is not None:
            m = DefnView.objects.get(id=id)
            names = request.POST.get('name')
            vals = request.POST.get('value')
            name_arr = names.split(";")
            val_arr = vals.split(";")
            # 设置Field值
            for i in range(len(name_arr)):
                name = name_arr[i]
                _val = val_arr[i]
                # 设置Field值
                m.__setattr__(name, _val)
            m.save(update_fields=name_arr)
        else:
            if DefnView.objects.count() == 0:
                _id = 1
            else:
                _m = DefnView.objects.latest('id')
                if _m is not None:
                    _id = _m.id + 1
                else:
                    _id = 1
            cursor.execute("insert into defn_view(id) values (%s)", [_id])
        flag = True
    except:
        print(traceback.format_exc())
        flag = False
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def view_del(request):
    try:
        id = request.POST.get('id')
        DefnView.objects.extra(where=['id IN (' + id + ')']).delete()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def view_copy(request):
    try:
        id = request.POST.get('id')
        list = DefnView.objects.extra(where=['id IN (' + id + ')']).all()
        for m in list:
            m.id = None
            m.save()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def view_create(request):
    try:
        cursor = connection.cursor()  # 获得一个游标(cursor)对象
        cursor.execute('select fnc_view()')
        result = cursor.fetchone()
        flag = result[0]
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def view_query(request):
    try:
        id = request.POST.get('id')
        list = DefnView.objects.filter(id=id)
        if list.count() == 1:
            logic = list.__getitem__(0).logic
            cursor = connections['data'].cursor()
            cursor.execute(logic)
            result = cursor.fetchall()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        "data": result,
        "flag": flag
    }, default=default), content_type="application_json")


def view_excel_export(request):
    try:
        id = request.GET.get('id')
        list = DefnView.objects.filter(id=id)
        if list.count() == 1:
            logic = list.__getitem__(0).logic
            cursor = connections['data'].cursor()
            cursor.execute(logic)
            result = cursor.fetchall()
    except:
        print(traceback.format_exc())
    if result:
        return export_excel(result)


@csrf_exempt
def d_type_list(request):
    get = request.GET
    search = get.get("searchText")
    page_size = get.get("pageSize")
    page_number = get.get("pageNumber", 1)
    list = DefnDType.objects.all()
    if search is not None:
        list = list.filter(Q(id__icontains=search) | Q(code__icontains=search) | Q(name__icontains=search))
    # 计算搜索之后的总数
    total = list.count()
    rows = []
    list = list.order_by("-id")
    # 分页
    paginator = Paginator(list, page_size)
    try:
        list = paginator.page(page_number)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    for m in list:
        dic = model_to_dict(m)
        rows.append(dic)
    result = {
        "total": total,
        "rows": rows
    }
    return HttpResponse(json.dumps(result, default=default), content_type="application_json")


@csrf_exempt
def d_type_edit(request):
    try:
        cursor = connection.cursor()
        id = request.POST.get('id')
        if id is not None:
            m = DefnDType.objects.get(id=id)
            names = request.POST.get('name')
            vals = request.POST.get('value')
            name_arr = names.split(";")
            val_arr = vals.split(";")
            # 设置Field值
            for i in range(len(name_arr)):
                name = name_arr[i]
                _val = val_arr[i]
                # 设置Field值
                m.__setattr__(name, _val)
            m.save(update_fields=name_arr)
        else:
            if DefnDType.objects.count() == 0:
                _id = 1
            else:
                _m = DefnDType.objects.latest('id')
                if _m is not None:
                    _id = _m.id + 1
                else:
                    _id = 1
            cursor.execute("insert into defn_dtype(id) values (%s)", [_id])
        flag = True
    except:
        print(traceback.format_exc())
        flag = False
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def d_type_del(request):
    try:
        id = request.POST.get('id')
        DefnDType.objects.extra(where=['id IN (' + id + ')']).delete()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def d_type_copy(request):
    try:
        id = request.POST.get('id')
        list = DefnDType.objects.extra(where=['id IN (' + id + ')']).all()
        for m in list:
            m.id = None
            m.save()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def type_list(request):
    get = request.GET
    search = get.get("searchText")
    page_size = get.get("pageSize")
    page_number = get.get("pageNumber", 1)
    list = DefnType.objects.all()
    if search is not None:
        list = list.filter(Q(id__icontains=search) | Q(code__icontains=search) | Q(name__icontains=search))
    # 计算搜索之后的总数
    total = list.count()
    rows = []
    list = list.order_by("-id")
    # 分页
    paginator = Paginator(list, page_size)
    try:
        list = paginator.page(page_number)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    for m in list:
        dic = model_to_dict(m)
        rows.append(dic)
    result = {
        "total": total,
        "rows": rows
    }
    return HttpResponse(json.dumps(result, default=default), content_type="application_json")


@csrf_exempt
def type_edit(request):
    try:
        cursor = connection.cursor()
        id = request.POST.get('id')
        if id is not None:
            m = DefnType.objects.get(id=id)
            names = request.POST.get('name')
            vals = request.POST.get('value')
            name_arr = names.split(";")
            val_arr = vals.split(";")
            # 设置Field值
            for i in range(len(name_arr)):
                name = name_arr[i]
                _val = val_arr[i]
                # 设置Field值
                m.__setattr__(name, _val)
            m.save(update_fields=name_arr)
        else:
            if DefnType.objects.count() == 0:
                _id = 1
            else:
                _m = DefnType.objects.latest('id')
                if _m is not None:
                    _id = _m.id + 1
                else:
                    _id = 1
            cursor.execute("insert into defn_type(id) values (%s)", [_id])
        flag = True
    except:
        print(traceback.format_exc())
        flag = False
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def type_del(request):
    try:
        id = request.POST.get('id')
        DefnType.objects.extra(where=['id IN (' + id + ')']).delete()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def type_copy(request):
    try:
        id = request.POST.get('id')
        list = DefnType.objects.extra(where=['id IN (' + id + ')']).all()
        for m in list:
            m.id = None
            m.save()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def error_list(request):
    get = request.GET
    search = get.get("searchText")
    page_size = get.get("pageSize")
    page_number = get.get("pageNumber", 1)
    list = DefnError.objects.all()
    if search is not None:
        list = list.filter(Q(id__icontains=search) | Q(code__icontains=search) | Q(name__icontains=search))
    # 计算搜索之后的总数
    total = list.count()
    rows = []
    list = list.order_by("-id")
    # 分页
    paginator = Paginator(list, page_size)
    try:
        list = paginator.page(page_number)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    for m in list:
        dic = model_to_dict(m)
        rows.append(dic)
    result = {
        "total": total,
        "rows": rows
    }
    return HttpResponse(json.dumps(result, default=default), content_type="application_json")


@csrf_exempt
def error_edit(request):
    try:
        cursor = connection.cursor()
        id = request.POST.get('id')
        if id is not None:
            m = DefnError.objects.get(id=id)
            names = request.POST.get('name')
            vals = request.POST.get('value')
            name_arr = names.split(";")
            val_arr = vals.split(";")
            # 设置Field值
            for i in range(len(name_arr)):
                name = name_arr[i]
                _val = val_arr[i]
                # 设置Field值
                m.__setattr__(name, _val)
            m.save(update_fields=name_arr)
        else:
            if DefnError.objects.count() == 0:
                _id = 1
            else:
                _m = DefnError.objects.latest('id')
                if _m is not None:
                    _id = _m.id + 1
                else:
                    _id = 1
            cursor.execute("insert into defn_error(id) values (%s)", [_id])
        flag = True
    except:
        print(traceback.format_exc())
        flag = False
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def error_del(request):
    try:
        id = request.POST.get('id')
        DefnError.objects.extra(where=['id IN (' + id + ')']).delete()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def error_copy(request):
    try:
        id = request.POST.get('id')
        list = DefnError.objects.extra(where=['id IN (' + id + ')']).all()
        for m in list:
            m.id = None
            m.save()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")
