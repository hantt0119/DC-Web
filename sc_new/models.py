from django.db import models


# 表定义-视图
class DirctTableDtl(models.Model):
    class Meta:
        db_table = 'dirct_table_dtl'
    id = models.IntegerField(primary_key=True)
    id_table = models.IntegerField(blank=False)
    code_table = models.CharField(max_length=255)
    code_column = models.CharField(max_length=255)
    name_column = models.CharField(max_length=255)
    sn = models.IntegerField(blank=False)
    bl_visible = models.CharField(max_length=1)
    num_width = models.IntegerField()


# defn_type
class DefnType(models.Model):
    class Meta:
        db_table = 'defn_type'
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    dscp = models.CharField(max_length=100)
    id_table = models.IntegerField(blank=False)
    id_column = models.IntegerField(blank=False)
    bl_active = models.CharField(max_length=1)
    u_cr = models.CharField(max_length=30, blank=False)
    u_md = models.CharField(max_length=30, blank=False)
    d_cr = models.DateTimeField(blank=False)
    d_md = models.DateTimeField(blank=False)
    cmnt = models.CharField(max_length=300, blank=False)


# defn_prog
class DefnProg(models.Model):
    class Meta:
        db_table = 'defn_prog'
    name = models.CharField(max_length=255, blank=False)
    type_layer = models.CharField(max_length=255, blank=False)
    bl_lock = models.CharField(max_length=1, blank=False)
    bl_active = models.CharField(max_length=1, blank=False)
    u_cr = models.CharField(max_length=255, blank=False)
    u_md = models.CharField(max_length=255, blank=False)
    d_cr = models.DateTimeField(blank=False)
    d_md = models.DateTimeField(blank=False)
    cmnt = models.CharField(max_length=255, blank=False)


# defn_prog_dtl
class DefnProgDtl(models.Model):
    class Meta:
        db_table = 'defn_prog_dtl'
    id_prog = models.IntegerField(blank=False)
    sn = models.IntegerField(blank=True)
    dscp = models.CharField(max_length=4000, blank=True)
    logic = models.CharField(max_length=4000, blank=True)
    array_dvar = models.CharField(max_length=4000, blank=True)
    array_ivar = models.CharField(max_length=4000, blank=True)
    logic_list = models.CharField(max_length=4000, blank=True)
    array_lvar = models.CharField(max_length=4000, blank=True)
    array_dval = models.CharField(max_length=4000, blank=True)
    array_lval = models.CharField(max_length=4000, blank=True)
    num_cut = models.IntegerField(blank=True)
    bl_lock = models.CharField(max_length=1, blank=True)
    bl_active = models.CharField(max_length=1, blank=True)
    u_cr = models.CharField(max_length=255, blank=True)
    d_cr = models.DateTimeField(blank=True)
    u_md = models.CharField(max_length=255, blank=True)
    d_md = models.DateTimeField(blank=True)
    cmnt = models.CharField(max_length=4000, blank=True)


# defn_inst
class DefnInst(models.Model):
    class Meta:
        db_table = 'defn_inst'
    name = models.CharField(max_length=30, blank=False)
    type = models.CharField(max_length=10, blank=False)
    type_layer = models.CharField(max_length=10, blank=False)
    id_prog = models.IntegerField()
    array_record = models.CharField(max_length=100, blank=False)
    id_list = models.IntegerField()
    array_absolve = models.CharField(max_length=100, blank=False)
    array_dispose = models.CharField(max_length=100, blank=False)
    array_dinst = models.CharField(max_length=100, blank=False)
    array_sn_dinst = models.CharField(max_length=100, blank=False)
    array_val = models.CharField(max_length=100, blank=False)
    bl_lock = models.CharField(max_length=1, blank=False)
    bl_active = models.CharField(max_length=1, blank=False)
    u_cr = models.CharField(max_length=30, blank=False)
    u_md = models.CharField(max_length=30, blank=False)
    d_cr = models.DateTimeField(blank=False)
    d_md = models.DateTimeField(blank=False)
    cmnt = models.CharField(max_length=300, blank=False)


