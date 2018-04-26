import json
import traceback
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from sc_new.models import DefnProg, DefnType, DefnProgDtl, DefnInst, DefnAide, DefnError, DefnProc, DefnSchd
from django.db.models import Q
from django.db import connection
from django.forms import model_to_dict
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from sc_new.util import default
from sc_new.task import run_schd


def prog_dtl(request):
    return render(request, './action/prog_dtl.html', {})


def inst_prog_aide(request):
    return render(request, './action/inst_prog_aide.html', {})


def proc_inst_aide(request):
    return render(request, './action/proc_inst_aide.html', {})


def schd_proc_aide(request):
    return render(request, './action/schd_proc_aide.html', {})


@csrf_exempt
def get_type_layers(request):
    type_list = DefnType.objects.filter(Q(id_table=10), Q(id_column=107))
    rows = []
    for type in type_list:
        rows.append(model_to_dict(type))
    return HttpResponse(json.dumps(rows, default=default), content_type="application_json")


@csrf_exempt
def prog_list(request):
    get = request.GET
    search = get.get("searchText")
    page_size = get.get("pageSize")
    page_number = get.get("pageNumber", 1)
    type_layer = get.get("type_layer")
    p_list = DefnProg.objects.filter(type_layer=type_layer)
    if search is not None:
        p_list = p_list.filter(Q(id__icontains=search) | Q(name__icontains=search))
    # 计算搜索之后的总数
    total = p_list.count()
    rows = []
    p_list = p_list.order_by("-id")
    # 分页
    paginator = Paginator(p_list, page_size)
    try:
        p_list = paginator.page(page_number)  # 获取当前页码的记录
    except PageNotAnInteger:
        p_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        p_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    for prg in p_list:
        rows.append(model_to_dict(prg))
    result = {
        "total": total,
        "rows": rows
    }
    return HttpResponse(json.dumps(result, default=default), content_type="application_json")


@csrf_exempt
def inst_prog_list(request):
    get = request.GET
    search = get.get("searchText")
    page_size = get.get("pageSize")
    page_number = get.get("pageNumber", 1)
    type_layer = get.get("type_layer")
    p_list = DefnProg.objects.filter(Q(type_layer=1) | Q(type_layer=type_layer))
    if search is not None:
        p_list = p_list.filter(Q(id__icontains=search) | Q(name__icontains=search))
    # 计算搜索之后的总数
    total = p_list.count()
    rows = []
    p_list = p_list.order_by("-id")
    # 分页
    paginator = Paginator(p_list, page_size)
    try:
        p_list = paginator.page(page_number)  # 获取当前页码的记录
    except PageNotAnInteger:
        p_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        p_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    for prg in p_list:
        rows.append(model_to_dict(prg))
    result = {
        "total": total,
        "rows": rows
    }
    return HttpResponse(json.dumps(result, default=default), content_type="application_json")


@csrf_exempt
def prog_edit(request):
    try:
        cursor = connection.cursor()
        id = request.POST.get('id')
        name = request.POST.get('name')
        val = request.POST.get('value')
        if id is not None:
            prog = DefnProg.objects.get(id=id)
            # 设置Field值
            prog.__setattr__(name, val)
            prog.save(update_fields =[name])
        else:
            _prog = DefnProg.objects.filter(id__isnull=False).latest('id')
            if _prog is not None:
                _id = _prog.id + 1
            else:
                _id = 1
            cursor.execute("insert into defn_prog(id, type_layer) values (%s, %s)", [_id, val])
        flag = True
    except:
        print(traceback.format_exc())
        flag = False
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def prog_del(request):
    try:
        id = request.POST.get('id')
        DefnProg.objects.extra(where=['id IN (' + id + ')']).delete()
        # 删除对应的明细
        DefnProgDtl.objects.extra(where=['id_prog IN (' + id + ')']).delete()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def prog_copy(request):
    try:
        id = request.POST.get('id')
        prog_list = DefnProg.objects.extra(where=['id IN (' + id + ')']).all()
        for prog in prog_list:
            prog_dtl_list = DefnProgDtl.objects.filter(id_prog=prog.id)
            prog.id = None
            prog.save()
            _prog = DefnProg.objects.latest('id')
            for prog_dtl in prog_dtl_list:
                prog_dtl.id = None
                prog_dtl.id_prog = _prog.id
                prog_dtl.save()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def prog_dtl_list(request):
    get = request.GET
    search = get.get("searchText")
    page_size = get.get("pageSize")
    page_number = get.get("pageNumber", 1)
    id_prog = get.get("id_prog")
    rows = []
    total=0
    try:
        p_list = DefnProgDtl.objects.filter(Q(id_prog=id_prog))
        # 搜索
        if search is not None:
            p_list = p_list.filter(Q(id__icontains=search))
        # 计算搜索之后的总数
        total = p_list.count()
        p_list = p_list.order_by("sn", "-id")
        # 分页s
        paginator = Paginator(p_list, page_size)
        try:
            p_list = paginator.page(page_number)  # 获取当前页码的记录
        except PageNotAnInteger:
            p_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
        except EmptyPage:
            p_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

        for prg in p_list:
            rows.append(model_to_dict(prg))
    except:
        print()
    result = {
        "total": total,
        "rows": rows
    }
    return HttpResponse(json.dumps(result, default=default), content_type="application_json")


