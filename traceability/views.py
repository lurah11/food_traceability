from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
import re
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Employee, ProductInfo, ProductDelivery, RawMaterial, TraceabilityStatus
from django.http import JsonResponse, HttpResponse
import sys, os, datetime
import pytz
# Create your views here.
def home_view(request):
    if request.user.is_authenticated :
        return redirect('traceability:welcome-view')
    return render(request,'traceability/home.html')

def login_view(request):
    if request.method == "POST" :
        username = request.POST.get('employee_login_username')
        password = request.POST.get('employee_login_pw')

    else :
        return render(request,"traceability/home.html")
    check_if_user_exists = User.objects.filter(username=username).exists()
    if check_if_user_exists:
        user = authenticate(request,username=username,password=password)
        if user is not None :
            login(request,user)
            context = {
                'user':user
            }
            return redirect("traceability:welcome-view")
        else:
            context = {
                'error':'invalid username or password'
            }
            return render (request,"traceability/home.html",context=context)
    else :
        context = {
            'error':'invalid username or password'
        }
        return render (request,"traceability/home.html",context=context)

def logout_view(request):
    logout(request)
    return redirect('traceability:home-view')

def welcome_view(request):
    emp = Employee.objects.get(user = request.user)
    no_product = False
    trace_list = ProductInfo.objects.all()
    if trace_list :
        context = {
            'trace_list' : trace_list,
            'np' : no_product
        }
        print("agus1")
    else :
        no_product = True
        print("agus2")
        context = {
            'np' : no_product
        }

    return render (request,"traceability/welcome.html",context=context)

def trace_detail_view(request,id):
    emp = Employee.objects.get(user = request.user)
    product = ProductInfo.objects.get(id=id)
    context = {
    't':product,
    }
    return render (request,"traceability/trace_detail.html",context=context)

def warehouse_view(request,id):
    emp = Employee.objects.get(user = request.user)
    delivered_qty = 0
    product = ProductInfo.objects.get(id=id)
    product_delivery_list = ProductDelivery.objects.filter(product=product)
    calc_stored_qty = product.qty_released
    for p in product_delivery_list :
        delivered_qty += p.qty
    calc_stored_qty -= delivered_qty
    actual_stored_qty = product.qty_stored
    total234 = product.qty_onhold + calc_stored_qty + delivered_qty
    total_actual = product.qty_onhold + actual_stored_qty + delivered_qty
    diff = total_actual - total234
    product.qty_delivered = delivered_qty
    product.qty_diff = diff
    product.save()
    context = {
        'pd':product_delivery_list,
        'product_id':product.id,
        'product':product,
        'delivered_qty' :delivered_qty,
        'total234':total234,
        'diff':diff,
        'calc_stored': calc_stored_qty,
        'emp':emp,
    }
    return render (request,"traceability/warehouse.html",context=context)

