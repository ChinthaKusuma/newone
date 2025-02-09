from django.shortcuts import render

def home(request):
    return render(request, "home.html")  # ✅ Loads the global template