"""sc_new URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from sc_new.view import views, action, base, data, monitor

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^get_table_define/', views.get_table_define, name="get_table_define"),

    # action
    url(r'^action/prog_dtl/', action.prog_dtl, name="prog_dtl"),
    url(r'^action/inst_prog_aide/', action.inst_prog_aide, name="inst_prog_aide"),
    url(r'^action/proc_inst_aide/', action.proc_inst_aide, name="proc_inst_aide"),
    url(r'^action/schd_proc_aide/', action.schd_proc_aide, name="schd_proc_aide"),

    url(r'^action/get_type_layers/', action.get_type_layers, name="get_type_layers"),

    url(r'^action/prog_list/', action.prog_list, name="prog_list"),
    # prog列表页，供程序-实例页面使用
    url(r'^action/inst_prog_list/', action.inst_prog_list, name="inst_prog_list"),
    url(r'^action/prog_edit/', action.prog_edit, name="prog_edit"),
    url(r'^action/prog_del/', action.prog_del, name="prog_del"),
    url(r'^action/prog_copy/', action.prog_copy, name="prog_copy"),

    url(r'^action/prog_dtl_list/', action.prog_dtl_list, name="prog_dtl_list"),
    url(r'^action/prog_dtl_edit/', action.prog_dtl_edit, name="prog_dtl_edit"),
    url(r'^action/prog_dtl_del/', action.prog_dtl_del, name="prog_dtl_del"),
    url(r'^action/prog_dtl_copy/', action.prog_dtl_copy, name="prog_dtl_copy"),

    url(r'^action/inst_list/', action.inst_list, name="inst_list"),
    # inst列表页，供程序-流程页面使用
    url(r'^action/proc_inst_list/', action.proc_inst_list, name="proc_inst_list"),
    url(r'^action/inst_edit/', action.inst_edit, name="inst_edit"),
    url(r'^action/inst_del/', action.inst_del, name="inst_del"),
    url(r'^action/inst_copy/', action.inst_copy, name="inst_copy"),

    url(r'^action/aide_list/', action.aide_list, name="aide_list"),
    url(r'^action/aide_edit/', action.aide_edit, name="aide_edit"),
    url(r'^action/aide_del/', action.aide_del, name="aide_del"),
    url(r'^action/aide_copy/', action.aide_copy, name="aide_copy"),

    url(r'^action/error_list/', action.error_list, name="error_list"),

    url(r'^action/proc_list/', action.proc_list, name="proc_list"),
    # proc列表页，供程序-流程页面使用
    url(r'^action/proc_proc_list/', action.proc_proc_list, name="proc_proc_list"),
    # proc列表页，供程序-计划页面使用
    url(r'^action/schd_proc_list/', action.schd_proc_list, name="schd_proc_list"),
    url(r'^action/proc_edit/', action.proc_edit, name="proc_edit"),
    url(r'^action/proc_del/', action.proc_del, name="proc_del"),
    url(r'^action/proc_copy/', action.proc_copy, name="proc_copy"),

    url(r'^action/schd_list/', action.schd_list, name="schd_list"),
    url(r'^action/schd_edit/', action.schd_edit, name="schd_edit"),
    url(r'^action/schd_del/', action.schd_del, name="schd_del"),
    url(r'^action/schd_copy/', action.schd_copy, name="schd_copy"),
    url(r'^action/schd_run/', action.schd_run, name="schd_run"),


    # base
    url(r'^base/table_view/', base.table_view, name="table_view"),
    url(r'^base/dtype_type_error/', base.dtype_type_error, name="dtype_type_error"),

    url(r'^base/table_list/', base.table_list, name="table_list"),
    url(r'^base/table_edit/', base.table_edit, name="table_edit"),
    url(r'^base/table_del/', base.table_del, name="table_del"),
    url(r'^base/table_copy/', base.table_copy, name="table_copy"),
    url(r'^base/table_create/', base.table_create, name="table_create"),

    url(r'^base/table_dtl_list/', base.table_dtl_list, name="table_dtl_list"),
    url(r'^base/table_dtl_edit/', base.table_dtl_edit, name="table_dtl_edit"),
    url(r'^base/table_dtl_del/', base.table_dtl_del, name="table_dtl_del"),
    url(r'^base/table_dtl_copy/', base.table_dtl_copy, name="table_dtl_copy"),

    url(r'^base/view_list/', base.view_list, name="view_list"),
    url(r'^base/view_edit/', base.view_edit, name="view_edit"),
    url(r'^base/view_del/', base.view_del, name="view_del"),
    url(r'^base/view_copy/', base.view_copy, name="view_copy"),
    url(r'^base/view_create/', base.view_create, name="view_create"),
    url(r'^base/view_query/', base.view_query, name="view_query"),
    url(r'^base/view_excel_export/', base.view_excel_export, name="view_excel_export"),

    url(r'^base/d_type_list/', base.d_type_list, name="d_type_list"),
    url(r'^base/d_type_edit/', base.d_type_edit, name="d_type_edit"),
    url(r'^base/d_type_del/', base.d_type_del, name="d_type_del"),
    url(r'^base/d_type_copy/', base.d_type_copy, name="d_type_copy"),

    url(r'^base/type_list/', base.type_list, name="type_list"),
    url(r'^base/type_edit/', base.type_edit, name="type_edit"),
    url(r'^base/type_del/', base.type_del, name="type_del"),
    url(r'^base/type_copy/', base.type_copy, name="type_copy"),

    url(r'^base/error_list/', base.error_list, name="error_list"),
    url(r'^base/error_edit/', base.error_edit, name="error_edit"),
    url(r'^base/error_del/', base.error_del, name="error_del"),
    url(r'^base/error_copy/', base.error_copy, name="error_copy"),


    # data
    url(r'^data/ds_dtl/', data.ds_dtl, name="ds_dtl"),
    url(r'^data/dm/', data.dm, name="dm"),
    url(r'^data/dr/', data.dr, name="dr"),

    url(r'^data/get_types/', data.get_types, name="get_types"),

    url(r'^data/ds_list/', data.ds_list, name="ds_list"),
    url(r'^data/ds_edit/', data.ds_edit, name="ds_edit"),
    url(r'^data/ds_del/', data.ds_del, name="ds_del"),
    url(r'^data/ds_copy/', data.ds_copy, name="ds_copy"),

    url(r'^data/ds_dtl_list/', data.ds_dtl_list, name="ds_dtl_list"),
    url(r'^data/ds_dtl_edit/', data.ds_dtl_edit, name="ds_dtl_edit"),
    url(r'^data/ds_dtl_del/', data.ds_dtl_del, name="ds_dtl_del"),
    url(r'^data/ds_dtl_copy/', data.ds_dtl_copy, name="ds_dtl_copy"),

    url(r'^data/dm_list/', data.dm_list, name="dm_list"),
    url(r'^data/dm_edit/', data.dm_edit, name="dm_edit"),
    url(r'^data/dm_del/', data.dm_del, name="dm_del"),
    url(r'^data/dm_copy/', data.dm_copy, name="dm_copy"),
    url(r'^data/dm_query/', data.dm_query, name="dm_query"),
    url(r'^data/dm_excel_export/', data.dm_excel_export, name="dm_excel_export"),

    url(r'^data/dr_list/', data.dr_list, name="dr_list"),
    url(r'^data/dr_edit/', data.dr_edit, name="dr_edit"),
    url(r'^data/dr_del/', data.dr_del, name="dr_del"),
    url(r'^data/dr_copy/', data.dr_copy, name="dr_copy"),
    url(r'^data/dr_query/', data.dr_query, name="dr_query"),
    url(r'^data/dr_excel_export/', data.dr_excel_export, name="dr_excel_export"),


    # monitor
    url(r'^monitor/log/', monitor.log, name="log"),

    url(r'^monitor/log_debug_list/', monitor.log_debug_list, name="log_debug_list"),
    url(r'^monitor/log_timer_list/', monitor.log_timer_list, name="log_timer_list"),
    url(r'^monitor/log_error_list/', monitor.log_error_list, name="log_error_list"),

    url(r'^monitor/log_debug_truncate/', monitor.log_debug_truncate, name="log_debug_truncate"),
    url(r'^monitor/log_timer_truncate/', monitor.log_timer_truncate, name="log_timer_truncate"),
    url(r'^monitor/log_error_truncate/', monitor.log_error_truncate, name="log_error_truncate"),
]