def warehouse_ajax_view(request, id):
        print(request.FILES)
        emp = Employee.objects.get(user=request.user)
        if request.method == 'POST':
            print("agus if 1")
            if request.POST.get('new'):
                product = ProductInfo.objects.get(id=id)
                new_pd = ProductDelivery.objects.create(product=product)
                new_pd.save()
                product_delivery_list = ProductDelivery.objects.filter(product=product)
                context = {
                    'pd':product_delivery_list,
                    'product_id':product.id,
                    'product':product,
                    'emp':emp
                }
                print("agus if 2")
                return render (request,"traceability/warehouse.html",context=context)
            elif request.POST.get('delete') :
                product_delivery = ProductDelivery.objects.get(id=request.POST.get('p_id'))
                product_delivery.delete()
                product = ProductInfo.objects.get(id=id)
                product_delivery_list = ProductDelivery.objects.filter(product=product)
                context = {
                    'pd':product_delivery_list,
                    'product_id':product.id,
                    'product':product,
                    'emp':emp
                }
                print("agus if 3")
                return render (request,"traceability/warehouse.html",context=context)
            else :
                print("agus if 4")
                print(request.FILES)
                product_id = ProductInfo.objects.get(id=id)
                p_id = request.POST.get('input_wh_hidden')
                if p_id :
                    print("agus if 5")
                    product_delivery = ProductDelivery.objects.get(id=p_id)
                    product_delivery.shipment_no = request.POST.get(f"shipment_{p_id}")
                    if request.POST.get(f"date_{p_id}") :
                        product_delivery.date = request.POST.get(f"date_{p_id}")
                    else :
                        product_delivery.date = None
                    product_delivery.receiver = request.POST.get(f"receiver_{p_id}")
                    product_delivery.destination = request.POST.get(f"destination_{p_id}")
                    product_delivery.address = request.POST.get(f"address_{p_id}")
                    product_delivery.qty = request.POST.get(f"qty_{p_id}")
                    try :
                        if request.FILES[f"record_{p_id}"]:
                            if product_delivery.record:
                                os.remove(product_delivery.record.path)
                                product_delivery.record = request.FILES[f"record_{p_id}"]
                            else :
                                product_delivery.record = request.FILES[f"record_{p_id}"]
                        else :
                            product_delivery.record.path = None
                    except :
                        print("OH noooooooooooooo")
                    product_delivery.save()
                    return redirect("traceability:warehouse-view", id=id)
                else :
                    print("agus if 6")
                    return redirect("traceability:warehouse-view", id=id)
        else :
            print("agus if 7")
            return redirect("traceability:warehouse-view", id=id)

def update_duration_view(request,id):
    emp = Employee.objects.get(user=request.user)
    product = ProductInfo.objects.get(id=id)
    total_duration = 0
    tz_indo = pytz.timezone('Asia/Jakarta')
    if request.method == 'POST' :
        print("agus lala 1")
        if emp.dept == 'qa' and request.POST.get('button') == 'start' :
            print("agus lala 2")
            now = datetime.datetime.now(tz_indo)
            product.duration = 0
            product.report_duration = 0
            product.wh_duration = 0
            product.pd_duration = 0
            product.qc_duration = 0
            product.updated = now
            product.save()
            res = {
                'total_duration':product.duration,
                'wh_duration':product.wh_duration,
                'prd_duration':product.pd_duration,
                'qc_duration':product.qc_duration,
                'report_duration':product.report_duration
            }
            return JsonResponse(res)
        elif emp.dept == 'qa' and request.POST.get('button') is None :
            print("agus lala 3")
            last_upd = product.updated
            print(last_upd)
            upd_time = datetime.datetime.now(tz_indo)
            print(upd_time)
            total_duration = upd_time - last_upd
            print(total_duration)
            int_total_duration = total_duration.seconds
            print(int_total_duration)
            product.duration = int_total_duration
            product.save()
            res = {
                'total_duration':product.duration,
                'wh_duration':product.wh_duration,
                'prd_duration':product.pd_duration,
                'qc_duration':product.qc_duration,
                'report_duration':product.report_duration
            }
            return JsonResponse(res)
        elif emp.dept == 'qa' and request.POST.get('button') == 'end' :
            print("agus lala 4")
            last_upd = product.updated
            upd_time = datetime.datetime.now(tz_indo)
            total_duration = upd_time - last_upd
            int_total_duration = total_duration.seconds
            product.duration = int_total_duration
            product.save()
            res = {
                'total_duration':product.duration,
                'wh_duration':product.wh_duration,
                'prd_duration':product.pd_duration,
                'qc_duration':product.qc_duration,
                'report_duration':product.report_duration,
                'end_traceability':'yes'
            }
            return JsonResponse(res)
        elif emp.dept == 'production' and request.POST.get('prd_submit') == 'prd_submit' :
            last_upd = product.updated
            upd_time = datetime.datetime.now(tz_indo)
            prd_duration = upd_time-last_upd
            int_prd_duration = prd_duration.seconds
            product.pd_duration = int_prd_duration
            product.save()
            res = {
                'prd_duration' : product.pd_duration
            }
            return JsonResponse(res)

        elif emp.dept == 'warehouse' and request.POST.get('wh_submit') == 'wh_submit' :
            last_upd = product.updated
            upd_time = datetime.datetime.now(tz_indo)
            wh_duration = upd_time-last_upd
            int_wh_duration = wh_duration.seconds
            product.wh_duration = int_wh_duration
            product.save()
            res = {
                'wh_duration' : product.wh_duration
            }
            return JsonResponse(res)

        elif emp.dept == 'qc' and request.POST.get('qc_submit') == 'qc_submit' :
            last_upd = product.updated
            upd_time = datetime.datetime.now(tz_indo)
            qc_duration = upd_time-last_upd
            int_qc_duration = qc_duration.seconds
            product.qc_duration = int_qc_duration
            product.save()
            res = {
                'qc_duration' : product.qc_duration
            }
            return JsonResponse(res)

        else :
            res = {
                'total_duration':product.duration,
                'wh_duration':product.wh_duration,
                'prd_duration':product.pd_duration,
                'qc_duration':product.qc_duration,
                'report_duration':product.report_duration
            }

            return JsonResponse(res)
    else :
        print("agus lala 5")
        res = {
            'total_duration':product.duration,
            'wh_duration':product.wh_duration,
            'prd_duration':product.pd_duration,
            'qc_duration':product.qc_duration,
            'report_duration':product.report_duration
        }

        return JsonResponse(res)

