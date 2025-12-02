from rest_framework.authentication import TokenAuthentication

class CustomHeaderTokenAuthentication(TokenAuthentication):
    keyword = 'Token'
    
    def authenticate(self, request):
        auth = request.META.get('HTTP_X_AUTH_TOKEN')
        if auth:
            request.META['HTTP_AUTHORIZATION'] = f'Token {auth}'
        
        return super().authenticate(request)