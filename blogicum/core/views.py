from django.shortcuts import render


def handle_csrf_failure(request, reason=''):
    return render(request, 'core/403csrf.html')


def handle_404(request, exception):
    return render(request, 'core/404.html', status=404)


def handle_500(request):
    return render(request, 'core/500.html', status=500)
