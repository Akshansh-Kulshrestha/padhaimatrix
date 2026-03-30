from django.shortcuts import render, get_object_or_404
from .models import Course, Specialization, Subject, Unit, Topic


# 🔥 1. COURSE LIST (Homepage / Courses page)
def course_list(request):
    courses = Course.objects.all()
    return render(request, "courses/course_list.html", {
        "courses": courses
    })


# 🔥 2. COURSE DETAIL → SPECIALIZATIONS
def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    specializations = course.specializations.all()

    return render(request, "courses/course_detail.html", {
        "course": course,
        "specializations": specializations
    })


# 🔥 3. SPECIALIZATION DETAIL → SUBJECTS
def specialization_detail(request, id):
    specialization = get_object_or_404(Specialization, id=id)
    subjects = specialization.subjects.all()

    return render(request, "courses/specialization_detail.html", {
        "specialization": specialization,
        "subjects": subjects
    })


# 🔥 4. SUBJECT DETAIL → UNITS
def subject_detail(request, id):
    subject = get_object_or_404(Subject, id=id)
    units = subject.units.all()

    return render(request, "courses/subject_detail.html", {
        "subject": subject,
        "units": units
    })


# 🔥 5. UNIT DETAIL → TOPICS
def unit_detail(request, id):
    unit = get_object_or_404(Unit, id=id)
    topics = unit.topics.all()

    return render(request, "courses/unit_detail.html", {
        "unit": unit,
        "topics": topics
    })


# 🔥 6. TOPIC DETAIL → FULL CONTENT PAGE
def topic_detail(request, id):
    topic = get_object_or_404(Topic, id=id)

    return render(request, "courses/topic_detail.html", {
        "topic": topic
    })


# 🔥 7. GLOBAL SEARCH (COURSE + SUBJECT + TOPIC)
def search(request):
    query = request.GET.get('q')

    courses = Course.objects.filter(name__icontains=query) if query else []
    specializations = Specialization.objects.filter(name__icontains=query) if query else []
    subjects = Subject.objects.filter(name__icontains=query) if query else []
    topics = Topic.objects.filter(name__icontains=query) if query else []

    return render(request, "courses/search.html", {
        "query": query,
        "courses": courses,
        "specializations": specializations,
        "subjects": subjects,
        "topics": topics
    })


# 🔥 8. BREADCRUMB HELPER (OPTIONAL BUT POWERFUL)
def get_topic_hierarchy(topic):
    unit = topic.unit
    subject = unit.subject
    specialization = subject.specialization
    course = specialization.course

    return {
        "course": course,
        "specialization": specialization,
        "subject": subject,
        "unit": unit,
        "topic": topic
    }


# 🔥 9. TOPIC DETAIL WITH BREADCRUMB
def topic_detail_with_breadcrumb(request, id):
    topic = get_object_or_404(Topic, id=id)
    hierarchy = get_topic_hierarchy(topic)

    return render(request, "courses/topic_detail.html", {
        "topic": topic,
        "hierarchy": hierarchy
    })