@csrf_exempt
def prog_dtl_edit(request):
    try:
        cursor = connection.cursor()
        id = request.POST.get('id')
        name = request.POST.get('name')
        val = request.POST.get('value')
        if id is not None:
            prog_dtl = DefnProgDtl.objects.get(id=id)
            # 设置Field值
            prog_dtl.__setattr__(name, val)
            prog_dtl.save(update_fields =[name])
        else:
            if DefnProgDtl.objects.count() == 0:
                _id = 1
            else:
                _m = DefnProgDtl.objects.latest('id')
                if _m is not None:
                    _id = _m.id + 1
                else:
                    _id = 1
            try:
                _prog_dtl = DefnProgDtl.objects.filter(Q(id_prog=val)).latest('sn')
                if _prog_dtl is not None:
                    sn = _prog_dtl.sn + 1
            except:
                sn = 1
            cursor.execute("insert into defn_prog_dtl(id,id_prog,sn) values (%s,%s,%s)", [_id, val, sn])
        flag = True
    except:
        print(traceback.format_exc())
        flag = False
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def prog_dtl_del(request):
    try:
        id = request.POST.get('id')
        DefnProgDtl.objects.extra(where=['id IN (' + id + ')']).delete()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def prog_dtl_copy(request):
    try:
        id = request.POST.get('id')
        prog_dtl_list = DefnProgDtl.objects.extra(where=['id IN (' + id + ')']).all()
        for prog_dtl in prog_dtl_list:
            prog_dtl.id = None
            prog_dtl.save()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def inst_list(request):
    get = request.GET
    search = get.get("searchText")
    page_size = get.get("pageSize")
    page_number = get.get("pageNumber", 1)
    type_layer = get.get("type_layer")
    list = DefnInst.objects.filter(type_layer=type_layer)
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
    aide_list = DefnAide.objects.all()
    error_list = DefnError.objects.all()
    prog_list = DefnProg.objects.all()
    for m in list:
        dic = model_to_dict(m)
        # 添加id_prog_name
        if m.id_prog is not None:
            prog_list = prog_list.filter(id=m.id_prog)
            if prog_list.count() > 0:
                dic['id_prog_name'] = prog_list.__getitem__(0).name
            else:
                dic['id_prog_name'] = m.id_prog
        # 添加id_list_name
        if m.id_list is not None:
            _aide_list = aide_list.filter(id=m.id_list)
            if _aide_list.count() > 0:
                dic['id_list_name'] = _aide_list.__getitem__(0).name
            else:
                dic['id_list_name'] = m.id_list
        #  添加array_record_name
        if m.array_record is not None and len(m.array_record) > 0:
            records = m.array_record.split(",")
            _records = []
            for i in range(len(records)):
                record = records[i]
                _aide_list = aide_list.filter(id=record)
                if _aide_list.count() > 0:
                    _records.append(_aide_list.__getitem__(0).name)
                else:
                    _records.append(record)
            dic['array_record_name'] = ",".join(_records)
        # 添加array_absolve_name
        if m.array_absolve is not None and len(m.array_absolve) > 0:
            absolves = m.array_absolve.split(",")
            _absolves = []
            for i in range(len(absolves)):
                absolve = absolves[i]
                _error_list = error_list.filter(code=absolve)
                if _error_list.count() > 0:
                    _absolves.append(_error_list.__getitem__(0).name)
                else:
                    _absolves.append(absolve)
            dic['array_absolve_name'] = ",".join(_absolves)
        # 添加array_dispose_name
        if m.array_dispose is not None and len(m.array_dispose) > 0:
            disposes = m.array_dispose.split(",")
            _disposes = []
            for i in range(len(disposes)):
                dispose = disposes[i]
                _error_list = error_list.filter(code=dispose)
                if _error_list.count() > 0:
                    _disposes.append(_error_list.__getitem__(0).name)
                else:
                    _disposes.append(dispose)
            dic['array_dispose_name'] = ",".join(_disposes)
        #  array_dinst_name
        if m.array_dinst is not None and len(m.array_dinst) > 0:
            array_dinst = m .array_dinst
            try:
                index = array_dinst.index(".")
            except ValueError:
                index = -1
            child_arr = []
            parent_arr = []
            if index >= 0:
                child = array_dinst[0:index]
                parent = array_dinst[index+1:]
                child_arr = child.split(",") if len(child) > 0 else []
                parent_arr = parent.split(".") if len(parent) > 0 else []
            else:
                child_arr = array_dinst.split(",")
            for i in range(len(child_arr)):
                child = child_arr[i]
                _aide_list = aide_list.filter(id=child)
                if _aide_list.count() > 0:
                    child_arr[i] = _aide_list.__getitem__(0).name
            if len(parent_arr) > 0:
                for i in range(len(parent_arr)):
                    parent = parent_arr[i]
                    _aide_list = aide_list.filter(id=parent)
                    if _aide_list.count() > 0:
                        parent_arr[i] = _aide_list.__getitem__(0).name
                array_dinst_name = ".".join([",".join(child_arr), ".".join(parent_arr)])
            else:
                array_dinst_name = ",".join(child_arr)
            dic['array_dinst_name'] = array_dinst_name
        rows.append(dic)
    result = {
        "total": total,
        "rows": rows
    }
    return HttpResponse(json.dumps(result, default=default), content_type="application_json")