def start_end_traceability_ajax_view(request): #code ini ternyata tidak perlu, tapi malas hapus dan adjust lagi
    if request.method == 'POST' :
        button = request.POST.get('button')
        emp = Employee.objects.get(user=request.user)
        jsonres = {}
        if button == 'start' :
            if emp.dept=='qa':
                jsonres['status'] = 'allowed'
                jsonres['traceability_started'] = 'yes'
                jsonres['traceability_ended'] = 'no'
                return JsonResponse(jsonres)
        elif button == 'end' :
            if emp.dept =='qa' :
                jsonres['status'] = 'allowed'
                jsonres['traceability_started'] = 'no'
                jsonres['traceability_ended'] = 'yes'
                return JsonResponse(jsonres)

def check_traceability_start_view(request,id):
    emp = Employee.objects.get(user=request.user)
    product = ProductInfo.objects.get(id=id)
    status = TraceabilityStatus.objects.get(product=product)
    button = request.POST.get('button')
    wh_submit = request.POST.get('wh_submit')
    prd_submit = request.POST.get('prd_submit')
    qc_submit = request.POST.get('qc_submit')
    res = {}
    if request.method == 'POST':
        if button == 'start' and emp.dept == 'qa':
            if  status.status == False :
                status.status = True
                status.wh_submit = False
                status.prd_submit = False
                status.qc_submit = False
                status.report_submit = False
                status.save()
                res['status'] = status.status
                res['wh_submit'] = status.wh_submit
                res['prd_submit'] = status.prd_submit
                res['qc_submit'] = status.qc_submit
                res['report_submit'] = status.report_submit
                return JsonResponse(res)
            else :
                res['status'] = status.status
                return JsonResponse(res)
        elif button == 'end' and emp.dept == 'qa' :
            if status.status == True :
                status.status = False
                status.wh_submit = True
                status.prd_submit = True
                status.qc_submit = True
                status.report_submit = True
                status.save()
                res['status'] = status.status
                res['wh_submit'] = status.wh_submit
                res['prd_submit'] = status.prd_submit
                res['qc_submit'] = status.qc_submit
                res['report_submit'] = status.report_submit
                return JsonResponse(res)
            else :
                res['status'] = status.status
                return JsonResponse(res)
        if wh_submit :
            status.wh_submit = True
            status.save()
            res['wh_submit'] = status.wh_submit
            return JsonResponse(res)
        if prd_submit :
            status.prd_submit = True
            status.save()
            res['prd_submit'] = status.prd_submit
            return JsonResponse(res)
        if qc_submit :
            status.qc_submit = True
            status.save()
            res['qc_submit'] = status.qc_submit
            return JsonResponse(res)
    else :
        res['status'] = status.status
        res['wh_submit'] = status.wh_submit
        res['prd_submit'] = status.prd_submit
        res['qc_submit'] = status.qc_submit
        res['report_submit'] = status.report_submit
        return JsonResponse(res)

