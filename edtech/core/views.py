from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from .models import CourseLevel, Specialization, Subject, Topic, UserProgress


def article_list(request):
    # Start with all published Subjects (the "Courses")
    subjects_qs = Subject.objects.filter(is_published=True)

    # 🔍 Search Logic
    query = request.GET.get("q")
    if query:
        subjects_qs = subjects_qs.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    # 🎯 Filter Logic (Directly filtering the Subject QuerySet)
    course_id = request.GET.get("course")
    spec_id = request.GET.get("specialization")
    subject_id = request.GET.get("subject")

    if course_id:
        # Subject -> Specialization -> CourseLevel
        subjects_qs = subjects_qs.filter(specialization__courselevel_id=course_id)

    if spec_id:
        # Subject -> Specialization
        subjects_qs = subjects_qs.filter(specialization_id=spec_id)

    if subject_id:
        # Exact Subject match
        subjects_qs = subjects_qs.filter(id=subject_id)

    context = {
        "articles": subjects_qs, # Kept as 'articles' for your template loop
        "courses": CourseLevel.objects.all(),
        "specializations": Specialization.objects.all(),
        "subjects": Subject.objects.all(), # For the dropdown filters
    }

    return render(request, "tutorials-list.html", context)


def article_detail(request, subject_slug, topic_slug):
    # 1. Fetch the topic that matches the slug AND belongs to the subject with the subject_slug
    topic = get_object_or_404(
        Topic, 
        slug=topic_slug, 
        subject__slug=subject_slug, 
        is_published=True
    )
    
    # 1. Mark as Visited/Progress
    if request.user.is_authenticated:
        UserProgress.objects.get_or_create(user=request.user, topic=topic)

    # 2. Calculate Progress Percentage
    all_topics_count = Topic.objects.filter(subject=topic.subject, is_published=True).count()
    
    if request.user.is_authenticated:
        visited_count = UserProgress.objects.filter(
            user=request.user, 
            topic__subject=topic.subject
        ).count()
        # Calculate percentage (prevent division by zero)
        progress_percent = int((visited_count / all_topics_count) * 100) if all_topics_count > 0 else 0
    else:
        progress_percent = 0
    
    # 2. Update views
    Topic.objects.filter(pk=topic.pk).update(views=F('views') + 1)
    topic.refresh_from_db()

    # 3. Sidebar: All topics in this specific subject
    sidebar_topics = Topic.objects.filter(
        subject=topic.subject, 
        is_published=True
    ).order_by('code')

    # 4. Next/Prev Logic
    prev_topic = Topic.objects.filter(
        subject=topic.subject, 
        is_published=True, 
        code__lt=topic.code
    ).order_by('-code').first()
    
    next_topic = Topic.objects.filter(
        subject=topic.subject, 
        is_published=True, 
        code__gt=topic.code
    ).order_by('code').first()

    context = {
        "article": topic,
        "sidebar_articles": sidebar_topics,
        "prev_topic": prev_topic,
        "next_topic": next_topic,
        "subjects": Subject.objects.filter(is_published=True), # Add this line
        "progress_percent": progress_percent,
    }
    return render(request, "tutorials.html", context)

@login_required
def suggest_article(request):
    if request.method == "POST":
        # Note: You'll need to update your ArticleSuggestion model 
        # to point to the new Topic/Subject hierarchy if you haven't yet.
        pass 
    
    context = {
        "courses": CourseLevel.objects.all(),
        "subjects": Subject.objects.all(),
    }
    return render(request, "articles/suggest_article.html", context)

def ask(request):
    if request.method == "POST":
        # Handle question submission logic here
        pass

    return render(request, "ask.html")