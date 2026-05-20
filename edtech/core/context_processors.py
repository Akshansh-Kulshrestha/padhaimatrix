from .models import  Subject

def subject_context(request):
    """
    Global context for PadhaiMatrix navigation.
    """
    return {
        
        # This handles your secondary horizontal navbar (Subjects list)
        # We prefetch 'topics' because your HTML checks {% if sub.topics.exists %}
        'subjects': Subject.objects.filter(is_published=True).prefetch_related('topics').all()
    }