from django.shortcuts import render
from plat_app_0_1.models import Ch_rete_dtl
from django.http import HttpResponse
from scipy.optimize import curve_fit
import numpy as np
import pandas as pd
from datetime import datetime
# Create your views here.



def mean_0(arr):
    arr = np.array(arr)
    return (arr.sum() / (arr!=0).sum())

def decay_rate(stay):
    first_day=stay[0]
    return [x / first_day for x in stay]

def func(x, a, b):
    return a * (x ** b)

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

# def search_name(request):
#     # 通过get()方法获取name关键字
#     search_name = request.GET.get("name", "")
#     # 在Event中匹配name字段
#     event_list = Ch_rete_dtl.objects.filter(ch_id__contains=search_name)
#     # 将匹配到的发布会列表注意这里是列表不是对象，返回给客户端
#     # render方法接收第三个参数是后台返回给浏览器的数据，它是一个字典。
#     # user，events 是你自定义的指针名字，会被对应的html文件应用（即event_manage）
#     return render(request, "index.html", {"events":event_list})

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
    # 将匹配到的发布会列表注意这里是列表不是对象，返回给客户端
    # render方法接收第三个参数是后台返回给浏览器的数据，它是一个字典。
    # user，events 是你自定义的指针名字，会被对应的html文件应用（即event_manage）
    return render(request, "index.html", {"events":event_list})
    #return HttpResponse(start_date1)

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
    #Django查询列表在服务端环境，字段排序会发生变化，导致基于位置的切片字段混乱，在此人为抛出问题字段
    query_df = query_df.drop('dnu',axis=1)
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
########
