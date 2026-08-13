# Notas de Implementación - FERROANDES Perú

## Información del Proyecto

**Cliente:** FERROANDESDEX 
**Solución:** Sistema de Sincronización Documental SharePoint - AWS S3  
**Versión:** 1.0.0  
**Fecha de creación:** 2024  
**Estado:** Producción  

---

## Descripción General

Este sistema ha sido desarrollado específicamente para FERROANDESDEX con el objetivo de automatizar la sincronización segura y confiable de documentos desde el repositorio compartido en SharePoint hacia AWS S3. 

### Caso de Uso

FERROANDES, empresa operadora del ferrocarril en Perú, requiere:
- Centralizar la gestión de documentos logísticos
- Garantizar la disponibilidad y redundancia de documentación crítica
- Automatizar flujos de copia de seguridad
- Facilitar acceso a archivos históricos
- Cumplir con políticas de retención de registros

### Solución Implementada

Un sistema modular que:
1. **Autentica** con SharePoint usando credenciales Office365
2. **Descarga** archivos seleccionados de carpetas específicas
3. **Almacena** archivos en el sistema de archivos local
4. **Sincroniza** documentos a AWS S3 para preservación
5. **Registra** todas las operaciones para auditoría

---

## Estructura de Carpetas Recomendada en SharePoint

```
Documentos Compartidos/
├── Documentos/
│   ├── 2024/
│   ├── 2023/
│   └── Archivo/
├── Operaciones/
│   ├── Manifiestos/
│   ├── Reportes/
│   └── Itinerarios/
├── Administrativo/
│   ├── Contratos/
│   └── Regulatorio/
└── Técnico/
    ├── Mantenimiento/
    └── Especificaciones/
```

---

## Estructura del Bucket S3

Recomendado crear la siguiente estructura en S3:

```
ferroandes-documentos-s3/
└── repositorio-sincronizado/
    ├── 2024/
    ├── 2023/
    ├── operaciones/
    ├── administrativo/
    └── tecnico/
```

---

## Guía de Uso por Rol

### Administrador TI
- Responsable de configuración inicial de credenciales
- Mantiene actualizada la estructura de `config.json`
- Monitorea logs de sincronización
- Gestiona actualizaciones de seguridad

### Especialista en Logística
- Solicita sincronización de documentos específicos
- Define patrones y carpetas a sincronizar
- Valida completitud de archivos en S3

### Auditoría
- Revisa logs de operaciones
- Verifica integridad de documentos sincronizados
- Confirma cumplimiento de políticas de retención

---

## Configuración de Automatización

### Opción 1: Windows Task Scheduler

Crear una tarea programada:
```
Programa: C:\Python\python.exe
Argumentos: C:\ferroandes-sync\project.py "Documentos/2024" "C:\sync-local" "None" "None"
Frecuencia: Diaria a las 02:00 AM
```

### Opción 2: Linux Cron

Agregar a crontab:
```
0 2 * * * cd /home/ferroandes/fileflow-to-s3 && python project.py "Documentos/2024" "/mnt/sync-local" "None" "None"
```

### Opción 3: Docker

Construir imagen:
```bash
docker build -t ferroandes-sync .
docker run --env-file .env ferroandes-sync
```

---

## Monitoreo y Alertas

### Métricas Recomendadas
- Cantidad de archivos sincronizados por día
- Tamaño total de datos transferidos
- Tiempo de ejecución
- Tasa de errores

### Alertas Sugeridas
- Fallo de autenticación SharePoint
- Error de conexión a AWS S3
- Sincronización tardía (> 30 minutos)
- Archivo no encontrado

---

## Mantenimiento y Actualizaciones

### Verificaciones Mensuales
- [ ] Validar conectividad a SharePoint
- [ ] Verificar permisos AWS S3
- [ ] Revisar logs de errores
- [ ] Confirmar espacio disponible en S3

### Respuesta a Incidentes
1. **Fallo de sincronización**: Revisar logs en `project.py`
2. **Error de credenciales**: Validar config.json y permisos
3. **Problemas de conectividad**: Verificar VPN y firewall
4. **Bajo rendimiento**: Revisar tamaño de carpetas

---

## Mejoras Futuras

- [ ] Interfaz web de monitoreo
- [ ] Notificaciones por correo
- [ ] Caché de metadatos locales
- [ ] Validación de integridad (checksums MD5)
- [ ] Compresión de archivos antes de subida
- [ ] Multi-threading para sincronización paralela


