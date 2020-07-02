from django.shortcuts import render
from plat_app_0_1.models import Ch_rete_dtl
from django.http import HttpResponse
from scipy.optimize import curve_fit
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import *
# Create your views here.



def mean_0(arr):
    arr = np.array(arr)
    return (arr.sum() / (arr!=0).sum())

def decay_rate(stay):
    first_day=stay[0]
    return [x / first_day for x in stay]

def func(x, a, b):
    return a * (x ** b)

def date_list_gen(m):
    date_list = []
    for i in range(1,int(m)+1):
        date_tmp = str(datetime.now()+relativedelta(months=+i))[0:10]
        date_list.append(date_tmp)
    return date_list

def dau_est_dict_gen(opt,m,ch_id,dnu):
    res_list = []
    for i in range(1,int(m)+1):
        res_dict = {}
        date_tmp = str(datetime.now()+relativedelta(months=+i))[0:10]
        res_dict['date_fmt'] = date_tmp
        res_dict['ch_id'] = ch_id
        res_dict['dau'] = int(power_pred(opt,int(i)*30)*int(dnu)) #严谨的写法应取时间差
        res_dict['dnu'] = dnu
        res_list.append(res_dict)
    return res_list

def dnu_est_dict_gen(opt,m,ch_id,dau):
    res_dict = {}
    date_tmp = str(datetime.now()+relativedelta(months=+int(m)))[0:10]
    res_dict['date_fmt'] = date_tmp
    res_dict['ch_id'] = ch_id
    res_dict['dnu'] = int(int(dau)/power_pred(opt,int(m)*30)) #严谨的写法应取时间差
    res_dict['dau'] = dau
    res_list = [res_dict]
    return res_list


def power_pred(act_stay,pred_days):
    decay = decay_rate(act_stay)
    days = [x for x in range(1, len(act_stay) + 1)]  # 生成x轴列表
    popt, pcov = curve_fit(func, days, decay, method='lm', maxfev=9999999)
    # 计算预测衰减率
    pred_days = [x for x in range(1, int(pred_days) + 1)]
    pred = [func(i, popt[0], popt[1]) for i in pred_days]
    pred_res = [x * act_stay[0] for x in pred]
    lt = round(sum(pred_res) + 1, 4)
    return lt

def index(request):
    #return HttpResponse("This is a small step.")
    return render(request, "index.html")


def search_name(request):
    # 通过get()方法获取name关键字
    search_name = request.GET.get("name", "")
    date_fmt = request.GET.get("daterange","")
    # 在Event中匹配name字段
    start_date = date_fmt.split('-')[0].strip()
    end_date = date_fmt.split('-')[1].strip()
    start_date = datetime.strptime(start_date, '%m/%d/%Y').strftime('%Y-%m-%d').replace('-','')
    end_date = datetime.strptime(end_date, '%m/%d/%Y').strftime('%Y-%m-%d').replace('-','')
    event_list = Ch_rete_dtl.objects.filter(ch_id__contains=search_name,
                                            pday__gte=start_date,
                                            pday__lte=end_date)
    return render(request, "index.html", {"events":event_list})


def lt_est(request):
    return render(request, "lt_est.html")

def dau_est(request):
    return render(request, "dau_est.html")

def dnu_est(request):
    return render(request, "dnu_est.html")

def lt_est_cal(request):
    search_name = request.GET.get("name", "")
    date_fmt = request.GET.get("daterange","")
    # 在Event中匹配name字段
    start_date = date_fmt.split('-')[0].strip()
    end_date = date_fmt.split('-')[1].strip()
    start_date = datetime.strptime(start_date, '%m/%d/%Y').strftime('%Y-%m-%d').replace('-','')
    end_date = datetime.strptime(end_date, '%m/%d/%Y').strftime('%Y-%m-%d').replace('-','')
    event_list = Ch_rete_dtl.objects.filter(ch_id__contains=search_name,
                                            pday__gte=start_date,
                                            pday__lte=end_date)
    query_df = pd.DataFrame(list(event_list.values()))
    #Django查询列表在服务端环境，字段排序会发生变化，导致基于位置的切片字段混乱，故在此重新组织排序
    query_df = query_df[['id', 'pday', 'ch_id', 'rete_d1', 'rete_d2', 'rete_d3', 'rete_d4',
       'rete_d5', 'rete_d6', 'rete_d7', 'rete_d8', 'rete_d9', 'rete_d10',
       'rete_d11', 'rete_d12', 'rete_d13', 'rete_d14', 'rete_d15', 'rete_d16',
       'rete_d17', 'rete_d18', 'rete_d19', 'rete_d20', 'rete_d21', 'rete_d22',
       'rete_d23', 'rete_d24', 'rete_d25', 'rete_d26', 'rete_d27', 'rete_d28',
       'rete_d29', 'dnu']]
    days = len(query_df)
    opt = []
    for i in range(days - 1):
        opt.append(mean_0(query_df.iloc[:, i + 3][0:days - 1 - i]))
    res_dict = {}
    res_dict['date'] = date_fmt
    res_dict['name'] = search_name
    res_dict['lt_30'] = power_pred(opt,30)
    res_dict['lt_60'] = power_pred(opt, 60)
    res_dict['lt_90'] = power_pred(opt, 90)
    res_dict['lt_120'] = power_pred(opt, 120)
    res_dict['lt_180'] = power_pred(opt, 180)
    res_dict['lt_360'] = power_pred(opt, 360)
    res_list = [res_dict]
    return render(request, "lt_est.html", {"events": res_list})

