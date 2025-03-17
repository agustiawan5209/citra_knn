from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import  DataLatih
from .forms import LatihForm
from kelas.models import Kelas
from django.core.paginator import Paginator
from django.contrib import messages
from .csv_form import CSVUploadForm
import numpy as np
import pandas as pd
import os
# Create your views here.

def dataset_list(request):
    user_id = request.user.id
    data_latih = DataLatih.objects.all()
    print(request.GET)

    if request.GET.get('filter'):
        dataset = data_latih.filter(kelas=request.GET.get('filter'))
    else:
        dataset = data_latih.filter(created_by_id=user_id)  # Show all data if no filter is provided

    paginator = Paginator(dataset, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "dataset": page_obj,
        "title": "DataLatih",
        'kelas': Kelas.objects.all()
    }
    return render(request, "dataset/index.html", context)

def dataset_create(request):
    if not request.user.is_authenticated:
        messages.error(request, "Maaf Akses Ditolak")
        return redirect('login_app')
    form = LatihForm()
    if request.method == "POST":
        form = LatihForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.created_by = request.user
            image.created_by_id = request.user.id
            image = form.save()
            messages.success(request, "Data Latih Berhasil Di Tambah!!")
            return redirect('dataset_list')
    else:
        form =LatihForm()
        
    context = {
        'title': 'Form Tambah datalatih',
        'form': form,
        'label': Kelas,
    }
    return render(request, 'dataset/form.html', context)

def dataset_update(request, pk):
    dataset = get_object_or_404(DataLatih, pk=pk)
    if request.method == "POST":
        form = LatihForm(request.POST, instance=dataset)
        if form.is_valid():
            messages.success(request, "Data Latih Berhasil Di Ubah!!")
            form.save()
            return redirect('dataset_list')
    
    else:
        form = LatihForm(instance=dataset)
    
    context = {
        'title': 'Form Ubah datalatih',
        'form': form,
        'label': Kelas,
        
    }
    return render(request, 'dataset/form.html', context)

def dataset_delete(request, pk):
    dataset = get_object_or_404(DataLatih, pk=pk)
    if request.method == "GET":
        dataset.delete()
        messages.success(request, "Data Latih Berhasil Di Hapus!!")
        return redirect('dataset_list')
    else:
        return redirect('dataset_list')



def upload_csv(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
                return redirect('upload_csv')
            # print(csv.)
            # Jika file terlalu besar, batasi di sini
            df = pd.read_csv(csv_file, sep=";")
            created_by = request.user
            created_by_id = request.user.id
            file_dir = 'datalatih'
            for index, row in df.iterrows():
                print(row)
                label = row['class'].lower()
                kelas = Kelas.objects.get(nama=label)
                name = row['image']
                image =os.path.join(file_dir,  str(row['image']))
                hue = string_to_float(row['hue'])
                saturation = string_to_float(row['saturation'])
                value = string_to_float(row['value'])
                edges = string_to_float(row['edges'])
        
                feature = np.hstack([
                    hue,
                    saturation,
                    value,
                    edges,
                    ])
                # Simpan ke model
                # Check if an object with the same name already exists
                data_latih, created = DataLatih.objects.get_or_create(
                    nama=name,
                    defaults={
                        'image': image,
                        'feature': feature,
                        'kelas_id': kelas.id,
                        'kelas': kelas,
                        'created_by': created_by,
                        'created_by_id': created_by_id,
                    }
                )
                if not created:
                    # If the object already exists, update its fields
                    data_latih.image = image
                    data_latih.feature = feature
                    data_latih.kelas_id = kelas.id
                    data_latih.kelas = kelas
                    data_latih.created_by = created_by
                    data_latih.created_by_id = created_by_id
                    data_latih.save()
            messages.success(request, 'CSV file successfully uploaded')
            return redirect('upload_csv')
    else:
        form = CSVUploadForm()
    return render(request, 'dataset/upload_csv.html', {'form': form})


def string_to_float(var):
    if isinstance(var, str):
        var = var.replace('.', '') if '.' in var else var  # remove all decimal points except the last one
        try:
            var = float(var)
            return var
        except ValueError:
            return var  # return the original value if it cannot be converted to a float
    return var