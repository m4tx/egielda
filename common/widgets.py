from django.forms import TextInput


class PhoneNumberInput(TextInput):
    input_type = 'tel'