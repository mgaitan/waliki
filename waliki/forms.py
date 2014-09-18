from django import forms
from .models import Page


class PageForm(forms.ModelForm):
    raw = forms.CharField(label="", widget=forms.Textarea)
    message = forms.CharField(max_length=200, required=False)

    def __init__(self, *args, **kwargs):
        is_hidden = kwargs.pop('is_hidden', None)
        super(PageForm, self).__init__(*args, **kwargs)
        self.fields['raw'].initial = self.instance.raw
        self.fields['message'].widget = forms.TextInput(attrs={'placeholder': 'Update %s' % self.instance.path})
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
        fields = ['title', 'raw', 'message']