def production_qc_view(request,id):
    emp = Employee.objects.get(user=request.user)
    print(request.POST.get('update'))
    if request.method == 'POST':
        print("agus if 1")
        if request.POST.get('new'):
            product= ProductInfo.objects.get(id=id)
            new_rm = RawMaterial.objects.create(product=product)
            new_rm.save()
            rm_list = RawMaterial.objects.filter(product=product)
            context = {
                'rm':rm_list,
                'product_id':product.id,
                'product':product,
                'emp':emp
            }
            print("agus if 2")
            return render (request,"traceability/prod_qc.html",context=context)
        elif request.POST.get('delete') :
            rm_id = request.POST.get('p_id')
            print(f"RM ID nya delete adalah {rm_id}")
            rm = RawMaterial.objects.get(id=rm_id)
            rm.delete()
            product = ProductInfo.objects.get(id=id)
            rm_list = RawMaterial.objects.filter(product=product)
            context = {
                'rm':rm_list,
                'product_id':product.id,
                'product':product,
                'emp':emp
            }
            print("agus if 3")
            return render (request,"traceability/prod_qc.html",context=context)
        elif request.POST.get('update') :
            product_id = ProductInfo.objects.get(id=id)
            rm_id = request.POST.get('input_prd_qc_hidden')
            print(f"RM ID nya post adalah {rm_id}")
            if emp.dept == 'production':
                if rm_id :
                    upd_rawmat = RawMaterial.objects.get(id=rm_id)
                    upd_rawmat.type = request.POST.get(f'type_{rm_id}')
                    upd_rawmat.code = request.POST.get(f'code_{rm_id}')
                    upd_rawmat.batch_no = request.POST.get(f'batch_no_{rm_id}')
                    upd_rawmat.qty = request.POST.get(f'qty_{rm_id}')
                    if request.POST.get(f'prod_date_{rm_id}') :
                        upd_rawmat.prod_date = request.POST.get(f'prod_date_{rm_id}')
                    else :
                        upd_rawmat.prod_date = None
                    if request.POST.get(f'exp_date_{rm_id}'):
                        upd_rawmat.exp_date = request.POST.get(f'exp_date_{rm_id}')
                    else :
                        upd_rawmat.exp_date = None
                    upd_rawmat.save()
                    product = ProductInfo.objects.get(id=id)
                    rm_list = RawMaterial.objects.filter(product=product)
                    context = {
                        'rm':rm_list,
                        'product_id':product.id,
                        'product':product,
                        'emp':emp
                    }
                    return render (request,"traceability/prod_qc.html",context=context)
                else :
                    print("agus if 6")
                    return HttpResponse("oopppss something wrong lalala -- inside production loop")
            elif emp.dept == 'qc':
                if rm_id :
                    upd_rawmat = RawMaterial.objects.get(id=rm_id)
                    if request.POST.get(f'prod_date_{rm_id}') :
                        upd_rawmat.prod_date = request.POST.get(f'prod_date_{rm_id}')
                    else :
                        upd_rawmat.prd_date = None
                    if request.POST.get(f'exp_date_{rm_id}'):
                        upd_rawmat.exp_date = request.POST.get(f'exp_date_{rm_id}')
                    else :
                        upd_rawmat.exp_date = None
                    upd_rawmat.qc_fs = request.POST.get(f'qc_fs_{rm_id}')
                    upd_rawmat.qc_halal = request.POST.get(f'qc_halal_{rm_id}')
                    upd_rawmat.qc_note = request.POST.get(f'qc_note{rm_id}')
                    try :
                        if request.FILES[f'qcfs_atch_{rm_id}']:
                            if upd_rawmat.qcfs_atch:
                                print("apakah masuk sini 1?")
                                print(upd_rawmat.qcfs_atch.path)
                                os.remove(upd_rawmat.qcfs_atch.path)
                                print("apakah ;laalalalla")
                                upd_rawmat.qcfs_atch = request.FILES[f'qcfs_atch_{rm_id}']
                            else :
                                print("apakah masuk sini 2?")
                                upd_rawmat.qcfs_atch = request.FILES[f'qcfs_atch_{rm_id}']
                        else :
                            upd_rawmat.qcfs_atch.path = None
                    except :
                        print("errro di qcfs attachment guys")
                    try :
                        if request.FILES[f'qchalal_atch_{rm_id}']:
                            if upd_rawmat.qchalal_atch:
                                print("apakah masuk sini halal 1?")
                                os.remove(upd_rawmat.qchalal_atch.path)
                            else :
                                upd_rawmat.qchalal_atch = request.FILES[f'qchalal_atch_{rm_id}']
                        else :
                            upd_rawmat.qchalal_atch.path = None
                    except :
                        print("errro di qchalal attachment guys")
                    upd_rawmat.save()
                    product = ProductInfo.objects.get(id=id)
                    rm_list = RawMaterial.objects.filter(product=product)
                    context = {
                        'rm':rm_list,
                        'product_id':product.id,
                        'product':product,
                        'emp':emp
                    }
                    return render (request,"traceability/prod_qc.html",context=context)
                else :
                    print("agus if 6-qc")
                    return HttpResponse("oopppss something wrong lalala -- inside qc loop")

        else :
            product = ProductInfo.objects.get(id=id)
            rm_list = RawMaterial.objects.filter(product=product)
            context = {
                'rm':rm_list,
                'product_id':product.id,
                'product':product,
                'emp':emp
            }
            return render (request,"traceability/prod_qc.html",context=context)

    else :
        product = ProductInfo.objects.get(id=id)
        rm_list = RawMaterial.objects.filter(product=product)
        context = {
            'rm':rm_list,
            'product_id':product.id,
            'product':product,
            'emp':emp
        }
        return render (request,"traceability/prod_qc.html",context=context)


