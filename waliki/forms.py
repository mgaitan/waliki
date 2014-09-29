from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Page
from ._markups import get_all_markups
from .settings import WALIKI_CODEMIRROR_SETTINGS as CM_SETTINGS


class PageForm(forms.ModelForm):
    raw = forms.CharField(label="", widget=forms.Textarea)
    # Translators: log message
    message = forms.CharField(label=_('Log message'), max_length=200, required=False)
    extra_data = forms.CharField(widget=forms.HiddenInput, required=False)


    class Media:
        modes = tuple('codemirror/mode/%s/%s.js' % (m.codemirror_mode, m.codemirror_mode)
                      for m in get_all_markups() if hasattr(m, 'codemirror_mode'))
        theme = ('codemirror/theme/%s.css' % CM_SETTINGS['theme'],) if 'theme' in CM_SETTINGS else ()

        js = ('codemirror/lib/codemirror.js',
              'codemirror/addon/mode/overlay.js') + modes + ('js/waliki.js',)
        css = {
            'all': ('codemirror/lib/codemirror.css', ) + theme
        }

    def __init__(self, *args, **kwargs):
        is_hidden = kwargs.pop('is_hidden', None)
        super(PageForm, self).__init__(*args, **kwargs)
        self.fields['raw'].initial = self.instance.raw
        self.fields['markup'].widget = forms.HiddenInput()
        # Translator: placeholder for log message
        self.fields['message'].widget = forms.TextInput(attrs={'placeholder': _('Update %s') % self.instance.path})
        if is_hidden:
            for field in self.fields.values():
                field.widget = forms.HiddenInput()

    def save(self, commit=True):
        instance = super(PageForm, self).save(commit)
        if commit:
            instance.raw = self.cleaned_data['raw']

        return instance

    class Meta:
        model = Page
        fields = ['title', 'markup', 'raw', 'message']
