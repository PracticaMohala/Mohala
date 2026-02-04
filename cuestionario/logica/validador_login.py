from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# Importación absoluta para evitar errores de nivel de carpeta
from cuestionario.models import Trabajador

def login_view(request):
    """
    Maneja la autenticación de trabajadores usando Email y la clave Mohala2026.
    """
    error_message = None
    
    # 1. Si el usuario ya está logueado, lo mandamos al index
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        correo = request.POST.get('username')
        clave = request.POST.get('password')
        
        # 2. Autenticar contra la tabla auth_user de Django
        user = authenticate(request, username=correo, password=clave)
        
        if user is not None:
            # 3. Iniciar sesión en Django
            login(request, user)
            
            # 4. Verificar que el usuario tenga un perfil de Trabajador asociado
            try:
                Trabajador.objects.get(user=user)
                return redirect('index')
            except Trabajador.DoesNotExist:
                error_message = "Usuario válido, pero no existe un registro en la tabla Trabajador."
        else:
            error_message = "Correo o contraseña incorrectos."
            
    # 5. Definimos el diccionario de contexto para el template
    context = {
        'error': error_message
    }
    
    # 6. Renderizamos usando la ruta que incluye la subcarpeta 'cuestionario'
    return render(request, 'cuestionario/login.html', context)

def logout_view(request):
    """
    Cierra la sesión y redirige al login.
    """
    logout(request)
    return redirect('login')