def dnu_est_cal(request):
    search_name = request.GET.get("name", "")
    date_fmt = request.GET.get("daterange","")
    dau_goal = request.GET.get("dau_goal", "")
    est_time_range = request.GET.get("est_time_range", "").strip('个月')
    # datelist_build
    date_list = date_list_gen(est_time_range)

    # LT est
    start_date = date_fmt.split('-')[0].strip()
    end_date = date_fmt.split('-')[1].strip()
    start_date = datetime.strptime(start_date, '%m/%d/%Y').strftime('%Y-%m-%d').replace('-', '')
    end_date = datetime.strptime(end_date, '%m/%d/%Y').strftime('%Y-%m-%d').replace('-', '')
    event_list = Ch_rete_dtl.objects.filter(ch_id__contains=search_name,
                                            pday__gte=start_date,
                                            pday__lte=end_date)
    query_df = pd.DataFrame(list(event_list.values()))
    # Django查询列表在服务端环境，字段排序会发生变化，导致基于位置的切片字段混乱，故在此重新组织排序
    query_df = query_df[['id', 'pday', 'ch_id', 'rete_d1', 'rete_d2', 'rete_d3', 'rete_d4',
                         'rete_d5', 'rete_d6', 'rete_d7', 'rete_d8', 'rete_d9', 'rete_d10',
                         'rete_d11', 'rete_d12', 'rete_d13', 'rete_d14', 'rete_d15', 'rete_d16',
                         'rete_d17', 'rete_d18', 'rete_d19', 'rete_d20', 'rete_d21', 'rete_d22',
                         'rete_d23', 'rete_d24', 'rete_d25', 'rete_d26', 'rete_d27', 'rete_d28',
                         'rete_d29', 'dnu']]
    days = len(query_df)
    opt = []
    for i in range(days - 1):
        opt.append(mean_0(query_df.iloc[:, i + 3][0:days - 1 - i]))
    res_list = dnu_est_dict_gen(opt, est_time_range, search_name, dau_goal)
    return render(request, "dnu_est.html", {"events": res_list})

def dau_est_cal(request):
    search_name = request.GET.get("name", "")
    date_fmt = request.GET.get("daterange","")
    dau_setted = request.GET.get("dnu_data", "")
    est_time_range = request.GET.get("est_time_range", "").strip('个月')

    #datelist_build
    date_list = date_list_gen(est_time_range)

    #LT est
    start_date = date_fmt.split('-')[0].strip()
    end_date = date_fmt.split('-')[1].strip()
    start_date = datetime.strptime(start_date, '%m/%d/%Y').strftime('%Y-%m-%d').replace('-','')
    end_date = datetime.strptime(end_date, '%m/%d/%Y').strftime('%Y-%m-%d').replace('-','')
    event_list = Ch_rete_dtl.objects.filter(ch_id__contains=search_name,
                                            pday__gte=start_date,
                                            pday__lte=end_date)
    query_df = pd.DataFrame(list(event_list.values()))
    #Django查询列表在服务端环境，字段排序会发生变化，导致基于位置的切片字段混乱，故在此重新组织排序
    query_df = query_df[['id', 'pday', 'ch_id', 'rete_d1', 'rete_d2', 'rete_d3', 'rete_d4',
       'rete_d5', 'rete_d6', 'rete_d7', 'rete_d8', 'rete_d9', 'rete_d10',
       'rete_d11', 'rete_d12', 'rete_d13', 'rete_d14', 'rete_d15', 'rete_d16',
       'rete_d17', 'rete_d18', 'rete_d19', 'rete_d20', 'rete_d21', 'rete_d22',
       'rete_d23', 'rete_d24', 'rete_d25', 'rete_d26', 'rete_d27', 'rete_d28',
       'rete_d29', 'dnu']]
    days = len(query_df)
    opt = []
    for i in range(days - 1):
        opt.append(mean_0(query_df.iloc[:, i + 3][0:days - 1 - i]))
    res_list = dau_est_dict_gen(opt,est_time_range,search_name,dau_setted)
    return render(request, "dau_est.html", {"events": res_list})
    #return HttpResponse(search_name+date_fmt+dnu_setted+est_time_range)
