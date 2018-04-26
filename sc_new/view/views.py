import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import HttpResponse
from django.forms import model_to_dict
from sc_new.models import DirctTableDtl


def index(request):
    return render(request, 'index.html', {})


@csrf_exempt
def get_table_define(request):
    code_table = request.POST.get("codeTable")
    t_list = DirctTableDtl.objects.filter(Q(code_table=code_table), Q(bl_visible='y'))
    # 按序号排序
    t_list = t_list.order_by("sn")
    rows = []
    for prg in t_list:
        rows.append(model_to_dict(prg))
    return HttpResponse(json.dumps(rows), content_type="application_json")