@csrf_exempt
def proc_inst_list(request):
    get = request.GET
    search = get.get("searchText")
    page_size = get.get("pageSize")
    page_number = get.get("pageNumber", 1)
    type_layer = get.get("type_layer")
    list = DefnInst.objects.filter(Q(type_layer=1) | Q(type_layer=type_layer))
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
        rows.append(model_to_dict(m))
    result = {
        "total": total,
        "rows": rows
    }
    return HttpResponse(json.dumps(result, default=default), content_type="application_json")


@csrf_exempt
def inst_edit(request):
    try:
        cursor = connection.cursor()
        id = request.POST.get('id')
        if id is not None:
            m = DefnInst.objects.get(id=id)
            names = request.POST.get('name')
            vals = request.POST.get('value')
            name_arr = names.split(";")
            val_arr = vals.split(";")
            # 设置Field值
            for i in range(len(name_arr)):
                name = name_arr[i]
                _val = val_arr[i]
                # 设置Field值
                if name == 'id_list' and _val == '':
                    m.__setattr__(name, None)
                else:
                    m.__setattr__(name, _val)
            m.save(update_fields=name_arr)
        else:
            val = request.POST.get('value')
            if DefnInst.objects.count() == 0:
                _id = 1
            else:
                _m = DefnInst.objects.latest('id')
                if _m is not None:
                    _id = _m.id + 1
                else:
                    _id = 1
            cursor.execute("insert into defn_inst(id, type_layer) values (%s, %s)", [_id, val])
        flag = True
    except:
        print(traceback.format_exc())
        flag = False
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def inst_del(request):
    try:
        id = request.POST.get('id')
        DefnInst.objects.extra(where=['id IN (' + id + ')']).delete()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def inst_copy(request):
    try:
        id = request.POST.get('id')
        list = DefnInst.objects.extra(where=['id IN (' + id + ')']).all()
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
def aide_list(request):
    get = request.GET
    search = get.get("searchText")
    page_size = get.get("pageSize")
    page_number = get.get("pageNumber", 1)
    type = get.get("type")
    type_sub = get.get("type_sub")
    list = DefnAide.objects.filter(Q(type=type), Q(type_sub=type_sub))
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
        rows.append(model_to_dict(m))
    result = {
        "total": total,
        "rows": rows
    }
    return HttpResponse(json.dumps(result, default=default), content_type="application_json")


