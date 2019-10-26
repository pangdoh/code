from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def index2(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'index2.html', context)

def hello(request, parame1, parame2):
    print("parame1", parame1)
    print("parame2", parame2)
    a = request.GET.get('a', '无匹配')
    print(a)
    # print(b)
    return HttpResponse("接收：%s" % a)

''' 接收参数 '''
# 表单
def search_form(request):
    return render_to_response('form/search_form.html')


# 接收请求数据
def search(request):
    request.encoding = 'utf-8'
    if 'q' in request.GET and request.GET['q']: # GET第二个参数为匹配不到时的默认值。
        message = '你搜索的内容为: ' + request.GET['q']
    else:
        message = '你提交了空表单'
    return HttpResponse(message)

# 在urls.py中定义name的作用
# 在视图类中做重定向
from django.shortcuts import reverse
from django.http import HttpResponse,HttpResponseRedirect
def redirect_to(request):
    return HttpResponseRedirect(reverse('blog'))

'''
POST接收方式
ctx ={}
    if request.POST:
        ctx['rlt'] = request.POST['q']
'''