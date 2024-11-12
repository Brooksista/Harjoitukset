from django.shortcuts import render

from rest_framework import viewsets
from .models import Tila, Varaaja, Varaus
from .serializers import TilaSerializer, VaraajaSerializer, VarausSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsUserOrAdmin
from .models import Tila, Varaaja, Varaus
from .serializers import TilaSerializer, VaraajaSerializer, VarausSerializer

# permissions

class TilaViewSet(viewsets.ModelViewSet):
    queryset = Tila.objects.all()
    serializer_class = TilaSerializer
    permission_classes = [IsAuthenticated, IsUserOrAdmin]

class VaraajaViewSet(viewsets.ModelViewSet):
    queryset = Varaaja.objects.all()
    serializer_class = VaraajaSerializer
    permission_classes = [IsAuthenticated, IsUserOrAdmin]

class VarausViewSet(viewsets.ModelViewSet):
    queryset = Varaus.objects.all()
    serializer_class = VarausSerializer
    permission_classes = [IsAuthenticated, IsUserOrAdmin]