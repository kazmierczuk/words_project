from django.shortcuts import render

# Create your views here.
def welcome_page(request):
    return render(request, 'matrix/welcome_page.html')