# defn_aide
class DefnAide(models.Model):
    class Meta:
        db_table = 'defn_aide'
    name = models.CharField(max_length=30, blank=False)
    dscp = models.CharField(max_length=100, blank=False)
    type = models.CharField(max_length=10, blank=False)
    type_sub = models.CharField(max_length=10, blank=False)
    logic = models.CharField(max_length=4000, blank=False)
    array_var = models.CharField(max_length=100, blank=False)
    bl_lock = models.CharField(max_length=1, blank=False)
    bl_active = models.CharField(max_length=1, blank=False)
    u_cr = models.CharField(max_length=30, blank=False)
    u_md = models.CharField(max_length=30, blank=False)
    d_cr = models.DateTimeField(blank=False)
    d_md = models.DateTimeField(blank=False)
    cmnt = models.CharField(max_length=300, blank=False)


# defn_error
class DefnError(models.Model):
    class Meta:
        db_table = 'defn_error'
    code = models.CharField(max_length=30, blank=False)
    name = models.CharField(max_length=30, blank=False)
    dscp = models.CharField(max_length=100, blank=False)
    bl_active = models.CharField(max_length=1, blank=False)
    u_cr = models.CharField(max_length=30, blank=False)
    u_md = models.CharField(max_length=30, blank=False)
    d_cr = models.DateTimeField(blank=False)
    d_md = models.DateTimeField(blank=False)
    cmnt = models.CharField(max_length=300, blank=False)


# defn_proc
class DefnProc(models.Model):
    class Meta:
        db_table = 'defn_proc'
    name = models.CharField(max_length=30, blank=False)
    dscp = models.CharField(max_length=100, blank=False)
    type_layer = models.CharField(max_length=10, blank=False)
    array_exec = models.CharField(max_length=100, blank=False)
    array_sn_exec = models.CharField(max_length=100, blank=False)
    array_record = models.CharField(max_length=100, blank=False)
    id_judge = models.IntegerField()
    id_list = models.IntegerField()
    bl_shell = models.CharField(max_length=1, blank=False)
    bl_lock = models.CharField(max_length=1, blank=False)
    bl_active = models.CharField(max_length=1, blank=False)
    u_cr = models.CharField(max_length=30, blank=False)
    u_md = models.CharField(max_length=30, blank=False)
    d_cr = models.DateTimeField(blank=False)
    d_md = models.DateTimeField(blank=False)
    cmnt = models.CharField(max_length=300, blank=False)


# defn_schd
class DefnSchd(models.Model):
    class Meta:
        db_table = 'defn_schd'
    name = models.CharField(max_length=30, blank=False)
    dscp = models.CharField(max_length=100, blank=False)
    type_layer = models.CharField(max_length=10, blank=False)
    code_object = models.CharField(max_length=30, blank=False)
    id_proc = models.IntegerField()
    t_launch = models.CharField(max_length=6, blank=False)
    t_recover = models.CharField(max_length=6, blank=False)
    t_offset = models.DecimalField(blank=False, max_digits=8, decimal_places=0)
    t_interval = models.DecimalField(blank=False, max_digits=8, decimal_places=0)
    num_times = models.IntegerField()
    lvl_timer = models.IntegerField()
    bl_success = models.CharField(max_length=1, blank=False)
    bl_debug = models.CharField(max_length=1, blank=False)
    bl_exec = models.CharField(max_length=1, blank=False)
    bl_lock = models.CharField(max_length=1, blank=False)
    bl_active = models.CharField(max_length=1, blank=False)
    u_cr = models.CharField(max_length=30, blank=False)
    u_md = models.CharField(max_length=30, blank=False)
    d_cr = models.DateTimeField(blank=False)
    d_md = models.DateTimeField(blank=False)
    cmnt = models.CharField(max_length=300, blank=False)


# defn_table
class DefnTable(models.Model):
    class Meta:
        db_table = 'defn_table'
    code = models.CharField(max_length=30, blank=False)
    code_user = models.CharField(max_length=30, blank=False)
    code_new = models.CharField(max_length=30, blank=False)
    code_nuser = models.CharField(max_length=30, blank=False)
    logic = models.CharField(max_length=4000, blank=False)
    bl_init = models.CharField(max_length=1, blank=False)
    bl_active = models.CharField(max_length=1, blank=False)
    u_cr = models.CharField(max_length=30, blank=False)
    u_md = models.CharField(max_length=30, blank=False)
    d_cr = models.DateTimeField(blank=False)
    d_md = models.DateTimeField(blank=False)
    cmnt = models.CharField(max_length=300, blank=False)