def report_view(request,id):
    product = ProductInfo.objects.get(id=id)
    emp = Employee.objects.get(user=request.user)
    context = {
        'product':product,
        'emp':emp
    }
    if request.method == 'POST'and emp.dept == 'qa':
        result = request.POST.get('result')
        summary = request.POST.get('summary')
        product.result = result
        product.summary = summary
        product.save()
        return render(request,"traceability/report.html", context=context)
    else :
        return render(request,"traceability/report.html",context=context)

@login_required
def html_report_view(request,id):
    allowed = True
    brand_owner = request.GET.get('brand_owner')
    other_customer = request.GET.get('other_customer')
    if brand_owner :
        allowed = True
    elif other_customer:
        allowed = False
    product = ProductInfo.objects.get(id=id)
    emp = Employee.objects.get(user=request.user)
    tz_indo = pytz.timezone('Asia/Jakarta')
    print_time = datetime.datetime.now(tz_indo)
    product_delivery_list = ProductDelivery.objects.filter(product=product)
    raw_material_list = RawMaterial.objects.filter(product=product)

    context = {
        'product':product,
        'product_delivery_list':product_delivery_list,
        'raw_material_list':raw_material_list,
        'emp':emp,
        'print_time':print_time,
        'allowed':allowed
    }
    return render(request,"traceability/html_report.html",context=context)
