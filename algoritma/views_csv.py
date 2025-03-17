import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from .csv_form import CSVUploadForm
from .models import DataLatih

def upload_csv(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
                return redirect('upload_csv')

            # Jika file terlalu besar, batasi di sini

            file_data = csv_file.read().decode("utf-8")
            lines = file_data.split("\n")

            for line in lines:
                fields = line.split(",")
                if len(fields) < 3:  # Skip incomplete lines
                    continue
                filename, class_name, feature = fields[0], fields[1], fields[2]

                # Simpan ke model
                DataLatih.objects.create(
                    filename=filename,
                    class_name=class_name,
                    feature=feature
                )
            messages.success(request, 'CSV file successfully uploaded')
            return redirect('upload_csv')
    else:
        form = CSVUploadForm()
    return render(request, 'algoritma/upload_csv.html', {'form': form})
