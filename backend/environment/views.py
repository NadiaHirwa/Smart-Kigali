import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, parsers
from django.core.files.storage import FileSystemStorage
from .models import District, EnvironmentalData
from .serializers import EnvironmentalDataSerializer


# 🌿 Viewset for managing environmental data through API
class EnvironmentDataViewSet(viewsets.ModelViewSet):
    queryset = EnvironmentalData.objects.all()
    serializer_class = EnvironmentalDataSerializer


# 📂 API for uploading CSV data
class UploadCSV(APIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get(self, request):
        return Response(
            {
                "detail": "POST a CSV file using multipart/form-data with the field name 'file'."
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        if 'file' not in request.FILES:
            return Response(
                {"error": "No file uploaded. Use multipart/form-data with a 'file' field."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        filepath = fs.path(filename)

        # Read the uploaded CSV using pandas
        df = pd.read_csv(filepath)

        # Loop through each row and save to database
        for _, row in df.iterrows():
            district, _ = District.objects.get_or_create(name=row['District'])
            EnvironmentalData.objects.create(
                district=district,
                temperature=row['Temperature'],
                air_quality_index=row['AQI'],
                rainfall=row['Rainfall'],
                date=row['Date']
            )

        return Response({"message": "Data uploaded successfully!"}, status=status.HTTP_201_CREATED)
