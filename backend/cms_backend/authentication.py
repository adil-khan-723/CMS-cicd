from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailBackend(ModelBackend):
    """Authenticate using email instead of username."""

    def authenticate(self, request, email=None, password=None, **kwargs):
        print(f"Trying to authenticate: {email}")  # Debugging

        try:
            user = User.objects.get(email=email)
            print("User found:", user)  # Debugging

            if user.check_password(password):
                print("Password correct")  # Debugging
                return user
            else:
                print("Incorrect password")  # Debugging

        except User.DoesNotExist:
            print("User does not exist")  # Debugging

        return None  # Authentication failed
        