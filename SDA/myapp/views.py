from django.core.paginator import Paginator
from django.shortcuts import render, redirect
import csv
import datetime
from django.http import HttpResponse
import tempfile
from django.template.loader import render_to_string  
import weasyprint
from myapp.forms import ContaForm

from myapp.models import Conta, ContaImage


def conta_list(request):
    
    obj = request.GET.get('obj')
    print(obj)
    if obj:
        conta_list = Conta.objects.filter(mes__icontains=obj)
    else:
        conta_list = Conta.objects.all()
        
    paginator = Paginator(conta_list, 6) # mostra 6 contas por pagina
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'list.html', {'page_obj': page_obj})


def form_conta(request):
    form = ContaForm()
    
    if request.method == 'POST':
        form = ContaForm(request.POST, request.FILES)
        if form.is_valid():
            conta = form.save()
            
            files = request.FILES.getlist('contas')
            if files:
                for f in files:
                    ContaImage.objects.create(
                        conta=conta, 
                        image=f)
            return redirect('conta-list')
        
    return render(request, 'form-create.html', {'form': form})


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Contas' + \
        str(datetime.datetime.now())+'.csv' 
        
    writer = csv.writer(response)
    writer.writerow(['Mês','Descrição','Valor','Imagens']) # head Titulo
    
    obj = request.GET.get('obj')
    print(obj)
    
    # contas = Conta.objects.all() # lista todos as contas 
    if obj:  
        contas = Conta.objects.filter(mes__icontains=obj)  
    else:
        contas = Conta.objects.all()

    for conta in contas: 
        image_conta = [el.image.url for el in conta.contas.all()] # todas as imagens da conta
  
        writer.writerow([conta.mes, conta.descricao,
            conta.valor,image_conta])
    
    return response


def export_pdf(request): 

    obj = request.GET.get('obj')
    # contas = Contas.objects.filter(name__icontains=obj) # lista todos as contas 
    print(obj) 
    if obj:  
        contas = Conta.objects.filter(mes__icontains=obj)  
    else:
        contas = Conta.objects.all()   
         
    context = {'contas': contas}

    html_index = render_to_string('export-pdf.html', context)  

    weasyprint_html = weasyprint.HTML(string=html_index, base_url='http://127.0.0.1:8000/media')
    pdf = weasyprint_html.write_pdf(stylesheets=[weasyprint.CSS(string='body { font-family: serif} img {margin: 10px; width: 50px;}')]) 
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Contas'+str(datetime.datetime.now())+'.pdf' 
    response['Content-Transfer-Encoding'] = 'binary'
    
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(pdf)
        output.flush() 
        output.seek(0)
        response.write(output.read()) 
    return response