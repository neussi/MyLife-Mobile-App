from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from notifications.models import Notification
from .models import AdvisorInteraction

class AdvisorDispatcher:
    def __init__(self, user):
        self.user = user

    def dispatch(self, mood, reports):
        """Send notifications and/or emails based on severity and mood."""
        if not reports:
            return

        mood_data = {
            'HAPPY': ('M. Bienveillant', 'Excellente progression ! Continue comme ça.'),
            'CONCERNED': ('M. Inquiet', 'Quelques points à surveiller...'),
            'ANGRY': ('Le Contrôleur', 'Attention, ça commence à déraper !'),
            'FURIOUS': ('LE DRAGON', 'C\'EST INACCEPTABLE ! RÉAGIS TOUT DE SUITE !'),
        }

        advisor_name, title = mood_data.get(mood, ('Conseiller', 'Nouveaux conseils'))
        
        # 1. Create In-App Notifications
        for report in reports:
            Notification.objects.create(
                user=self.user,
                title=f"{advisor_name}: {report['category']}",
                message=report['message'],
                type='ADVISOR',
                link='/dashboard/' # Or specific page
            )

        # 2. Decide if we send an email (only for HIGH urgency or ANGRY/FURIOUS moods)
        high_urgency = any(r['severity'] == 'HIGH' for r in reports)
        if high_urgency or mood in ['ANGRY', 'FURIOUS']:
            self.send_advisor_email(mood, advisor_name, title, reports)

    def send_advisor_email(self, mood, advisor_name, title, reports):
        """Handle the actual email sending logic."""
        subject = f"[{advisor_name}] {title}"
        context = {
            'mood': mood,
            'mood_display': mood,
            'title': title,
            'greeting': f"Ici {advisor_name}, ton conseiller.",
            'reports': reports,
            'site_url': 'http://localhost:8000/dashboard/', # Should use absolute URI from settings
        }
        
        html_message = render_to_string('emails/advisor_notification.html', context)
        plain_message = strip_tags(html_message)
        
        try:
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [self.user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            # Log the interaction
            AdvisorInteraction.objects.create(
                user=self.user,
                mood_at_time=mood,
                message_type='ADVISOR_ALERT',
                message_content="\n".join([r['message'] for r in reports]),
                is_email=True
            )
        except Exception as e:
            # For now, just log to console or handle gracefully
            print(f"Error sending email: {e}")
