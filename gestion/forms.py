from django import forms
from .models import Message, Coment

class MessageForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Message
        fields = ('text',)

class ComentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Coment
        fields = ('text',)
