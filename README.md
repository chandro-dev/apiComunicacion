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
- `providers/`: integraciones externas (SMTP, Supabase OTP SMS, console)
- `domain/`: modelos y enums

Flujo:

1. `POST /api/v1/notifications/send`
2. `NotificationService` valida reglas del canal
3. `NotificationProviderFactory` construye proveedor segun config
4. Proveedor envia y retorna `SendResult`

## Patron Factory (core)

La clase `NotificationProviderFactory` desacopla la API de implementaciones concretas:

- Email: `console`, `smtp`
- SMS: `console`, `supabase_otp`

Cambias proveedor solo con variables de entorno, sin modificar controladores.

## Supabase y SMS (importante)

Supabase **no es un gateway SMS generico** para mensajes personalizados.

Con este proyecto se usa `Supabase Auth OTP` (`/auth/v1/otp`), que:
- Envia codigos OTP por SMS
- Requiere que en Supabase tengas configurado un proveedor SMS (Twilio, MessageBird, etc.)
- Ignora el texto custom del campo `message`

Si quieres SMS transaccional libre (texto arbitrario), tendras que integrar otro proveedor compatible o usar `console` para desarrollo.

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

### Ejemplo SMS (console)

```bash
curl -X POST http://localhost:8000/api/v1/notifications/send \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "sms",
    "to": "+573001112233",
    "message": "Tu OTP es 123456"
  }'
```

## Configuracion

1. Copia variables:

```bash
cp .env.example .env
```

2. Configura proveedor por canal:

- `EMAIL_PROVIDER=console` o `smtp`
- `SMS_PROVIDER=console` o `supabase_otp`

## Ejecucion local

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
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

