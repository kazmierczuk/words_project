from django.shortcuts import render
from .static.py.a_star import a_Loop

# View with matrix bg and user input
def welcome_page(request):
    return render(request, 'matrix/welcome_page.html')

# Shows all possible combinations of given letters and descriptions of the words
def results(request):
    definitions = a_Loop('letters')
    contex = {'definitions':definitions}
    return render(request, 'matrix/results.html', context=contex)

# About author and the project
def about(request):
    return render(request, 'matrix/about.html')
