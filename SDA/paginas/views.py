from django.views.generic import TemplateView

#View da pagina inicial
class Index(TemplateView):
    template_name = 'paginas/index.html'
