from django.shortcuts import render

# View with matrix bg and user input
def welcome_page(request):
    return render(request, 'matrix/welcome_page.html')

# Shows all possible combinations of given letters and descriptions of the words
def results(request):
    return render(request, 'matrix/results.html')

# About author and the project
def about(request):
    return render(request, 'matrix/about.html')