# defn_table_dtl
class DefnTableDtl(models.Model):
    class Meta:
        db_table = 'defn_table_dtl'
    id_table = models.IntegerField()
    code = models.CharField(max_length=30, blank=False)
    code_new = models.CharField(max_length=30, blank=False)
    name = models.CharField(max_length=30, blank=False)
    dscp = models.CharField(max_length=100, blank=False)
    sn = models.IntegerField()
    str_dtype = models.CharField(max_length=100, blank=False)
    str_default = models.CharField(max_length=100, blank=False)
    bl_null = models.CharField(max_length=1, blank=False)
    bl_visible = models.CharField(max_length=1, blank=False)
    bl_active = models.CharField(max_length=1, blank=False)
    u_cr = models.CharField(max_length=30, blank=False)
    u_md = models.CharField(max_length=30, blank=False)
    d_cr = models.DateTimeField(blank=False)
    d_md = models.DateTimeField(blank=False)
    cmnt = models.CharField(max_length=300, blank=False)
    num_width = models.IntegerField()


# defn_view
class DefnView(models.Model):
    class Meta:
        db_table = 'defn_view'
    code = models.CharField(max_length=30, blank=False)
    code_user = models.CharField(max_length=30, blank=False)
    code_new = models.CharField(max_length=30, blank=False)
    code_nuser = models.CharField(max_length=30, blank=False)
    logic = models.CharField(max_length=4000, blank=False)
    num_mrow = models.DecimalField(blank=False, max_digits=8, decimal_places=0)
    bl_merge = models.CharField(max_length=1, blank=False)
    bl_init = models.CharField(max_length=1, blank=False)
    bl_active = models.CharField(max_length=1, blank=False)
    u_cr = models.CharField(max_length=30, blank=False)
    u_md = models.CharField(max_length=30, blank=False)
    d_cr = models.DateTimeField(blank=False)
    d_md = models.DateTimeField(blank=False)
    cmnt = models.CharField(max_length=300, blank=False)


# defn_dtype
class DefnDType(models.Model):
    class Meta:
        db_table = 'defn_dtype'
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    dscp = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    bl_active = models.CharField(max_length=1, blank=False)
    u_cr = models.CharField(max_length=30, blank=False)
    u_md = models.CharField(max_length=30, blank=False)
    d_cr = models.DateTimeField(blank=False)
    d_md = models.DateTimeField(blank=False)
    cmnt = models.CharField(max_length=300, blank=False)
    type_group = models.CharField(max_length=3)


# defn_dm
class DefnDm(models.Model):
    class Meta:
        db_table = 'defn_dm'
    name = models.CharField(max_length=30)
    dscp = models.CharField(max_length=100)
    type = models.CharField(max_length=10)
    logic = models.CharField(max_length=9999)
    lvl = models.IntegerField()
    num_mrow = models.DecimalField(blank=False, max_digits=8, decimal_places=0)
    bl_merge = models.CharField(max_length=1, blank=False)
    bl_right = models.CharField(max_length=1, blank=False)
    bl_init = models.CharField(max_length=1, blank=False)
    bl_access = models.CharField(max_length=1, blank=False)
    bl_lock = models.CharField(max_length=1, blank=False)
    bl_active = models.CharField(max_length=1, blank=False)
    u_cr = models.CharField(max_length=30, blank=False)
    u_md = models.CharField(max_length=30, blank=False)
    d_cr = models.DateTimeField(blank=False)
    d_md = models.DateTimeField(blank=False)
    cmnt = models.CharField(max_length=300, blank=False)


# defn_dr
class DefnDr(models.Model):
    class Meta:
        db_table = 'defn_dr'
    name = models.CharField(max_length=30)
    dscp = models.CharField(max_length=100)
    type = models.CharField(max_length=10)
    logic = models.CharField(max_length=9999)
    lvl = models.IntegerField()
    array_column = models.CharField(max_length=200)
    array_str_column = models.CharField(max_length=200)
    num_mrow = models.DecimalField(blank=False, max_digits=8, decimal_places=0)
    bl_merge = models.CharField(max_length=1, blank=False)
    bl_right = models.CharField(max_length=1, blank=False)
    bl_init = models.CharField(max_length=1, blank=False)
    bl_access = models.CharField(max_length=1, blank=False)
    bl_lock = models.CharField(max_length=1, blank=False)
    bl_active = models.CharField(max_length=1, blank=False)
    u_cr = models.CharField(max_length=30, blank=False)
    u_md = models.CharField(max_length=30, blank=False)
    d_cr = models.DateTimeField(blank=False)
    d_md = models.DateTimeField(blank=False)
    cmnt = models.CharField(max_length=300, blank=False)


