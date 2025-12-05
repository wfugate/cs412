## tracker/authentication.py
## Author: William Fugate wfugate@bu.edu
## description: authentication classes for runtracker app
from rest_framework.authentication import TokenAuthentication

class CustomHeaderTokenAuthentication(TokenAuthentication): #overwrite TokenAuthentication to use our custom auth token instead
    keyword = 'Token'
    
    def authenticate(self, request):
        auth = request.META.get('HTTP_X_AUTH_TOKEN') #get the custom auth token from the request
        if auth:
            request.META['HTTP_AUTHORIZATION'] = f'Token {auth}' #use it instead of the normal auth token (also add Token prefix)
        
        return super().authenticate(request)