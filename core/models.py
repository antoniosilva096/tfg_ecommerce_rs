from datetime import timezone
from django.db import models
from django.urls import reverse

# Create your models here.

class Empleado(models.Model):
    ESTADOS_CHOICES = [
        ('activo', 'Activo'),
        ('baja', 'Baja'),
    ]

    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    codigo_nfc = models.CharField(max_length=50, unique=True)
    estado = models.CharField(max_length=10, choices=ESTADOS_CHOICES, default='activo')
    informacion_adicional = models.CharField(max_length=250, blank=True, null=True)
    documento = models.FileField(upload_to='documentos_empleados/', blank=True, null=True)
    rol = models.CharField(max_length=50, choices=[
        ('Oficina', 'Oficina'),
        ('Direccion', 'Direccion'),
        ('Tecnico', 'Tecnico'),
    ])

    def __str__(self):
        return f"{self.nombre} ({self.dni})"
    
    
    
    
    

class Oferta(models.Model):
    ESTADO_CHOICES = [
        ('inicio_conversacion', 'Inicio de la conversación'),
        ('oferta_enviada', 'Oferta enviada'),
        ('esperando_respuesta', 'Esperando respuesta'),
        ('cancelada', 'Cancelada'),
        ('aprobada', 'Aprobada'),
    ]

    numero_de_oferta = models.CharField(max_length=6, unique=True, editable=False)
    persona_responsable = models.ForeignKey(
        Empleado,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'rol__in': ['Oficina', 'Direccion']},
        related_name='ofertas_responsable'
    )
    cliente = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)
    estado = models.CharField(max_length=25, choices=ESTADO_CHOICES, default='inicio_conversacion')

    def save(self, *args, **kwargs):
        if not self.numero_de_oferta:
            current_year = timezone.now().year
            last_two_digits = str(current_year)[-2:]
            last_oferta = Oferta.objects.filter(numero_de_oferta__startswith=last_two_digits).order_by('-numero_de_oferta').first()
            if last_oferta:
                last_num = int(last_oferta.numero_de_oferta[-4:])
                new_num = last_num + 1
            else:
                new_num = 1
            self.numero_de_oferta = f"{last_two_digits}{new_num:04d}"
        super(Oferta, self).save(*args, **kwargs)

    def __str__(self):
        return self.numero_de_oferta

    def get_absolute_url(self):
        return reverse('oferta_detail', kwargs={'pk': self.pk})
    
    
    
class HistoricoOferta(models.Model):
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE, related_name='historicos')
    fecha_creacion_estado = models.DateTimeField(auto_now_add=True)
    comentario = models.CharField(max_length=250, blank=True, null=True)
    estado = models.CharField(max_length=25, choices=Oferta.ESTADO_CHOICES)
    importe_euros = models.DecimalField(max_digits=10, decimal_places=2)
    documento = models.FileField(upload_to='historico_ofertas_documentos/', blank=True, null=True)
    url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.oferta.numero_de_oferta} - {self.get_estado_display()} - {self.fecha_creacion_estado.strftime('%d/%m/%Y')}"

    class Meta:
        ordering = ['-fecha_creacion_estado']
        