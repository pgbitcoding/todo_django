from django.contrib.auth.tokens import PasswordResetTokenGenerator  
from django.utils import six  

class TokenGenerator(PasswordResetTokenGenerator):  
    def _make_hash_value(self, user, timestamp):  
        return (  
            six.text_type(user.pk)   
        )  
account_activation_token = TokenGenerator()  