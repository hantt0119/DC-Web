import json
import traceback

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from sc_new.models import MonitorLogDebug, MonitorLogError, MonitorLogTimer
from django.db.models import Q
from django.db import connection
from django.forms import model_to_dict
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from sc_new.util import default


def log(request):
    return render(request, './monitor/log.html', {})


@csrf_exempt
def log_debug_list(request):
    get = request.GET
    search = get.get("searchText")
    page_size = get.get("pageSize")
    page_number = get.get("pageNumber", 1)
    sort_order = get.get("sortOrder", 'asc')
    list = MonitorLogDebug.objects.all()
    if search is not None:
        list = list.filter(Q(name_proc__icontains=search) | Q(name_prog__icontains=search))
    # 计算搜索之后的总数
    total = list.count()
    rows = []
    if sort_order == 'asc':
        list = list.order_by("id")
    else:
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
def log_timer_list(request):
    get = request.GET
    search = get.get("searchText")
    page_size = get.get("pageSize")
    page_number = get.get("pageNumber", 1)
    sort_order = get.get("sortOrder", 'asc')
    list = MonitorLogTimer.objects.all()
    if search is not None:
        list = list.filter(Q(name_exec__icontains=search) | Q(name_lvl__icontains=search))
    # 计算搜索之后的总数
    total = list.count()
    rows = []
    if sort_order == 'asc':
        list = list.order_by("id")
    else:
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
def log_error_list(request):
    get = request.GET
    search = get.get("searchText")
    page_size = get.get("pageSize")
    page_number = get.get("pageNumber", 1)
    sort_order = get.get("sortOrder", 'asc')
    list = MonitorLogError.objects.all()
    if search is not None:
        list = list.filter(Q(name_proc__icontains=search) | Q(name_prog__icontains=search))
    # 计算搜索之后的总数
    total = list.count()
    rows = []
    if sort_order == 'asc':
        list = list.order_by("id")
    else:
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
def log_debug_truncate(request):
    try:
        cursor = connection.cursor()
        cursor.execute('truncate log_debug')
        flag = 1
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }), content_type="application_json")


@csrf_exempt
def log_timer_truncate(request):
    try:
        cursor = connection.cursor()
        cursor.execute('truncate log_timer')
        flag = 1
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }), content_type="application_json")


@csrf_exempt
def log_error_truncate(request):
    try:
        cursor = connection.cursor()
        cursor.execute('truncate log_error')
        flag = 1
    except:
        flag = False
        print(traceback.format_exc())
    return HttpResponse(json.dumps({
        'flag': flag
    }), content_type="application_json")