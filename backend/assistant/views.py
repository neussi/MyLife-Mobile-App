from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .engine import AdvisorBrain
from .models import AdvisorInteraction

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_advisor_insight(request):
    brain = AdvisorBrain(request.user)
    mood, reports = brain.get_advice()
    
    # Log interaction
    image = request.GET.get('image', None)
    if image:
        # If we had image analysis, we would use it here.
        pass
        
    AdvisorInteraction.objects.create(
        user=request.user,
        user_message="Checking status...",
        advisor_response=str(reports),
        mood_at_time=mood
    )
    
    return Response({
        'mood': mood,
        'reports': reports,
        'anger_level': brain.mood_obj.anger_level
    })
