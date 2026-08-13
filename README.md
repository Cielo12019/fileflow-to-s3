# Sistema de Sincronización Documental

**Solución personalizada**

Herramienta automatizada para sincronizar archivos desde el repositorio SharePoint de FERROANDES hacia AWS S3, garantizando la preservación, seguridad y accesibilidad centralizada de documentos críticos en las operaciones logísticas ferroviarias.

## Características

✓ Descarga automática de documentos desde SharePoint FERROANDES  
✓ Sincronización segura a AWS S3  
✓ Soporte para descarga de archivos individuales, carpetas completas o por patrón  
✓ Autenticación Office365 integrada  
✓ Manejo robusto de errores  
✓ Logs detallados de operaciones  

## Instalación

### Requisitos
- Python 3.8 o superior
- Acceso a SharePoint de FERROANDES
- Credenciales AWS S3

### Pasos de configuración

1. **Clonar o descargar el proyecto**
```bash
cd fileflow-to-s3
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar credenciales** (`config.json`)
```json
{
    "share_point": {
        "user": "tu_usuario@ferroandesperu.sharepoint.com",
        "password": "tu_contraseña",
        "url": "https://ferroandesperu.sharepoint.com",
        "site": "https://ferroandesperu.sharepoint.com/sites/RepositorioDocumental",
        "doc_library": "Documentos Compartidos/"
    },
    "aws_bucket": {
        "aws_access_key_id": "tu_access_key",
        "aws_secret_access_key": "tu_secret_key",
        "bucket_name": "ferroandes-documentos-s3",
        "bucket_subfolder": "repositorio-sincronizado"
    }
}
```

## Uso

### Descargar una carpeta completa
```bash
python project.py "Documentos/2024" "C:/descargas" "None" "None"
```

### Descargar un archivo específico
```bash
python project.py "Documentos/2024" "C:/descargas" "manifiesto_carga.pdf" "None"
```

### Descargar archivos por patrón (expresión regular)
```bash
python project.py "Documentos/2024" "C:/descargas" "None" ".*\.pdf$"
```

### Parámetros
- **Parámetro 1**: Ruta de la carpeta en SharePoint (ej: `Documentos/2024`)
- **Parámetro 2**: Ruta local de destino (ej: `C:/descargas`)
- **Parámetro 3**: Nombre de archivo específico (usar `None` si no aplica)
- **Parámetro 4**: Patrón regex para filtrar archivos (usar `None` si no aplica)

## Estructura del proyecto

```
fileflow-to-s3/
├── project.py           # Script principal de sincronización
├── sharepoint.py        # Módulo de conexión a SharePoint
├── config.json          # Configuración de credenciales y buckets
├── requirements.txt     # Dependencias de Python
└── README.md            # Este archivo
```

## Documentación técnica

### Módulo: `RepositorioDocumentalFerroandes` (sharepoint.py)
Clase especializada para gestionar conexiones y descargas desde el repositorio SharePoint de FERROANDES.

**Métodos principales:**
- `auth()`: Autentica contra Office365
- `conectar_carpeta()`: Establece conexión con una carpeta específica
- `descargar_archivo()`: Descarga un archivo individual
- `descargar_archivos()`: Obtiene lista de archivos de una carpeta

### Funciones principales (project.py)
- `subir_archivo_s3()`: Sube archivos a AWS S3
- `descargar_y_sincronizar_archivo()`: Descarga individual y sube a S3
- `descargar_y_sincronizar_carpeta()`: Sincroniza carpeta completa
- `descargar_y_sincronizar_por_patron()`: Sincroniza archivos filtrados por patrón

## Gestión de errores

El sistema incluye manejo robusto de excepciones:
- Errores de autenticación en SharePoint
- Fallos de conectividad a AWS S3
- Archivos no encontrados
- Problemas de permisos

Todos los errores se registran con mensajes descriptivos para facilitar el diagnóstico.

## Seguridad

- Nunca incluir credenciales en el código fuente
- Usar variables de entorno o bóveda de secretos para credenciales en producción
- Restringir permisos de acceso a `config.json`
- Usar roles IAM específicos en AWS con permisos mínimos
- Auditar regularmente accesos a S3

## Soporte y contacto

Para soporte técnico o reportar issues, contactar al equipo de tecnología de FERROANDES.

---
*Solución desarrollada| Versión 1.0.0*
