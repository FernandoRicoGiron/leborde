from django import forms

class Productos(forms.Form):
	# your_name = forms.CharField(label='Your name', max_length=100)
	nombre = forms.CharField(label='Nombre',max_length=100)
	descripcion = forms.CharField(label='Descripción', widget=forms.Textarea)
	# precio = MoneyField(max_digits=14, decimal_places=2, default_currency='MXN')
	popular = forms.BooleanField(label='Es popular',)
	# imagenes = forms.ManyToManyField()
	inventario = forms.IntegerField(label='inventario',)
	# categoria = forms.ForeignKey(Categoria, on_delete=models.CASCADE)