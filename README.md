# OTP Backend

This is the OTP Relay System Backend. It provides a clean, scalable, production-ready backend foundation using Django and Django REST Framework.

## Prerequisites

- Python 3.9+
- PostgreSQL

## Installation

### Virtual Environment

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Requirements Installation

Install all required Python dependencies:

```bash
pip install -r requirements.txt
```

### Environment Variables

Copy the `.env.example` file to `.env` and fill in the required database credentials and secrets:

```bash
cp .env.example .env
```

Ensure your PostgreSQL instance is running and you have created a database matching your `.env` configuration.

### Migration

Run database migrations to initialize the database tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Run Server

Start the development server:

```bash
python manage.py runserver
```

## REST API Endpoints

The backend exposes a simple, flexible REST API prefixed with `/api/v1/`.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/health/` | Health check endpoint returning `{"status": "ok"}`. |
| `GET` | `/api/v1/otp-messages/` | Returns a list of all stored OTP messages, ordered newest first. |
| `POST` | `/api/v1/otp-messages/` | Creates a new OTP message record. |
| `GET` | `/api/v1/otp-messages/<uuid>/` | Retrieves a specific OTP message by its UUID. |

### Example Request

**`POST /api/v1/otp-messages/`**

```json
{
    "otp": "483921",
    "sender": "bKash",
    "receiver_number": "+88017XXXXXXXX",
    "message_body": "Your OTP is 483921",
    "received_at": "2026-07-30T12:00:00Z",
    "metadata": {
        "sender_type": "ALPHANUMERIC",
        "carrier": "Grameenphone",
        "sim_slot": 0
    },
    "raw_payload": {
        "android_version": 16,
        "device_model": "Pixel 8"
    }
}
```

### Example Response

**`201 Created`**

```json
{
    "id": "e4f8d5b1-12c8-4a5e-b9e7-9d7a2b0c3a2f",
    "otp": "483921",
    "sender": "bKash",
    "receiver_number": "+88017XXXXXXXX",
    "message_body": "Your OTP is 483921",
    "received_at": "2026-07-30T12:00:00Z",
    "metadata": {
        "sender_type": "ALPHANUMERIC",
        "carrier": "Grameenphone",
        "sim_slot": 0
    },
    "raw_payload": {
        "android_version": 16,
        "device_model": "Pixel 8"
    },
    "created_at": "2026-07-30T12:01:05.123456Z",
    "updated_at": "2026-07-30T12:01:05.123456Z"
}
```

## Testing

You can interact with and test the APIs using either the built-in Swagger documentation or the provided Postman collection.

### Swagger URL

Once the development server is running, access the interactive API documentation at:

- **Swagger UI:** `http://localhost:8000/api/swagger/`
- **ReDoc UI:** `http://localhost:8000/api/redoc/`
- **OpenAPI Schema:** `http://localhost:8000/api/schema/`

*How to use Swagger:* Navigate to the Swagger UI URL in your browser. You can click on any endpoint (like `POST /api/v1/otp-messages/`), click "Try it out", edit the JSON body, and execute the request directly from the browser. 

### Postman Usage

A ready-to-use Postman Collection is located in `docs/postman_collection.json`.

*How to use Postman:*
1. Open the Postman App.
2. Click **Import** (top left).
3. Select the `docs/postman_collection.json` file from this repository.
4. The collection "OTP Backend API" will appear in your workspace containing pre-configured requests (with example bodies) for Health Check, Listing OTPs, Creating OTPs, and Retrieving a specific OTP.

## Database Model

The backend is built around a single primary model designed to capture incoming Android SMS data efficiently and flexibly.

### `OTPMessage`

This model stores intercepted SMS messages that contain OTPs. 

#### Fields Explanation

- `id`: A UUID primary key ensuring global uniqueness and security against ID-guessing.
- `otp`: (`CharField`) The extracted One-Time Password. It is nullable, allowing the Android app to send the message even if OTP extraction fails locally.
- `sender`: (`CharField`) The origin phone number or alphanumeric sender ID of the SMS.
- `receiver_number`: (`CharField`) The phone number of the Android device that received the message.
- `message_body`: (`TextField`) The full, unmodified body of the received SMS.
- `received_at`: (`DateTimeField`) The exact timestamp when the SMS was received by the Android device.
- `metadata`: (`JSONField`) Why it exists: To provide extreme flexibility. If the Android app eventually needs to send extra contextual information (like device ID, carrier name, battery level, Android version), it can simply include it in this JSON block. The backend will accept and store it without requiring database schema changes or new migrations.
- `raw_payload`: (`JSONField`) Why it exists: As an audit and debugging mechanism. It stores the exact, original JSON payload exactly as it was received from the Android device. If parsing fails, or if a bug occurs, this field allows developers to trace what the device actually sent.
- `created_at`: (`DateTimeField`) System timestamp indicating when the record was created in the database.
- `updated_at`: (`DateTimeField`) System timestamp updated automatically whenever the record is modified.

## Deployment (Render)

This backend is pre-configured for automated deployment on Render using Infrastructure as Code (IaC) via `render.yaml`.

### 1. Connecting your GitHub Repository
1. Push this repository to your GitHub account.
2. Sign in to your [Render Dashboard](https://dashboard.render.com).
3. Go to the "Blueprints" tab.
4. Click "New Blueprint Instance".
5. Connect your GitHub account and select this repository.

### 2. Creating the PostgreSQL Database
Render automatically reads the `render.yaml` file in this repository. It will automatically provision a free PostgreSQL database named `otp_db` for you.
No manual database creation is required—the Blueprint handles it.
The `DATABASE_URL` will be automatically generated and injected into the Web Service environment variables.

### 3. Required Environment Variables
Most environment variables are handled automatically by the `render.yaml` Blueprint (e.g., `DATABASE_URL` and a securely auto-generated `DJANGO_SECRET_KEY`).
However, you can manage the following in the Render Dashboard (under the Environment tab of your Web Service) if you need to override them:

| Variable | Default (in render.yaml) | Description |
|---|---|---|
| `DJANGO_SETTINGS_MODULE` | `config.settings.production` | Directs Django to use the production settings file. |
| `DJANGO_DEBUG` | `False` | Must be `False` in production for security. |
| `DJANGO_ALLOWED_HOSTS` | `*` | Allows Render to route traffic. You can restrict this to your specific `.onrender.com` domain later. |
| `PYTHON_VERSION` | `3.9.6` | Tells Render which Python version to use for the build environment. |

### 4. Verifying Deployment
1. Once the blueprint finishes syncing, Render will start building the service using `build.sh` (which installs dependencies, runs migrations, and collects static files).
2. After the build succeeds, it will deploy using Gunicorn.
3. Once the status turns "Live", click on the Web Service URL provided by Render (e.g., `https://otp-backend-xxxx.onrender.com`).
4. Append `/api/v1/health/` to the URL.
5. If you see `{"status": "ok"}`, your deployment is successful! You can also check `/api/swagger/` to see the live documentation.
