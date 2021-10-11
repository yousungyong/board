from .models import Board, Reply
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
# Create your views here.
def index(request):
    kw = request.GET.get("kw", '')
    page = request.GET.get("page", 1)
    cate = request.GET.get("cate", '')

    if kw:
        if cate == 'subject':
            b = Board.objects.filter(subject__startswith=kw)
        elif cate == 'writer':
            b = Board.objects.filter(writer=kw)
        else:
            b = Board.objects.filter(content__contains=kw)
    else:
        b = Board.objects.all()

    pag = Paginator(b, 10)
    obj = pag.get_page(page)

    context={
        'con' : obj,
        'kw' : kw,
        'cate' : cate,
    }
    return render(request, "board/index.html", context)

def create(request):
    if request.method == "POST":
        s = request.POST.get('subject')
        w = request.user.username
        c = request.POST.get('content')
        if s and c:
            Board(subject=s, writer=w, content=c).save()
        return redirect("board:index")
    return render(request, "board/create.html")

def detail(request, num):
    b = Board.objects.get(id=num)
    r = b.reply_set.all()
    context={
        'con' : b,
        'rep' : r,
    }
    return render(request, "board/detail.html", context)

def delete(request, num):
    b = Board.objects.get(id=num)
    if request.user.username == b.writer:
        b.delete()
    else:
        return render(request, "error/forbidden.html")
    return redirect("board:index")

def update(request, num):
    b = Board.objects.get(id=num)
    if request.user.username == b.writer:
        if request.method == "POST":
            b.subject = request.POST.get('subject')
            b.content = request.POST.get('content')
            b.save()
            return redirect("board:detail", num=num)

        context = {
            'con' : b
        }
    else:
        return render(request, "error/forbidden.html")
    return render(request, "board/update.html", context)

def up(request, conid, st):
    b = Board.objects.get(id=conid)
    if st == 'up':
        b.up.add(request.user)
    else:
        b.up.remove(request.user)
    b.up.add(request.user)
    return redirect("board:detail", num=conid)

def create_reply(request, conid):
    b = Board.objects.get(id=conid)
    c = request.POST.get('comment')
    Reply(subject=b, comment=c, replyer=request.user.username, replyer_pic=request.user.pic).save()
    return redirect("board:detail", num=conid)


def agree(request, num, conid):
    r = Reply.objects.get(id=num)
    r.agree.add(request.user)
    return redirect("board:detail", num=conid)