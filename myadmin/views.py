from django.shortcuts import render, redirect, reverse
from django.http.response import HttpResponse
from django.core.paginator import Paginator
from myadmin.models import Users

# Create your views here.

# 后台首页
def index(request):
    return render(request, './myadmin/index.html')

# 执行分页操作
def users(request, pIndex=1):
    # 获取会员信息
    list = Users.objects.filter()
    # 判断并封装搜索条件
    # 定义一个用于维持搜索条件的变量
    where = []
    if request.GET.get('name', '') != '':
        list = list.filter(name__contains=request.GET.get('name'))
        where.append('name='+request.GET.get('name'))
    if request.GET.get('sex', '') != '':
        list = list.filter(sex=request.GET['sex'])
        where.append('sex='+request.GET.get('sex'))
    # 传入数据和页大小来创建分页对象
    p = Paginator(list, 4)
    # 判断页号没有值时初始化为1
    if pIndex == '':
        pIndex = '1'
    pIndex = int(pIndex) #类型转换
    list2 = p.page(pIndex) #获取当前页数据
    plist = p.page_range #获取页码信息
    # 封装分页信息
    context = {'userlist':list2, 'plist':plist, 'pIndex':pIndex, 'where':where}
    return render(request, "./myadmin/users/index.html", context)

# ==============后台会员管理======================
# 浏览会员
def usersindex(request):
    # 执行数据查询，并放置在模板中
    list = Users.objects.all()
    context = {"userslist":list}
    return render(request, 'myadmin/users/index.html', context)

# 会员信息添加表单
def usersadd(request):
    return render(request, 'myadmin/users/add.html')

# 执行会员信息添加
def usersinsert(request):
    try:
        ob = Users()
        ob.username = request.POST['username']
        ob.name = request.POST['name']

        # 获取密码并md5
        import hashlib
        m = hashlib.md5()
        # update函数要求参数是bytes
        m.update(bytes(request.POST['password'], encoding="utf8"))
        ob.password = m.hexdigest()
        ob.gender = request.POST['sex']
        ob.address = request.POST['address']
        ob.state = 1
        ob.save()
        context = {"info":"添加成功"}
    except:
        context = {"info":"添加失败"}

    return render(request, "myadmin/info.html", context)

# 执行会员信息删除
def usersdel(request, uid):
    try:
        ob = Users.objects.get(id=uid)
        ob.delete()
        context = {"info":"删除成功"}
    except:
        context = {"info":"删除失败"}
    return render(request, "myadmin/info.html", context)

# 打开会员信息编辑表单
def usersedit(request, uid):
    try:
        ob = Users.objects.get(id=uid)
        context = {"user":ob}
        return render(request, "myadmin/users/edit.html", context)
    except:
        context = {"info":"没有找到要修改的信息"}
    return render(request, "myadmin/users/edit.html", context)

# 执行会员信息编辑
def usersupdate(request, uid):
    try:
        ob = Users.objects.get(id=uid)
        ob.name = request.POST['name']
        ob.gender = request.POST['sex']
        ob.address = request.POST['address']
        ob.state = request.POST['state']
        ob.save()
        context = {"info":"修改成功"}
    except:
        context = {"info":"修改失败"}
    return render(request, "myadmin/info.html", context)



# 后台管理员操作
# 会员登录表单
def login(request):
    return render(request, "myadmin/login.html")

def dologin(request):
    # 校验验证码
    verifycode = request.session['verifycode']
    code = request.POST['code'].lower()
    if verifycode != code:
        context = {"info":"验证码错误"}
        return render(request, "myadmin/login.html", context)
    try:
        # 根据账号获得登陆者信息
        user = Users.objects.get(username=request.POST['username'])
        # 判断当前用户是否为后台管理员用户
        if user.state == 0:
            # 验证密码
            import hashlib
            m = hashlib.md5()
            m.update(bytes(request.POST['password'], encoding='utf8'))
            if user.password == m.hexdigest():
                # 此处登陆成功，将当前登录信息放在session中，并跳转页面
                request.session['adminuser'] = user.name
                return redirect(reverse('myadmin_index'))
            else:
                context = {"info":"登录密码错误"}
        else:
            context = {"info":"此用户非管理员用户"}
    except:
        context = {"info":"账号登录错误"}
    return render(request, "myadmin/login.html", context)

# 会员退出
def logout(request):
    # 清除登陆的session信息
    del request.session['adminuser']
    # 跳转登录页面（url地址改变）
    return redirect(reverse('myadmin_login'))

# 会员登录表单
def verify(request):
    # 引入随机函数模块
    import random
    from PIL import Image, ImageDraw, ImageFont
    # 定义变量，用于画面的背景色，宽，高
    # 背景色设置，用RGB三个值
    bgcolor = (150,154,194)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0,100):
        xy = (random.randrange(0,width), random.randrange(0,height))
        fill = (random.randrange(0,255), 255, random.randrange(0,255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD23EFGHJK456MNOPQRS789TUVWXYZ0'
    # 随机选取四个值作为验证码
    rand_str = ''
    for i in range(0,4):
        rand_str += str1[random.randrange(0,len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('static/myadmin/font/STXIHEI.TTF', 21)
    # 构造字体颜色
    for i in range(0,4):
        # 构造字体颜色
        fontcolor = (random.randrange(0,255), random.randrange(0,255),random.randrange(0,255))
        # 绘制四个字
        draw.text((5+i*24, -4), rand_str[i], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于进一步验证
    request.session['verifycode'] = rand_str.lower()

    # 内存文件操作
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型png
    im.save(buf,'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')