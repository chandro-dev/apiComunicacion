# API de Comunicacion (Flask + Factory Pattern)

API orientada a objetos para enviar notificaciones por `email` o `sms`, con proveedores intercambiables mediante patron `Factory`.

Incluye:
- Flask con `app factory`
- Swagger/OpenAPI con `flask-smorest`
- Docker listo para Raspberry Pi
- GitHub Actions para `test`, `build/push` multiarquitectura y `deploy` por SSH

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

## Tests

```bash
pytest -q
```

## Docker (Raspberry Pi)

### Construir y ejecutar local

```bash
docker compose up --build -d
```

### Multi-arch para RPi desde GitHub Actions

Workflow: `.github/workflows/docker-publish.yml`

Publica imagen en:
- `ghcr.io/<owner>/<repo>:latest` (main)
- `ghcr.io/<owner>/<repo>:sha-...`
- `ghcr.io/<owner>/<repo>:vX.Y.Z` (tags)

## Deploy automatico a RPi

Workflow manual: `.github/workflows/deploy-rpi.yml`

Secrets necesarios:
- `RPI_HOST`
- `RPI_USER`
- `RPI_SSH_KEY`
- `RPI_APP_DIR`
- `GHCR_USER`
- `GHCR_TOKEN`
- `GHCR_IMAGE` (ejemplo: `ghcr.io/tu-org/api-comunicacion`)

En la Raspberry, deja `docker-compose.yml` y `.env` en `RPI_APP_DIR`.

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
