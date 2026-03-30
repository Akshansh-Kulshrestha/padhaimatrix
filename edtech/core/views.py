from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone

from .models import (
    Article,
    CourseLevel,
    Specialization,
    Subject,
    Topic,
    ArticleCorrection,
    ArticleSuggestion
)

def article_list(request):
    articles = Article.objects.filter(is_published=True)

    # 🔍 Search
    query = request.GET.get("q")

    # 🎯 Filters
    course = request.GET.get("course")
    specialization = request.GET.get("specialization")
    subject = request.GET.get("subject")
    topic = request.GET.get("topic")

    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    if course:
        articles = articles.filter(course_level_id=course)

    if specialization:
        articles = articles.filter(specialization_id=specialization)

    if subject:
        articles = articles.filter(subject_id=subject)

    if topic:
        articles = articles.filter(topic_id=topic)

    context = {
        "articles": articles,
        "courses": CourseLevel.objects.all(),
        "specializations": Specialization.objects.all(),
        "subjects": Subject.objects.all(),
        "topics": Topic.objects.all(),
    }

    return render(request, "articles/article_list.html", context)

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)

    # 📈 Increase views
    article.views += 1
    article.save()

    return render(request, "articles/article_detail.html", {"article": article})

@login_required
def suggest_correction(request, slug):
    article = get_object_or_404(Article, slug=slug)

    if request.method == "POST":
        suggested_title = request.POST.get("title")
        suggested_content = request.POST.get("content")
        comment = request.POST.get("comment")

        ArticleCorrection.objects.create(
            article=article,
            user=request.user,
            suggested_title=suggested_title,
            suggested_content=suggested_content,
            comment=comment
        )

        return redirect("article_detail", slug=slug)

    return render(request, "articles/suggest_correction.html", {"article": article})

@login_required
def suggest_article(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        course = request.POST.get("course")
        specialization = request.POST.get("specialization")
        subject = request.POST.get("subject")
        topic = request.POST.get("topic")

        ArticleSuggestion.objects.create(
            user=request.user,
            title=title,
            content=content,
            course_level_id=course if course else None,
            specialization_id=specialization if specialization else None,
            subject_id=subject if subject else None,
            topic_id=topic if topic else None
        )

        return redirect("article_list")

    context = {
        "courses": CourseLevel.objects.all(),
        "specializations": Specialization.objects.all(),
        "subjects": Subject.objects.all(),
        "topics": Topic.objects.all(),
    }

    return render(request, "articles/suggest_article.html", context)

def trending_articles(request):
    articles = Article.objects.filter(is_published=True).order_by("-views")[:10]

    return render(request, "articles/trending.html", {"articles": articles})