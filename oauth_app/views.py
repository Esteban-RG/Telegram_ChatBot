from django.shortcuts import redirect, render
from django.urls import reverse
from google_auth_oauthlib.flow import InstalledAppFlow
from django.conf import settings

# Configura tus credenciales y alcances
CLIENT_SECRET_FILE = settings.GOOGLE_CLIENT_SECRET_FILE  # Archivo de credenciales
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

def login(request):
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

    # Configura el flujo de OAuth y completa el proceso
    flow = InstalledAppFlow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRET_FILE,
        scopes=['https://www.googleapis.com/auth/photoslibrary.readonly'],
        state=state  # Revisa el estado almacenado
    )

    # Completa la autenticación con el código de autorización
    credentials = flow.fetch_token(authorization_response=request.build_absolute_uri())

    # Guarda las credenciales para su uso posterior
    if credentials:
        with open(settings.TOKEN_FILE_PATH, 'w') as token_file:
            token_file.write(credentials.to_json())

    # Redirige al usuario a una página de inicio después de la autenticación
    return redirect('home')  # Redirige a la vista que deseas después de la autenticación