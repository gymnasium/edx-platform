from .models import ExtraInfo
from django.forms import ModelForm

class ExtraInfoForm(ModelForm):
    """
    The fields on this form are derived from the ExtraInfo model in models.py.
    """
    def __init__(self, *args, **kwargs):
        super(ExtraInfoForm, self).__init__(*args, **kwargs)
        self.fields['market'].error_messages = {
            "required": u"Please select the region nearest to you.",
            "invalid": u"Please select a valid region.",
        }

    class Meta(object):
        model = ExtraInfo
        fields = ('market',)
