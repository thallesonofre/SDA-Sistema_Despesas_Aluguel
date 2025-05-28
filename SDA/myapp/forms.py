from django import forms
from .models import Conta, ContaImage

class ContaForm(forms.ModelForm):
    contas = forms.FileField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}))
    class Meta:
        model = Conta
        fields = ['mes', 'descricao', 'valor'] 
        
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)  
        for field_name, field in self.fields.items():   
            field.widget.attrs['class'] = 'form-control'

class ContaImageForm(forms.ModelForm):
    class Meta:
        model = ContaImage
        fields = ['image', 'conta']