# Contenedores

El proyecto implementa una aplicación web tipo To-Do (CRUD) distribuida en tres servicios siguiendo el patrón de microservicios: frontend, backend (API) y base de datos.
- **Se despliega en dos máquinas de la red local (LAN):**
  - Máquina A – Steam Deck (Windows + Docker): aloja backend y base de datos en contenedores separados.
  - Máquina B – Raspberry Pi 4 (Docker ARM64): aloja el frontend estático servido por Nginx.

Objetivo didáctico: practicar orquestación con contenedores, separación de responsabilidades, comunicación entre servicios por red y uso de variables de entorno (12-factor).

![explicacion imagen](../Imagenes/InformacionGeneral.png)

- **Componentes y responsabilidades**
  - Frontend (Raspberry Pi 4, Docker) SPA construida (p. ej., React + Vite) y servida por Nginx.  
    Responsabilidad: interfaz de usuario y consumo de la API vía HTTP/JSON.  
  - Backend / API (Steam Deck, Docker) Servicio FastAPI (o Node/Express) que implementa la lógica de negocio y expone endpoints REST para crear, listar, actualizar y eliminar tareas.  
    Responsabilidad: validación, reglas de negocio, acceso a la BD.  
  - Base de datos (Steam Deck, Docker) Contenedor con PostgreSQL (o MySQL/MariaDB) que almacena las tareas en tablas relacionales.  
    Responsabilidad: persistencia y consultas de datos.  
- **Topología de red**
  - El frontend (Pi) se comunica con el backend (Deck) mediante la IP LAN de la Máquina A y el puerto 8000.
  - El backend se comunica con la base de datos por la red interna de Docker en la Máquina A (la BD no publica puertos al host).
  - No existe comunicación directa entre frontend y base de datos (principio de “backend-for-frontend”).