@csrf_exempt
def aide_edit(request):
    try:
        cursor = connection.cursor()
        post = request.POST
        id = post.get('id')
        name = post.get('name')
        val = post.get('value')
        type = post.get("type")
        type_sub = post.get("type_sub")
        if id is not None:
            m = DefnAide.objects.get(id=id)
            # 设置Field值
            m.__setattr__(name, val)
            m.save(update_fields=[name])
        else:
            if DefnAide.objects.count() == 0:
                _id = 1
            else:
                _m = DefnAide.objects.latest('id')
                if _m is not None:
                    _id = _m.id + 1
                else:
                    _id = 1
            cursor.execute("insert into defn_aide(id,type,type_sub) values (%s,%s,%s)", [_id, type, type_sub])
        flag = True
    except:
        print(traceback.format_exc())
        flag = False
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def aide_del(request):
    try:
        id = request.POST.get('id')
        DefnAide.objects.extra(where=['id IN (' + id + ')']).delete()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def aide_copy(request):
    try:
        id = request.POST.get('id')
        list = DefnAide.objects.extra(where=['id IN (' + id + ')']).all()
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
    rows = []
    try:
        list = DefnError.objects.filter(bl_active='y')
        for m in list:
            rows.append(model_to_dict(m))
    except:
        print(traceback.format_exc())
    return HttpResponse(json.dumps(rows, default=default), content_type="application_json")


@csrf_exempt
def proc_list(request):
    get = request.GET
    search = get.get("searchText")
    page_size = get.get("pageSize")
    page_number = get.get("pageNumber", 1)
    type_layer = get.get("type_layer")
    list = DefnProc.objects.filter(type_layer=type_layer)
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
    aide_list = DefnAide.objects.all()
    for m in list:
        dic = model_to_dict(m)
        # 添加id_list_name
        if m.id_list is not None:
            _aide_list = aide_list.filter(id=m.id_list)
            if _aide_list.count() > 0:
                dic['id_list_name'] = _aide_list.__getitem__(0).name
            else:
                dic['id_list_name'] = m.id_list

        # 添加id_judge_name
        if m.id_judge is not None:
            _aide_list = aide_list.filter(id=m.id_judge)
            if _aide_list.count() > 0:
                dic['id_judge_name'] = _aide_list.__getitem__(0).name
            else:
                dic['id_judge_name'] = m.id_list
        #  添加array_record_name
        if m.array_record is not None and len(m.array_record) > 0:
            records = m.array_record.split(",")
            _records = []
            for i in range(len(records)):
                record = records[i]
                _aide_list = aide_list.filter(id=record)
                if _aide_list.count() > 0:
                    _records.append(_aide_list.__getitem__(0).name)
                else:
                    _records.append(record)
            dic['array_record_name'] = ",".join(_records)
        # 添加array_exec_name
        if m.array_exec is not None and len(m.array_exec) > 0:
            _array_exec = m.array_exec
            try:
                _if = _array_exec.split("t")[0]
            except ValueError:
                _if = ''
            try:
                _then = _array_exec.split("t")[1].split("e")[0]
            except ValueError:
                _then = ''
            try:
                _else = _array_exec.split("t")[1].split("e")[1]
            except ValueError:
                _else = ''
            if_arr = _if.split(",") if len(_if) > 0 else []
            then_arr = _then.split(",") if len(_then) > 0 else []
            else_arr = _else.split(",") if len(_else) > 0 else []
            changeArr(if_arr)
            changeArr(then_arr)
            changeArr(else_arr)
            dic['array_exec_name'] = "e_else".join(["t_then".join([",".join(if_arr), ",".join(then_arr)]), ",".join(else_arr)])
        rows.append(dic)
    result = {
        "total": total,
        "rows": rows
    }
    return HttpResponse(json.dumps(result, default=default), content_type="application_json")


