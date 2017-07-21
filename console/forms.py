from django import forms

from .models import VHost, Snapshot, Datastore

class VHForm(forms.ModelForm):

    class Meta:
        model = VHost
        fields = ('id', 'name', 'ipaddr', 'VType','user', 'sshkey', 'sshport', 'isopath')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'VType': forms.Select(attrs={'class': 'form-control'}),
            'ipaddr': forms.TextInput(attrs={'class': 'form-control'}),
            'user': forms.TextInput(attrs={'class': 'form-control'}),
            'sshkey': forms.TextInput(attrs = {'class': 'form-control'}),
            'sshport': forms.NumberInput(attrs={'class': 'form-control'}),
            'isopath': forms.TextInput(attrs={'class': 'form-control'}),

        }

class DSForm(forms.ModelForm):

    class Meta:
        model = Datastore
        fields = ('id','name','dpath','VHost')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'dpath': forms.TextInput(attrs={'class': 'form-control'}),
            'VHost': forms.Select(attrs={'class': 'form-control'}),
        }


class SnapForm(forms.ModelForm):

    class Meta:
        model = Snapshot
        fields = ('id','name', 'suuid', 'VMachine',)




