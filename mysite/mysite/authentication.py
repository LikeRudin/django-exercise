from django.utils.translation import gettext_lazy as translateIfTranslationFileExist

from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from users.models import User


"""
구현 포인트 

1. 공식문서의 BasicAuthentication을 참고하여 번역파일이 있을경우 번역되게 만들었습니다.
2. Django RestFramework가 기본으로 사용하는 헤더인 Authorization의 요소로 X-USERNAME이 들어와도 괜찮게 만들었습니다.

다음 두가지 방법중 한가지로 X-USERNAME을 제공하면 됩니다.

Django restFramework가 Authorization에 사용하는 헤더: Authorization 이용
- Authorization: X-USERNAME username

X-USERNAME 헤더를 직접 추가
- X-USERNAME : username

insomnia를 이용시
표준 헤더의 X-USERNAME을 인식하지못합니다. 따옴표로 감싸서 "X-USERNAME"을 제공해주세요.
"""


class UsernameAuthentication(BaseAuthentication):

    def authenticate(self, request):
        authorization_header = get_authorization_header(request).split()
        
        if authorization_header and authorization_header[0] == b'X-USERNAME':
            try:
                username = authorization_header[1].decode('utf-8')
            except IndexError:
                raise AuthenticationFailed(translateIfTranslationFileExist('Invalid authorization header format.'))
        else:
            username = request.headers.get('X-USERNAME')

        if not username:
            return None
            
        try:
            user = User.objects.get(username=username.strip())
            return (user,None)
        
        except User.DoesNotExist:
            msg = translateIfTranslationFileExist('Invalid username.')
            raise AuthenticationFailed(msg)
    
    def authenticate_header(self, request):
        return 'Authorization:X-USERNAME realm="Provide your X-USERNAME username in the header or Authorization header"'