def changeArr(arr):
    for i in range(len(arr)):
        val = arr[i]
        # 判断是否是s开头
        if val.startswith('s'):
            _row = DefnProc.objects.filter(id=val[1:])
        else:
            _row = DefnInst.objects.filter(id=val)
        if _row.count() > 0:
            arr[i] = _row.__getitem__(0).name


@csrf_exempt
def proc_proc_list(request):
    get = request.GET
    search = get.get("searchText")
    page_size = get.get("pageSize")
    page_number = get.get("pageNumber", 1)
    type_layer = get.get("type_layer")
    list = DefnProc.objects.filter(Q(type_layer=1) | Q(type_layer=type_layer))
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
        rows.append(model_to_dict(m))
    result = {
        "total": total,
        "rows": rows
    }
    return HttpResponse(json.dumps(result, default=default), content_type="application_json")


@csrf_exempt
def schd_proc_list(request):
    get = request.GET
    search = get.get("searchText")
    page_size = get.get("pageSize")
    page_number = get.get("pageNumber", 1)
    type_layer = get.get("type_layer")
    list = DefnProc.objects.filter(Q(type_layer=1) | Q(type_layer=type_layer))
    list = list.filter(bl_shell='y')
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
        rows.append(model_to_dict(m))
    result = {
        "total": total,
        "rows": rows
    }
    return HttpResponse(json.dumps(result, default=default), content_type="application_json")


@csrf_exempt
def proc_edit(request):
    try:
        cursor = connection.cursor()
        id = request.POST.get('id')
        if id is not None:
            m = DefnProc.objects.get(id=id)
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
            if DefnProc.objects.count() == 0:
                _id = 1
            else:
                _m = DefnProc.objects.latest('id')
                if _m is not None:
                    _id = _m.id + 1
                else:
                    _id = 1
            cursor.execute("insert into defn_proc(id, type_layer) values (%s, %s)", [_id, val])
        flag = True
    except:
        print(traceback.format_exc())
        flag = False
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def proc_del(request):
    try:
        id = request.POST.get('id')
        DefnProc.objects.extra(where=['id IN (' + id + ')']).delete()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def proc_copy(request):
    try:
        id = request.POST.get('id')
        list = DefnProc.objects.extra(where=['id IN (' + id + ')']).all()
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
def schd_list(request):
    get = request.GET
    search = get.get("searchText")
    page_size = get.get("pageSize")
    page_number = get.get("pageNumber", 1)
    type_layer = get.get("type_layer")
    list = DefnSchd.objects.filter(type_layer=type_layer)
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
    proc_list = DefnProc.objects.all()
    for m in list:
        dic = model_to_dict(m)
        # 添加id_list_name
        if m.id_proc is not None:
            _proc_list = proc_list.filter(id=m.id_proc)
            if _proc_list.count() > 0:
                dic['id_proc_name'] = _proc_list.__getitem__(0).name
            else:
                dic['id_proc_name'] = m.id_proc
        rows.append(dic)
    result = {
        "total": total,
        "rows": rows
    }
    return HttpResponse(json.dumps(result, default=default), content_type="application_json")


@csrf_exempt
def schd_edit(request):
    try:
        cursor = connection.cursor()
        id = request.POST.get('id')
        if id is not None:
            m = DefnSchd.objects.get(id=id)
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
            if DefnSchd.objects.count() == 0:
                _id = 1
            else:
                _m = DefnSchd.objects.latest('id')
                if _m is not None:
                    _id = _m.id + 1
                else:
                    _id = 1
            cursor.execute("insert into defn_schd(id, type_layer) values (%s, %s)", [_id, val])
        flag = True
    except:
        print(traceback.format_exc())
        flag = False
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def schd_del(request):
    try:
        id = request.POST.get('id')
        DefnSchd.objects.extra(where=['id IN (' + id + ')']).delete()
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")


@csrf_exempt
def schd_copy(request):
    try:
        id = request.POST.get('id')
        list = DefnSchd.objects.extra(where=['id IN (' + id + ')']).all()
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
def schd_run(request):
    try:
        id = request.POST.get('id')
        run_schd(id)
        flag = True
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }, default=default), content_type="application_json")