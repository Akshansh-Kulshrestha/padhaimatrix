from .models import Course, Specialization

def courses_list(request):
    return {
        'nav_courses': Course.objects.all()
    }

def courses_nav(request):
    courses = Course.objects.prefetch_related('specializations').all()
    return {
        'nav_courses': courses
    }