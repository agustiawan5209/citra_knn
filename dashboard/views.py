from django.shortcuts import render
from datauji.models import DataUji
from algoritma.models import DataLatih
from kelas.models import Kelas
from collections import Counter
from django.http import JsonResponse
from django.http import HttpResponse
from datauji.models import DataUji
# Create your views here.

def dasboard(request):
    datalatih = DataLatih.objects.count()
    datauji = DataUji.objects.count()
    context = {
        'title': 'Dashboard',
        'datauji': datauji,
        'datalatih': datalatih,
    }
    return render(request, 'dashboard/dashboard.html', context)


def chart_data(request):
    kelas = Kelas.objects.all()
    
    data = []
    for k in kelas:
        count = DataLatih.objects.filter(kelas=k).count()
        data.append(count)
    
    labels = [kelas.nama for kelas in kelas]
    labels.append('Data Uji')
    
    data.append(DataUji.objects.count())
    
    return JsonResponse({'data': data, 'labels': labels}, safe=False)
