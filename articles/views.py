from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Article, Comment
from .forms import ArticleForm, CommentForm



@require_GET  
def index(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)


@require_GET
def detail(request, article_pk):
    # 사용자가 url 에 적어보낸 article_pk 를 통해 디테일 페이지를 보여준다.
    # Article.objects.get(pk=article_pk) => 방법1
    article = get_object_or_404(Article, pk=article_pk)
    form = CommentForm()
    comments = Comment.objects.all()
    context = {'article': article, 'form': form, 'comments': comments}
    return render(request, 'articles/detail.html', context)
    

@login_required  # ==> /accounts/login/  으로 보내줌, 만약 url을 다른 방식으로 설정했으면 쟝고 세팅을 바꿔줘야함 @login_required(login_url='/accounts/login/')
# GET 요청으로 사용되는 곳만 사용할 수 있다.
# Create your views here.
def create(request):
    if request.method == 'POST':
        # Article 을 생성해달라고 하는 요청
        form = ArticleForm(request.POST)
        if form.is_valid():  # 유효성 검사
            form.save()
            return redirect('articles:index')

    else: # GET
        # Article 을 생성하기 위한 페이지를 달라고 하는 요청
        form = ArticleForm()
    context = {'form': form}
    return render(request, 'articles/create.html', context)


@login_required
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article_pk)
    else:  # GET method
        form = ArticleForm(instance=article)
    context = {'form': form}
    return render(request, 'articles/update.html', context)


@require_POST
def delete(request, article_pk):
    if request.user.is_authenticated:

        # article_pk에 맞는 article 을 꺼낸다.
        # 삭제한다.
        article = get_object_or_404(Article, pk=article_pk)
        article.delete()
    return redirect('articles:index')


@require_POST
def create_com(request, article_pk):
    if request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # 데이터베이스에는 적용시키지 마라
            comment.article_id = article_pk
            form.save()
    return redirect('articles:detail', article_pk)


@require_POST
def comments_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.delete()
        return redirect('articles:detail', article_pk)
    return HttpResponse('You are Unauthorized', status=401)

