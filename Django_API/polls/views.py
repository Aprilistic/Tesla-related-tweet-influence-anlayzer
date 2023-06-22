from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse

def first_page(request):
	return render(request, 'index.html')