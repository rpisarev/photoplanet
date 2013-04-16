from django.http import HttpResponse

def home(request):
    body = '''<html>
<body>
<p>Hello, World!</p>
</body>
</html>'''
    return HttpResponse(body)
