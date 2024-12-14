from django.shortcuts import redirect, render
from django.urls import reverse
from google_auth_oauthlib.flow import InstalledAppFlow
from django.conf import settings
from oauth_app.models import OAuthCredentials
from django.http import JsonResponse
import json

# Configura tus credenciales y alcances
CLIENT_SECRET_FILE = settings.GOOGLE_CLIENT_SECRET_FILE  # Archivo de credenciales
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

def login(request):
    # Obtiene el user_id desde los parámetros GET
    user_id = request.GET.get('user_id')
    if not user_id:
        return render(request, 'oauth/error.html', {'message': 'user_id no proporcionado.'})

    # Guarda el user_id en la sesión para usarlo en la vista `callback`
    request.session['user_id'] = user_id

    # Obtiene el URI de redirección completo para la vista 'callback'
    redirect_uri = request.build_absolute_uri(reverse('callback'))

    print(f'URI de Redireccionamiento: {redirect_uri}')
    # Configura el flujo de OAuth
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPES
    )

    # Establece el URI de redirección correcto
    flow.redirect_uri = redirect_uri

    # Genera la URL de autorización y redirige al usuario
    auth_url, state = flow.authorization_url(
        access_type='offline',  # Necesario para obtener un refresh token
        include_granted_scopes='true'
    )

        
    # Guarda el estado en la sesión para evitar ataques CSRF
    request.session['state'] = state

    # Redirige al usuario a la URL de autenticación de Google
    return redirect(auth_url)



def callback(request):
    # Recupera el estado de la sesión
    state = request.session.get('state')
    user_id = request.session.get('user_id')

    if not user_id:
        return render(request, 'oauth/error.html', {'message': 'user_id no encontrado en la sesión.'})
    
    # Obtiene el URI de redirección completo para la vista 'callback'
    redirect_uri = request.build_absolute_uri(reverse('callback'))

    # Configura el flujo de OAuth y completa el proceso
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPES,
        state=state  # Revisa el estado almacenado
    )

    # Establece el URI de redirección correcto en el flujo
    flow.redirect_uri = redirect_uri

    # Completa la autenticación con el código de autorización
    credentials = flow.fetch_token(authorization_response=request.build_absolute_uri())

    if credentials:
        # Convierte las credenciales a JSON
        credentials_dict = credentials  # `credentials` ya es un dict en este punto

        # Cargar los valores del archivo client_secret_file
        with open(CLIENT_SECRET_FILE, 'r') as file:
            client_secrets = json.load(file)
            credentials_dict['client_id'] = client_secrets['web']['client_id']
            credentials_dict['client_secret'] = client_secrets['web']['client_secret']

        # Convertir el diccionario combinado a JSON
        credentials_json = json.dumps(credentials_dict)

        # Guarda las credenciales en la base de datos
        OAuthCredentials.objects.update_or_create(
            user_id=user_id,  # Relaciona las credenciales con el user_id
            defaults={'token': credentials_json}  # Actualiza el token si ya existe
        )

    return redirect('end')  # Redirige a la vista que deseas después de la autenticación


def get_credentials(request, user_id):
    try:
        # Buscar las credenciales asociadas al user_id
        credentials_obj = OAuthCredentials.objects.get(user_id=user_id)

        # Cargar las credenciales del modelo y devolverlas en formato JSON
        credentials_json = credentials_obj.token
        return JsonResponse({'success': True, 'credentials': credentials_json}, status=200)

    except OAuthCredentials.DoesNotExist:
        # Si no se encuentran credenciales para el user_id
        return JsonResponse({'success': False, 'error': 'Credenciales no encontradas para este user_id.'}, status=404)

    except Exception as e:
        # Manejar otros errores
        return JsonResponse({'success': False, 'error': f'Error inesperado: {str(e)}'}, status=500)


def end(request):
    template_view = "oauth/end.html"
    return render(request, template_view)