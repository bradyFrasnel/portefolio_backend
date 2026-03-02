from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class AdminLoginView(APIView):
    """
    Vue d'authentification par Token pour l'interface admin Vue.js.
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = [] # On n'exige pas de token pour se connecter
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_staff:
                # On crée ou récupère le token pour cet utilisateur
                token, created = Token.objects.get_or_create(user=user)
                
                # Optionnel : On peut quand même connecter la session côté Django
                login(request, user) 
                
                return Response({
                    'success': True,
                    'token': token.key, # C'est ce que Vue.js va stocker
                    'message': 'Authentification réussie',
                    'user': {
                        'username': user.username,
                        'is_staff': user.is_staff
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': 'Accès refusé : vous n\'êtes pas administrateur'
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({
                'success': False,
                'message': 'Identifiants incorrects'
            }, status=status.HTTP_401_UNAUTHORIZED)
