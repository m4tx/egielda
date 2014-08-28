from django.contrib.auth import forms


class PasswordChangeForm(forms.PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

        # Set all inputs the "required" attribute
        for field in self.fields:
            self.fields[field].widget.attrs['required'] = 'required'