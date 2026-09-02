import re

with open('portfolio/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Make sure send_mail is imported
if 'from django.core.mail import send_mail' not in content:
    content = content.replace('from django.conf import settings', 'from django.conf import settings\nfrom django.core.mail import send_mail')

old_create = '''    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Message envoyé avec succès"},
            status=status.HTTP_201_CREATED,
            headers=headers
        )'''

new_create = '''    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message_obj = serializer.save()
        
        # Envoi d'email
        try:
            subject = f"Nouveau message Portfolio: {message_obj.type_projet} - {message_obj.nom}"
            mail_content = f\"\"\"Nouveau message de contact reçu !
            
Nom: {message_obj.nom}
Email: {message_obj.email}
Téléphone: {message_obj.telephone}
Type de projet: {message_obj.type_projet}
Budget: {message_obj.budget}

Message:
{message_obj.message}
            \"\"\"
            send_mail(
                subject,
                mail_content,
                settings.DEFAULT_FROM_EMAIL,
                ['mokumabrady13@gmail.com'], # Destinataire
                fail_silently=True
            )
        except Exception as e:
            print("Erreur envoi email:", e)
            
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Message envoyé avec succès"},
            status=status.HTTP_201_CREATED,
            headers=headers
        )'''

content = content.replace(old_create, new_create)

with open('portfolio/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
