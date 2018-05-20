from django import forms
from .models import (
    Directory, DirectoryItem,
)


class MainForm(forms.Form):
    dir_forms = list()
    user_id = int

class DirectoryForm(forms.ModelForm):
    item_forms = list()

    class Meta:
        model = Directory
        fields = []


class DirectoryItemForm(forms.ModelForm):

    class Meta:
        model = DirectoryItem
        fields = ["is_bad"]
