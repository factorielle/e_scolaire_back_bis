from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
from StudentApp.models import Matiere, Note, Classe, Admission, Eleve, Inscription, Professeur, Enseignement, Admin, Dossier, Rapport, Appreciation, Bulletin
from StudentApp.serializers import MatiereSerializer, UserSerializer, NoteSerializer, ClasseSerializer, AdmissionSerializer, EleveSerializer, InscriptionSerializer, ProfesseurSerializer, EnseignementSerializer, AdminSerializer, DossierSerializer, RapportSerializer, AppreciationSerializer, BulletinSerializer, BulletinNoteSerializer


# Create your views here.


# Inscription
class UserSignup(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#  connnexion
class UserLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "User logged in successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)







# eleve

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def studentApi(request, id=0):
    if request.method == 'GET':
        # Récupérer tous les étudiants
        students = Eleve.objects.all()
        # Sérialiser les étudiants
        student_serializer = EleveSerializer(students, many=True)
        # Retourner les données sérialisées en tant que réponse JSON
        return JsonResponse(student_serializer.data, safe=False)
    elif request.method == 'POST':
        # Analyser les données JSON de la requête
        student_data = JSONParser().parse(request)
        # Créer un sérialiseur pour les données de l'étudiant
        student_serializer = EleveSerializer(data=student_data)
        if student_serializer.is_valid():
            # Sauvegarder l'étudiant dans la base de données
            student_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'PUT':
        student_data = JSONParser().parse(request)
        student = Eleve.objects.get(id=id)
        student_serializer = EleveSerializer(student, data=student_data)
        if student_serializer.is_valid():
            student_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method == 'DELETE':
        student = Eleve.objects.get(id=id)
        student.delete()
        return JsonResponse("Deleted Successfully", safe=False)

# # professeur
# @api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
# def profApi(request, id=0):
#     if request.method == 'GET':
#         # Récupérer tous les étudiants
#         prof= Professeur.objects.all()
#         # Sérialiser les étudiants
#         prof_serializer = ProfesseurSerializer(prof, many=True)
#         # Retourner les données sérialisées en tant que réponse JSON
#         return JsonResponse(prof_serializer.data, safe=False)
#     elif request.method == 'POST':
#         # Analyser les données JSON de la requête
#         prof_data = JSONParser().parse(request)
#         # Créer un sérialiseur pour les données de l'étudiant
#         prof_serializer = ProfesseurSerializer(data=prof_data)
#         if prof_serializer.is_valid():
#             # Sauvegarder l'étudiant dans la base de données
#             prof_serializer.save()
#             return JsonResponse("Added Successfully", safe=False)
#         return JsonResponse("Failed to Add", safe=False)
#     elif request.method == 'PUT':
#         prof_data = JSONParser().parse(request)
#         prof = Professeur.objects.get(id=id)
#         prof_serializer = ProfesseurSerializer(prof, data=prof_data)
#         if prof_serializer.is_valid():
#             prof_serializer.save()
#             return JsonResponse("Updated Successfully", safe=False)
#         return JsonResponse("Failed to Update")
#     elif request.method == 'DELETE':
#         prof = Professeur.objects.get(id=id)
#         prof.delete()
#         return JsonResponse("Deleted Successfully", safe=False)




