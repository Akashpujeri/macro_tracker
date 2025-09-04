from rest_framework import generics, permissions
from .models import FoodEntry, Goal, FoodTemplate
from .serializers import FoodEntrySerializer, GoalSerializer, FoodTemplateSerializer

class FoodEntryListCreateView(generics.ListCreateAPIView):
    serializer_class = FoodEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FoodEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GoalRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Goal.objects.get_or_create(user=self.request.user)[0]

class FoodTemplateListCreateView(generics.ListCreateAPIView):
    serializer_class = FoodTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FoodTemplate.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
