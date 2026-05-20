from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from .models import CourseLevel, Specialization, Subject, Topic, UserProgress, University, Notes, Software


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

@login_required
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

@login_required
def ask(request):
    if request.method == "POST":
        # Handle question submission logic here
        pass

    return render(request, "ask.html")

@login_required
def notes_page(request):
    universities = University.objects.filter(is_published=True)
    notes_qs = Notes.objects.filter(is_published=True)

    # Capture filter parameters
    selected_uni_slug = request.GET.get('university')
    selected_branch = request.GET.get('branch')
    selected_sem = request.GET.get('semester')
    query = request.GET.get("q")

    # 1. Apply Filters
    if selected_uni_slug:
        notes_qs = notes_qs.filter(uni_name__slug=selected_uni_slug)
    
    if selected_branch:
        notes_qs = notes_qs.filter(branch=selected_branch)
    
    if selected_sem:
        notes_qs = notes_qs.filter(semester=selected_sem)

    if query:
        notes_qs = notes_qs.filter(
            Q(name__icontains=query) |
            Q(uni_name__name__icontains=query) |
            Q(branch__icontains=query)
        )

    # Get unique branches and semesters for the dropdowns
    # We only show branches that actually have notes uploaded
    available_branches = Notes.objects.filter(is_published=True).values_list('branch', flat=True).distinct()

    context = {
        "notes": notes_qs,
        "universities": universities,
        "branches": available_branches,
        "semesters": range(1, 9), # Semesters 1 to 8
        "selected_uni": selected_uni_slug,
        "selected_branch": selected_branch,
        "selected_sem": selected_sem,
    }
    return render(request, "notes.html", context)



@login_required
def software_list(request):
    software_qs = Software.objects.filter(is_published=True)

    query = request.GET.get("q")
    if query:
        software_qs = software_qs.filter(
            Q(name__icontains=query) |
            Q(code__icontains=query)
        )

    context = {
        "software_list": software_qs,
        "subjects": Subject.objects.filter(is_published=True), # Add this line
    }
    return render(request, "software_list.html", context)