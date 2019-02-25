from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

from django.shortcuts import HttpResponse,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from . import models
from . import asset_handler


@csrf_exempt
def report(request):
    '''

    :param request:
    :return:
    '''

    if request.method == "POST":
        asset_data = request.POST.get('asset_data')
        data = json.loads(asset_data)
        if not data:
            return HttpResponse(" 没有数据 !")
        if not issubclass(dict,type(data)):
            return HttpResponse("数据必须为字典格式")
        sn = data.get('sn', None)
        if sn:
            # 进入审批流程
            # 首先判断是否在上线资产中存在该sn
            asset_obj = models.Asset.objects.filter(sn=sn)
            if asset_obj:
                # 进入资产更新流程
                update_asset = asset_handler.UpdateAsset(request,asset_obj[0],data)
                return HttpResponse("资产数据已经更新！")
            else:
                # 该资产不存在，新加入资产，进入审批流程或者创建资产流程
                obj = asset_handler.NewAsset(request,data)
                response = obj.add_to_new_assets_zone()
                return HttpResponse(response)
    else:
        return HttpResponse("没有资产sn序列号，请检查数据")


@login_required(login_url='/')
def asset_list(request):
    '''
    列出所有服务器资源
    :param request:
    :return:
    '''
    username = request.user.username
    asset_all = models.Asset.objects.all()
    return render(request, 'asset/index.html', locals())


@login_required(login_url='/')
def asset_detail(request,asset_id):
    '''
    资产详情页
    :param request:
    :return:
    '''
    username = request.user.username
    asset = get_object_or_404(models.Asset,id=asset_id)
    return render(request, 'asset/asset_detail.html',locals())