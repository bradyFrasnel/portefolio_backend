from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login


class AdminLoginView(APIView):
    """
    Vue d'authentification pour l'interface admin Vue.js
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_staff:
                login(request, user)
                return Response({
                    'success': True,
                    'message': 'Authentification réussie',
                    'user': {
                        'username': user.username,
                        'is_staff': user.is_staff
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': 'Accès refusé : utilisateur non administrateur'
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({
                'success': False,
                'message': 'Identifiants incorrects'
            }, status=status.HTTP_401_UNAUTHORIZED)
