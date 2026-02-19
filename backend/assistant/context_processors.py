from assistant.models import AdvisorMood

def advisor_processor(request):
    if request.user.is_authenticated:
        mood_obj, _ = AdvisorMood.objects.get_or_create(user=request.user)
        return {'advisor_mood': mood_obj}
    return {}
