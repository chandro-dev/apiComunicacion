# API de Comunicacion (Flask + Factory Pattern)

API orientada a objetos para enviar notificaciones por `email` o `sms`, con proveedores intercambiables mediante patron `Factory`.

Incluye:
- Flask con `app factory`
- Swagger/OpenAPI con `flask-smorest`
- Docker listo para Raspberry Pi
- GitHub Actions en `self-hosted runner` para deploy simple con Docker Compose

## Arquitectura

Se aplica una separacion por capas:

- `api/`: endpoints HTTP
- `services/`: logica de negocio
- `factory/`: seleccion dinamica del proveedor
- `providers/`: integraciones externas (SMTP, Twilio SMS, console)
- `domain/`: modelos y enums

Flujo:

1. `POST /api/v1/notifications/send`
2. `NotificationService` valida reglas del canal
3. `NotificationProviderFactory` construye proveedor segun config
4. Proveedor envia y retorna `SendResult`

## Patron Factory (core)

La clase `NotificationProviderFactory` desacopla la API de implementaciones concretas:

- Email: `console`, `smtp`
- SMS: `console`, `twilio`

Cambias proveedor solo con variables de entorno, sin modificar controladores.

## Twilio trial (USD 15) recomendado para pruebas

Para gastar lo minimo y validar rapido:

1. Crea cuenta trial en Twilio y usa el credito inicial.
2. Verifica el telefono destino en Twilio (trial solo envia a numeros verificados).
3. Usa el numero trial de Twilio como `TWILIO_FROM_NUMBER`.
4. Configura `SMS_PROVIDER=twilio`.

Nota: en trial, Twilio agrega un texto de prueba al SMS y tiene restricciones de envio.

Que numero poner:
- `TWILIO_FROM_NUMBER`: el numero que Twilio te asigna en la consola (`Phone Numbers > Manage > Active numbers`), en formato E.164, por ejemplo `+1415XXXXXXX`.
- `to` en el request: tu celular verificado en Twilio, tambien en E.164. Para Colombia seria `+57` seguido del numero, por ejemplo `+573001112233`.

## Email con Twilio SendGrid (opcional)

No necesitas otro provider en codigo: puedes usar el provider `smtp` existente.

Config base para SendGrid SMTP:
- `EMAIL_PROVIDER=smtp`
- `SMTP_HOST=smtp.sendgrid.net`
- `SMTP_PORT=587`
- `SMTP_USERNAME=apikey`
- `SMTP_PASSWORD=<tu_sendgrid_api_key>`
- `SMTP_FROM=<sender_verificado_en_sendgrid>`

## Endpoints

- `GET /health`
- `POST /api/v1/notifications/send`
- Swagger UI: `GET /swagger-ui`

### Ejemplo email

```bash
curl -X POST http://localhost:8000/api/v1/notifications/send \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "email",
    "to": "destino@correo.com",
    "subject": "Prueba",
    "message": "Hola desde Flask Factory"
  }'
```

### Ejemplo SMS (Twilio)

```bash
curl -X POST http://localhost:8000/api/v1/notifications/send \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "sms",
    "to": "+573001112233",
    "message": "Prueba Twilio desde Flask"
  }'
```

## Configuracion

Ya existe un `.env` base en el proyecto. Solo reemplaza los valores `REPLACE_WITH_...`.

Configura proveedor por canal:

- `EMAIL_PROVIDER=console` o `smtp`
- `SMS_PROVIDER=console` o `twilio`

## Ejecucion local con venv (PowerShell - Windows)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python run.py
```

Si PowerShell bloquea la activacion:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Ejecucion local con venv (Linux/Mac)

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
python -m pip install --upgrade pip
pip install -r requirements.txt
python run.py
```

## Docker (Raspberry Pi)

### Construir y ejecutar local

```bash
docker compose up --build -d
```

## Deploy RPi (1 workflow)

Workflow unico:
- `.github/workflows/deploy-rpi.yml`

### 1. Preparar runner en tu servidor (Raspberry Pi / Linux)

Instala Docker, Docker Compose y registra un runner en el repo con labels:
- `self-hosted`
- `linux`

El usuario del runner debe poder ejecutar Docker:

```bash
sudo usermod -aG docker <runner_user>
sudo systemctl restart actions.runner.<org>-<repo>.<runner_name>.service
```

### 2. Guardar `.env` seguro en GitHub

No guardes credenciales en el repo. Crea un Environment `production` y agrega el secret:
- `APP_ENV_FILE` (multilinea, contenido completo de tu `.env`)

Si usas GitHub CLI:

```bash
gh secret set APP_ENV_FILE --env production < .env
```

Ejemplo de valor para `APP_ENV_FILE`:

```env
EMAIL_PROVIDER=smtp
SMS_PROVIDER=twilio
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=tu_correo@gmail.com
SMTP_PASSWORD=tu_app_password
SMTP_FROM=tu_correo@gmail.com
SMTP_TIMEOUT_SECONDS=10
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_FROM_NUMBER=+1XXXXXXXXXX
TWILIO_MESSAGING_SERVICE_SID=MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_TIMEOUT_SECONDS=10
```

### 3. Deploy automatico

Al hacer push a `main`, el workflow de CD:
1. Hace checkout del repo en el runner.
2. Crea `.env` desde `APP_ENV_FILE`.
3. Ejecuta `docker compose up -d --build --remove-orphans`.
4. Muestra estado con `docker compose ps`.

Si quieres ejecutar manualmente, usa `workflow_dispatch` en `deploy-rpi.yml`.

## Estructura

```text
communication_api/
  api/
  domain/
  factory/
  providers/
    email/
    sms/
  services/
tests/
Dockerfile
docker-compose.yml
```
