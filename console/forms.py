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

'''
Borrar si no se usa




class VMForm_test(forms.ModelForm):

    class Meta:
        model = VMachine
        fields = ('name', 'VHost', 'Datastore','cpu', 'mem', 'OsType', 'rdport', 'rdpuser', 'rdppass')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'VHost': forms.Select(attrs={'class': 'form-control'}),
            'Datastore':  forms.Select(attrs={'class': 'form-control'}),
            'OsType': forms.Select(attrs={'class': 'form-control'}),
            'cpu': forms.NumberInput(attrs={'class': 'form-control'}),
            'mem': forms.NumberInput(attrs={'class': 'form-control'}),
            'rdpuser': forms.TextInput(attrs = {'class': 'form-control'}),
            'rdport': forms.NumberInput(attrs={'class': 'form-control'}),
            'rdpass': forms.TextInput(attrs = {'class': 'form-control'}),
        }

class VDForm(forms.ModelForm):

    class Meta:
        model = VDisk
        fields = ('name', 'VMachine', 'size')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id_for_label': 'dname'}),
            'VMachine': forms.TextInput(attrs={'class': 'form-control'}),
            'size': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class VIForm(forms.ModelForm):

    class Meta:
        model = VBOX_IFACE
        fields = ('id','type', 'VMachine', 'driver', 'int_net', 'phy_iface')


'''






