from django import forms
from .models import Oferta, HistoricoOferta, Empleado

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'dni', 'codigo_nfc', 'estado', 'informacion_adicional', 'documento']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_nfc': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'informacion_adicional': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'documento': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        
        
        

class OfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = [
            'numero_de_oferta',  # Opcional: si deseas mostrarlo en el formulario
            'persona_responsable',
            'cliente',
            'empresa',
            'estado',
            'importe_euros',
            'documento',
            'url',
        ]
        widgets = {
            'numero_de_oferta': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'persona_responsable': forms.Select(attrs={'class': 'form-select'}),
            'cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'importe_euros': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'documento': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(OfertaForm, self).__init__(*args, **kwargs)
        # Filtrar persona_responsable para roles 'Oficina' o 'Direccion'
        self.fields['persona_responsable'].queryset = Empleado.objects.filter(rol__in=['Oficina', 'Direccion'])
        # Si 'numero_de_oferta' es autogenerado, puedes ocultarlo o hacerlo readonly
        if not self.instance.pk:
            self.fields['numero_de_oferta'].widget.attrs['readonly'] = True
            self.fields['numero_de_oferta'].required = False
        else:
            self.fields['numero_de_oferta'].required = False
    
    def clean_documento(self):
        documento = self.cleaned_data.get('documento', False)
        if documento:
            if documento.size > 4*1024*1024:
                raise forms.ValidationError("El archivo es demasiado grande. Tamaño máximo: 4MB.")
            if not documento.name.endswith('.pdf'):
                raise forms.ValidationError("Solo se permiten archivos PDF.")
        return documento

class HistoricoOfertaForm(forms.ModelForm):
    class Meta:
        model = HistoricoOferta
        fields = [
            'oferta',
            'estado',
            'comentario',
            'importe',
            'documento',
            'url',
        ]
        widgets = {
            'oferta': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': 250}),
            'importe': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'documento': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
        }
    
    def clean_documento(self):
        documento = self.cleaned_data.get('documento', False)
        if documento:
            if documento.size > 4*1024*1024:
                raise forms.ValidationError("El archivo es demasiado grande. Tamaño máximo: 4MB.")
            if not documento.name.endswith('.pdf'):
                raise forms.ValidationError("Solo se permiten archivos PDF.")
        return documento