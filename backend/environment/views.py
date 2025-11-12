import pandas as pd
from rest_framework import generics, parsers, status, viewsets
from rest_framework.response import Response
from .models import District, EnvironmentalData
from .serializers import EnvironmentalDataSerializer, UploadCSVSerializer


# 🌿 Viewset for managing environmental data through API
class EnvironmentDataViewSet(viewsets.ModelViewSet):
    queryset = EnvironmentalData.objects.all()
    serializer_class = EnvironmentalDataSerializer


# 📂 API for uploading CSV data
class UploadCSV(generics.GenericAPIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    serializer_class = UploadCSVSerializer

    def get(self, request):
        return Response(
            {
                "detail": "POST a CSV file using multipart/form-data with the field name 'file'."
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        upload = serializer.validated_data['file']
        df = pd.read_csv(upload)

        created = 0
        for _, row in df.iterrows():
            district, _ = District.objects.get_or_create(name=row['District'])
            EnvironmentalData.objects.create(
                district=district,
                temperature=row['Temperature'],
                air_quality_index=row['AQI'],
                rainfall=row.get('Rainfall'),
                date=row['Date']
            )
            created += 1

        return Response(
            {"message": f"Data uploaded successfully! {created} rows imported."},
            status=status.HTTP_201_CREATED,
        )
