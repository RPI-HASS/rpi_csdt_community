from registration.forms import RegistrationForm
from captcha.fields import CaptchaField

class CaptchaRegistrationForm(RegistrationForm):
    captcha = CaptchaField()

