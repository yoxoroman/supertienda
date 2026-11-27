from django import forms

from .models import Comentario


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ("nombre", "contenido")
        widgets = {"contenido": forms.Textarea(attrs={"rows": 5}),
                   "nombre": forms.TextInput(attrs={"placeholder": "Opcional"})}
        labels = {"nombre": "Su nombre (opcional)", "contenido": "Comentario"}
