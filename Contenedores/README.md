# Contenedores (To-Do App en 2 máquinas)

Aplicación **To-Do** (CRUD) distribuida en **tres contenedores** siguiendo el patrón de microservicios:
- **Backend (API)** y **Base de datos** se ejecutan en la **Steam Deck (Windows + Docker Desktop)**.
- **Frontend** (SPA estática) se ejecuta en la **Raspberry Pi 4 (Kali + Docker)**.

Objetivo: practicar separación por servicios, comunicación por red (LAN) y uso de variables de entorno.

![Arquitectura general](../Imagenes/InformacionGeneral.png)

---

## Arquitectura y responsabilidades

- **Frontend – Raspberry Pi (Nginx + React/Vite)**
  - Interfaz de usuario. Consume la API vía HTTP/JSON.
  - Expone **5173/tcp** hacia la LAN.
  - En el build se inyecta `VITE_API_URL="http://<IP_DECK>:8000"`.

- **Backend – Steam Deck (FastAPI + Uvicorn)**
  - Lógica de negocio y endpoints REST (`/health`, `/todos`).
  - Expone **8000/tcp** hacia la LAN.
  - CORS permite el origen del frontend: `CORS_ORIGINS=http://<IP_PI>:5173`.

- **Base de datos – Steam Deck (PostgreSQL 16 Alpine)**
  - Persistencia de tareas.
  - **Solo** accesible desde el backend por la **red interna de Docker** (hostname `db:5432`).
  - Volumen `pg_data` para persistencia.

**Flujo de red**
- Frontend (Pi) → Backend (Deck) por **LAN**: `http://<IP_DECK>:8000`.
- Backend (Deck) → DB (Deck) por **red interna de Docker**: `db:5432`.
- No hay acceso directo Frontend → DB.

---

## Capturas del sistema en ejecución

**Contenedores en el Deck (backend + DB):**  
![Deck corriendo](../Imagenes/ContenedorDeckCoriendo.png)

**Frontend sirviendo en la Raspberry Pi:**  
![Pi corriendo](../Imagenes/RaspheryCoriendoPagina.png)

---

## Instalación de Docker (resumen)

- **Raspberry Pi (Kali)**

```bash
  sudo apt update
  sudo apt install -y docker.io
  sudo systemctl enable --now docker
  sudo usermod -aG docker $USER && newgrp docker

  # Compose v2 (si hace falta):
  mkdir -p ~/.docker/cli-plugins
  curl -SL https://github.com/docker/compose/releases/download/v2.28.1/docker-compose-linux-armv7 \
    -o ~/.docker/cli-plugins/docker-compose
  chmod +x ~/.docker/cli-plugins/docker-compose

  docker --version
  docker compose version
```

- **Steam Deck (Windows)**

```bash
wsl --install
wsl --set-default-version 2
winget install -e --id Docker.DockerDesktop
docker --version
docker compose version

```

## Despliegue
```bash
cd ~/Desktop/frontend
docker compose build --no-cache
docker compose up -d
# Abrir en navegador: http://<IP_PI>:5173

```

- **Steam Deck (Windows)**

```bash

cd "$env:USERPROFILE\OneDrive\Desktop\todo-stack"
docker compose up -d --build
curl.exe http://localhost:8000/health   # {"status":"ok"}

```

## Problemas encontrados (Raspberry Pi + contenedores) y lecciones

Durante el desarrollo salieron varios tropiezos típicos al trabajar con Docker en una Raspberry Pi 4. Los documento aquí con **síntomas, causa y solución/mitigación**.

### 1) Builds lentos en la Pi (~6 minutos la primera vez)
- **Síntoma:** construir la imagen del frontend (Node + Vite) tardó ~6 min.
- **Causas probables:**
  - CPU/IO limitados de la Pi y SD card lenta.
  - Capas base pesadas (`node:20` ~200 MB). La primera vez hay que descargar todo.
  - Falta de caché: `npm ci` descarga el árbol completo.

### 2) Página en blanco al abrir el frontend
- **Síntoma:** el navegador mostraba la página en blanco aunque Nginx devolvía 200.
- **Causa:** Nginx servía el JS con MIME incorrecto; el `<script type="module">` no se ejecutaba.
- **Solución:** incluir `mime.types` y fallback SPA en `nginx.conf`:

```bash
  ```nginx
  http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    server {
      listen 80;
      root /usr/share/nginx/html;
      location / { try_files $uri /index.html; }
    }
  }
  
  ```