import json
import traceback

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from sc_new.models import DefnDs, DefnDsDtl, DefnType, DefnDm, DefnDr
from django.db.models import Q
from django.db import connection,connections
from django.forms import model_to_dict
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from sc_new.util import default, export_excel


def ds_dtl(request):
    return render(request, './data/ds_dtl.html', {})


def dm(request):
    return render(request, './data/dm.html', {})


def dr(request):
    return render(request, './data/dr.html', {})


@csrf_exempt
def get_types(request):
    strc_list = DefnType.objects.filter(Q(id_table=22), Q(id_column=356))
    incr_list = DefnType.objects.filter(Q(id_table=22), Q(id_column=357))
    strcs = []
    incrs = []
    for strc in strc_list:
        strcs.append(model_to_dict(strc))
    for incr in incr_list:
        incrs.append(model_to_dict(incr))
    return HttpResponse(json.dumps({
        "strcs": strcs,
        "incrs": incrs
    }, default=default), content_type="application_json")


@csrf_exempt
def ds_list(request):
    get = request.GET
    search = get.get("searchText")
    page_size = get.get("pageSize")
    page_number = get.get("pageNumber", 1)
    list = DefnDs.objects.all()
    if search is not None:
        type_list = DefnType.objects.filter(Q(id_table=22), Q(id_column=35), Q(name__icontains=search))
        type_layer = 'asdf'
        if len(search) > 0 and type_list.count() > 0:
            type_layer = type_list.__getitem__(0).code
        list = list.filter(Q(id__icontains=search) | Q(name__icontains=search) | Q(type_strc__icontains=type_layer))
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
def ds_edit(request):
    try:
        cursor = connection.cursor()
        id = request.POST.get('id')
        if id is not None:
            m = DefnDs.objects.get(id=id)
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
            if DefnDs.objects.count() == 0:
                _id = 1
            else:
                _m = DefnDs.objects.latest('id')
                if _m is not None:
                    _id = _m.id + 1
                else:
                    _id = 1
            cursor.execute("insert into defn_ds(id) values (%s)", [_id])
        flag = True
    except:
        print(traceback.format_exc())
        flag = False
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def ds_del(request):
    try:
        id = request.POST.get('id')
        DefnDs.objects.extra(where=['id IN (' + id + ')']).delete()
        # 删除对应明细
        DefnDsDtl.objects.extra(where=['id_ds IN (' + id + ')']).delete()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def ds_copy(request):
    try:
        id = request.POST.get('id')
        list = DefnDs.objects.extra(where=['id IN (' + id + ')']).all()
        for m in list:
            ds_dtl_list = DefnDsDtl.objects.filter(id_ds=m.id)
            m.id = None
            m.save()
            _m = DefnDs.objects.latest('id')
            for m_dtl in ds_dtl_list:
                m_dtl.id = None
                m_dtl.id_ds = _m.id
                m_dtl.save()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def ds_dtl_list(request):
    get = request.GET
    search = get.get("searchText")
    page_size = get.get("pageSize")
    page_number = get.get("pageNumber", 1)
    id_ds = get.get("id_ds")
    list = DefnDsDtl.objects.filter(id_ds=id_ds)
    if search is not None:
        list = list.filter(Q(id__icontains=search) | Q(code__icontains=search) | Q(name__icontains=search))
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
def ds_dtl_edit(request):
    try:
        cursor = connection.cursor()
        id = request.POST.get('id')
        if id is not None:
            m = DefnDsDtl.objects.get(id=id)
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
            if DefnDsDtl.objects.count() == 0:
                _id = 1
            else:
                _m = DefnDsDtl.objects.latest('id')
                if _m is not None:
                    _id = _m.id + 1
                else:
                    _id = 1
            cursor.execute("insert into defn_ds_dtl(id,id_ds) values (%s,%s)", [_id, val])
        flag = True
    except:
        print(traceback.format_exc())
        flag = False
    return HttpResponse(json.dumps({
        'flag': flag
    }), content_type="application_json")


@csrf_exempt
def ds_dtl_del(request):
    try:
        id = request.POST.get('id')
        DefnDsDtl.objects.extra(where=['id IN (' + id + ')']).delete()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def ds_dtl_copy(request):
    try:
        id = request.POST.get('id')
        list = DefnDsDtl.objects.extra(where=['id IN (' + id + ')']).all()
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
def dm_list(request):
    get = request.GET
    search = get.get("searchText")
    page_size = get.get("pageSize")
    page_number = get.get("pageNumber", 1)
    list = DefnDm.objects.all()
    if search is not None:
        list = list.filter(Q(id__icontains=search) | Q(name__icontains=search))
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
def dm_edit(request):
    try:
        cursor = connection.cursor()
        id = request.POST.get('id')
        if id is not None:
            m = DefnDm.objects.get(id=id)
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
            if DefnDm.objects.count() == 0:
                _id = 1
            else:
                _m = DefnDm.objects.latest('id')
                if _m is not None:
                    _id = _m.id + 1
                else:
                    _id = 1
            cursor.execute("insert into defn_dm(id) values (%s)", [_id])
        flag = True
    except:
        print(traceback.format_exc())
        flag = False
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def dm_del(request):
    try:
        id = request.POST.get('id')
        DefnDm.objects.extra(where=['id IN (' + id + ')']).delete()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def dm_copy(request):
    try:
        id = request.POST.get('id')
        list = DefnDm.objects.extra(where=['id IN (' + id + ')']).all()
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
def dr_list(request):
    get = request.GET
    search = get.get("searchText")
    page_size = get.get("pageSize")
    page_number = get.get("pageNumber", 1)
    list = DefnDr.objects.all()
    if search is not None:
        list = list.filter(Q(id__icontains=search) | Q(name__icontains=search))
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
def dr_edit(request):
    try:
        cursor = connection.cursor()
        id = request.POST.get('id')
        if id is not None:
            m = DefnDr.objects.get(id=id)
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
            if DefnDr.objects.count() == 0:
                _id = 1
            else:
                _m = DefnDr.objects.latest('id')
                if _m is not None:
                    _id = _m.id + 1
                else:
                    _id = 1
            cursor.execute("insert into defn_dr(id) values (%s)", [_id])
        flag = True
    except:
        print(traceback.format_exc())
        flag = False
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def dr_del(request):
    try:
        id = request.POST.get('id')
        DefnDr.objects.extra(where=['id IN (' + id + ')']).delete()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def dr_copy(request):
    try:
        id = request.POST.get('id')
        list = DefnDr.objects.extra(where=['id IN (' + id + ')']).all()
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
def dm_query(request):
    try:
        id = request.POST.get('id')
        list = DefnDm.objects.filter(id=id)
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


@csrf_exempt
def dr_query(request):
    try:
        id = request.POST.get('id')
        list = DefnDr.objects.filter(id=id)
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


def dm_excel_export(request):
    try:
        id = request.GET.get('id')
        list = DefnDm.objects.filter(id=id)
        if list.count() == 1:
            logic = list.__getitem__(0).logic
            cursor = connections['data'].cursor()
            cursor.execute(logic)
            result = cursor.fetchall()
    except:
        print(traceback.format_exc())
    if result:
        return export_excel(result)


def dr_excel_export(request):
    try:
        id = request.GET.get('id')
        list = DefnDr.objects.filter(id=id)
        if list.count() == 1:
            logic = list.__getitem__(0).logic
            cursor = connections['data'].cursor()
            cursor.execute(logic)
            result = cursor.fetchall()
    except:
        print(traceback.format_exc())
    if result:
        return export_excel(result)
