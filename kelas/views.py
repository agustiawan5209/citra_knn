from django.shortcuts import render, redirect, get_object_or_404
from .models import Kelas
from .forms import KelasForm
from django.core.paginator import Paginator
from django.contrib import messages
# Create your views here.
# CRUD TABEL KELAS

def kelas_list(request):
    label_kelas = Kelas.objects.all()

    paginator = Paginator(label_kelas, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Kelas Klasifikasi',
        "kelas": page_obj,
    }
    return render(request, "kelas/index.html", context)

def kelas_create(request):
    if not request.user.is_authenticated:
        messages.error(request, "Maaf Akses Ditolak")
        return redirect('login_app')
    form = KelasForm()
    if request.method == "POST":
        form = KelasForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Kelas Label Berhasil Di Tambah!!")
            return redirect('kelas_list')
    else:
        form =KelasForm()
        
    context = {
        'title': 'Form Tambah Label Kelas',
        'form': form,
    }
    return render(request, 'kelas/form.html', context)

def kelas_update(request, pk):
    kelas = get_object_or_404(Kelas, pk=pk)
    if request.method == "POST":
        form = KelasForm(request.POST, instance=kelas)
        if form.is_valid():
            messages.success(request, "Kelas Label Berhasil Di Ubah!!")
            form.save()
            return redirect('kelas_list')
    
    else:
        form = KelasForm(instance=kelas)
    
    context = {
        'title': 'Form Ubah Label Kelas',
        'form': form,
    }
    return render(request, 'kelas/form.html', context)

def kelas_delete(request, pk):
    kelas = get_object_or_404(Kelas, pk=pk)
    if request.method == "GET":
        kelas.delete()
        messages.success(request, "Kelas Label Berhasil Di Hapus!!")
        return redirect('kelas_list')
    
    
        
