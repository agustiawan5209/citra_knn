from django.shortcuts import get_object_or_404, render,redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse
from rest_framework import viewsets, status
from .models import DataUji
from algoritma.models import DataLatih
from algoritma.utils import ekstraksi_ciri
from kelas.models import Kelas
from .serializers import SerializerDataUji
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers_review import MyTokenObtainPairSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing ,metrics
import numpy as np
import pandas as pd
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from PIL import Image
import numpy as np
from sklearn.preprocessing import StandardScaler
from django.core.files.uploadedfile import TemporaryUploadedFile

class PermissionUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

class PredictImageView(APIView):
    queryset = DataUji.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = SerializerDataUji
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.is_valid(raise_exception=True)  # Validate the data

            image = serializer.validated_data['image']
            temp_file = TemporaryUploadedFile(image.name, image.content_type, image.size, image.charset, image.content_type_extra)
            temp_file.write(image.read())

            img_array = ekstraksi_ciri(temp_file.temporary_file_path())
            img_array = np.array(img_array).reshape(1, -1)

            feature, labels_data = datalatihall()

            # Get the model and scaler
            knn, scaler = knn_model()  # FIX: Now scaler is used
            
            # Apply scaling to the input image features
            img_array_scaled = scaler.transform(img_array)  # FIX: Scale the input image feature

            # Make predictions
            distances, indices = knn.kneighbors(img_array_scaled)  # FIX: Use scaled image
            prediction = knn.predict(img_array_scaled)  # FIX: Use scaled image for prediction
            labels = get_object_or_404(Kelas, pk=prediction[0])

            training_object = []
            
            for x in indices[0]:
                print(labels_data[x])
                training = get_object_or_404(Kelas, pk=labels_data[x])
                training_object.append(training.nama)
            
            # Print the results for debugging
            ecludian = []
            for index, item in enumerate(distances[0]):
                ecludian.append([training_object[index], item])

            hue = img_array_scaled[0][0]
            saturation = img_array_scaled[0][1]
            value = img_array_scaled[0][2]
            edges = img_array_scaled[0][3]

            serializer.save(created_by=request.user, kelas=labels, feature=img_array_scaled)
            return Response({'predict': serializer.data, 'feature': {
                'hue': hue,
                'saturation': saturation,
                'value': value,
                'edges': edges,
            }, 'distance': ecludian})
        
        return Response('Data Tidak Dapat Dikenali', status=status.HTTP_400_BAD_REQUEST)
    
    
def datalatihall():
    datalatih = DataLatih.objects.all().order_by('nama')

    feature = []
    labels = []
    
    for row in datalatih:
        feature_list = row.feature.replace('[', '').replace(']', '').split("'") if '[' in row.feature or ']' in row.feature else row.feature

        # Remove empty strings from the list
        feature_list = [i for i in feature_list if i]

        # Split the strings that contain scientific notation into individual numbers
        feature_list = [i for sublist in [x.split() for x in feature_list] for i in sublist]

        # Convert the strings to floats
        feature_list = [float(i) for i in feature_list]
        # print(feature_list)
        feature.append(feature_list)
        labels.append(row.kelas_id)
    
    return [feature, labels]

def knn_model():
    feature, labels = datalatihall()

    # Convert feature list to numpy array
    feature = np.array(feature)
    
    # Initialize StandardScaler and scale the features
    scaler = preprocessing.StandardScaler()
    feature_scaled = scaler.fit_transform(feature)  # FIX: Apply scaling before splitting

    # Split the data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(
        feature_scaled, labels, test_size=0.02, random_state=0
    )

    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(x_train, y_train)
    
    # Return both the trained model and scaler to use later for prediction
    return knn, scaler


# CRUD API

class DataUjiViewSet(viewsets.ModelViewSet):
    queryset = DataUji.objects.all()
    serializer_class = SerializerDataUji
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return DataUji.objects.filter(created_by=user)
    
    def retrieve(self, request, pk=None):
        # Menggunakan get_object_or_404 untuk mengambil objek dengan pk yang diberikan atau mengembalikan 404 jika tidak ditemukan
        image = get_object_or_404(DataUji, pk=pk)

        # Menggunakan serializer untuk mengubah objek ke format JSON
        serializer = self.serializer_class(image)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(
                {"message": "Gambar Berhasil Di Simpan", "data": serializer.data},
                status=201,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        # Menggunakan get_object_or_404 untuk mengambil objek dengan pk yang diberikan atau mengembalikan 404 jika tidak ditemukan
        image = get_object_or_404(DataUji, pk=pk)
        image.delete()
        return Response({"message": "Gambar Berhasil Di Hapus"}, status=204)


# CRUD LOKAL SERVER

def datauji_list(request):
    list_datauji = DataUji.objects.all()

    paginator = Paginator(list_datauji, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'datauji Klasifikasi',
        "datauji": page_obj,
    }
    return render(request, "datauji/index.html", context)


def datauji_delete(request, pk):
    datauji = get_object_or_404(DataUji, pk=pk)
    if request.method == "GET":
        datauji.delete()
        messages.success(request, "datauji Berhasil Di Hapus!!")
        return redirect('datauji_list')
    