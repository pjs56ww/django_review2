from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model  # 현재 활성화(active)된 user model 을 return 한다.


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', ]