# defn_ds
class DefnDs(models.Model):
    class Meta:
        db_table = 'defn_ds'
    name = models.CharField(max_length=30)
    dscp = models.CharField(max_length=100)
    type_strc = models.CharField(max_length=10)
    type_incr = models.CharField(max_length=10)
    logic = models.CharField(max_length=4000)
    array_tkey = models.CharField(max_length=100)
    array_pkey = models.CharField(max_length=100)
    array_spkey = models.CharField(max_length=100)
    array_ikey = models.CharField(max_length=100)
    code_stamp = models.CharField(max_length=30)
    bl_lock = models.CharField(max_length=1, blank=False)
    bl_active = models.CharField(max_length=1, blank=False)
    u_cr = models.CharField(max_length=30, blank=False)
    u_md = models.CharField(max_length=30, blank=False)
    d_cr = models.DateTimeField(blank=False)
    d_md = models.DateTimeField(blank=False)
    cmnt = models.CharField(max_length=300, blank=False)


# defn_ds_dtl
class DefnDsDtl(models.Model):
    class Meta:
        db_table = 'defn_ds_dtl'
    id_ds = models.IntegerField()
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=200)
    dscp = models.CharField(max_length=100)
    sn = models.IntegerField()
    str_dtype = models.CharField(max_length=100)
    str_default = models.CharField(max_length=100)
    bl_null = models.CharField(max_length=1, blank=False)
    bl_active = models.CharField(max_length=1, blank=False)
    u_cr = models.CharField(max_length=30, blank=False)
    u_md = models.CharField(max_length=30, blank=False)
    d_cr = models.DateTimeField(blank=False)
    d_md = models.DateTimeField(blank=False)
    cmnt = models.CharField(max_length=300, blank=False)


# monitor_log_timer
class MonitorLogTimer(models.Model):
    class Meta:
        db_table = 'monitor_log_timer'
    id_exec = models.IntegerField()
    name_exec = models.CharField(max_length=255)
    lvl = models.IntegerField()
    name_lvl = models.CharField(max_length=255)
    code_object = models.CharField(max_length=255)
    d_begin = models.DateTimeField(blank=False)
    d_end = models.DateTimeField(blank=False)
    times_s = models.IntegerField()
    times_m = models.DecimalField(blank=False, max_digits=8, decimal_places=0)
    times_h = models.DecimalField(blank=False, max_digits=8, decimal_places=0)


# monitor_log_debug
class MonitorLogDebug(models.Model):
    class Meta:
        db_table = 'monitor_log_debug'
    id_proc = models.IntegerField()
    name_proc = models.CharField(max_length=255)
    id_inst = models.IntegerField()
    name_inst = models.CharField(max_length=255)
    id_prog = models.IntegerField()
    name_prog = models.CharField(max_length=255)
    id_type = models.IntegerField()
    name_type = models.CharField(max_length=255)
    code_object = models.CharField(max_length=255)
    logic = models.CharField(max_length=4000)
    str_exec = models.CharField(max_length=4000)
    d_cr = models.DateTimeField(blank=False)


# monitor_log_error
class MonitorLogError(models.Model):
    class Meta:
        db_table = 'monitor_log_error'
    id_proc = models.IntegerField()
    name_proc = models.CharField(max_length=255)
    id_inst = models.IntegerField()
    name_inst = models.CharField(max_length=255)
    id_prog = models.IntegerField()
    name_prog = models.CharField(max_length=255)
    code_object = models.CharField(max_length=255)
    logic = models.CharField(max_length=4000)
    code_error = models.CharField(max_length=255)
    name_error = models.CharField(max_length=255)
    str_error = models.CharField(max_length=255)
    d_cr = models.DateTimeField(blank=False)


