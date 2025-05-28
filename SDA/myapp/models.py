from django.db import models

# Create your models here.
class Conta(models.Model):
    mes = models.CharField(max_length=20, verbose_name="Mês")
    descricao = models.TextField(verbose_name="Descrição")
    valor = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Valor")
    
    def __str__(self):
        return self.mes
    
class ContaImage(models.Model):
    image = models.FileField('Arquivos', upload_to='image')
    conta = models.ForeignKey(Conta, related_name='contas', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.conta.name