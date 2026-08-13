"""Sistema de sincronización automática de documentos FERROANDES a AWS S3

Descarga archivos del repositorio SharePoint de FERROANDES y los almacena
en AWS S3 para su preservación y acceso centralizado.

Uso:
    python project.py <carpeta> <destino> <archivo> <patrón>
"""

from sharepoint import RepositorioDocumentalFerroandes
import re
import sys, os, json
import boto3
from botocore.exceptions import ClientError

# Parámetros de línea de comandos:
# 1 = Carpeta en el repositorio FERROANDES (ej: Documentos/2024)
carpeta_origen = sys.argv[1]
# 2 = Ruta local donde se guardarán los archivos
destino_local = sys.argv[2]
# 3 = Nombre de archivo específico (si solo se descarga uno)
archivo_especifico = sys.argv[3]
# 4 = Patrón regex para filtrar archivos (ej: .*\.pdf$)
patron_archivo = sys.argv[4]


# Cargar configuración de AWS desde archivo local
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = '\\'.join([ROOT_DIR, 'config.json'])

with open(config_path) as config_file:
    config = json.load(config_file)
    config = config['aws_bucket']

AWS_ACCESS_KEY_ID = config['aws_access_key_id']
AWS_SECRET_ACCESS_KEY = config['aws_secret_access_key']
BUCKET = config['bucket_name']
BUCKET_SUBFOLDER = config['bucket_subfolder']

# Funciones de integración con AWS S3 para FERROANDES
def subir_archivo_s3(ruta_archivo_local, bucket, nombre_s3):
    """Sube un archivo al bucket de AWS S3 de FERROANDES.
    
    Args:
        ruta_archivo_local: Ruta local del archivo a subir
        bucket: Nombre del bucket de S3
        nombre_s3: Nombre del archivo en S3
        
    Returns:
        bool: True si fue exitoso, False en caso contrario
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    try:
        s3_client.upload_file(ruta_archivo_local, bucket, nombre_s3)
        print(f"✓ Archivo subido a S3: {nombre_s3}")
    except ClientError as e:
        print(f"✗ Error al subir archivo a S3: {e}")
        return False
    return True
        

def construir_ruta_s3(subcarpeta_s3, nombre_archivo):
    """Construye la ruta completa del archivo en S3.
    
    Args:
        subcarpeta_s3: Subcarpeta dentro del bucket
        nombre_archivo: Nombre del archivo
        
    Returns:
        str: Ruta completa del archivo en S3
    """
    if subcarpeta_s3 != '':
        ruta_completa = '/'.join([subcarpeta_s3, nombre_archivo])
        return ruta_completa
    else:
        return nombre_archivo

def guardar_archivo_local(nombre_archivo, contenido_archivo):
    """Guarda un archivo descargado en el sistema de archivos local.
    
    Args:
        nombre_archivo: Nombre del archivo
        contenido_archivo: Contenido del archivo en bytes
    """
    ruta_archivo = '\\'.join([destino_local, nombre_archivo])
    # Crear directorios si no existen
    os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
    with open(ruta_archivo, 'wb') as f:
        f.write(contenido_archivo)
    print(f"✓ Archivo guardado localmente: {nombre_archivo}")

def descargar_y_sincronizar_archivo(nombre_archivo, carpeta_origen):
    """Descarga un archivo de FERROANDES y lo sincroniza a S3.
    
    Args:
        nombre_archivo: Nombre del archivo a descargar
        carpeta_origen: Carpeta en el repositorio FERROANDES
    """
    contenido = RepositorioDocumentalFerroandes().descargar_archivo(nombre_archivo, carpeta_origen)
    guardar_archivo_local(nombre_archivo, contenido)
    ruta_archivo = '\\'.join([destino_local, nombre_archivo])
    nombre_s3 = construir_ruta_s3(BUCKET_SUBFOLDER, nombre_archivo)
    subir_archivo_s3(ruta_archivo, BUCKET, nombre_s3)

def descargar_y_sincronizar_carpeta(carpeta_origen):
    """Descarga todos los archivos de una carpeta FERROANDES y los sincroniza a S3.
    
    Args:
        carpeta_origen: Carpeta en el repositorio FERROANDES
    """
    repo = RepositorioDocumentalFerroandes()
    archivos_lista = repo.descargar_archivos(carpeta_origen)
    for archivo in archivos_lista:
        descargar_y_sincronizar_archivo(archivo['Name'], carpeta_origen)

def descargar_y_sincronizar_por_patron(patron, carpeta_origen):
    """Descarga archivos que coincidan con un patrón y los sincroniza a S3.
    
    Args:
        patron: Patrón regex para filtrar archivos
        carpeta_origen: Carpeta en el repositorio FERROANDES
    """
    repo = RepositorioDocumentalFerroandes()
    archivos_lista = repo.descargar_archivos(carpeta_origen)
    for archivo in archivos_lista:
        if re.search(patron, archivo['Name']):
            descargar_y_sincronizar_archivo(archivo['Name'], carpeta_origen)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Sistema de Sincronización Documental FERROANDES - S3")
    print("="*60 + "\n")
    
    try:
        if archivo_especifico != 'None':
            print(f"Descargando archivo específico: {archivo_especifico}")
            descargar_y_sincronizar_archivo(archivo_especifico, carpeta_origen)
        elif patron_archivo != 'None':
            print(f"Descargando archivos con patrón: {patron_archivo}")
            descargar_y_sincronizar_por_patron(patron_archivo, carpeta_origen)
        else:
            print(f"Descargando todos los archivos de: {carpeta_origen}")
            descargar_y_sincronizar_carpeta(carpeta_origen)
        
        print("\n✓ Sincronización completada exitosamente")
        print("="*60 + "\n")
    except Exception as e:
        print(f"\n✗ Error durante la sincronización: {e}")
        print("="*60 + "\n")
        sys.exit(1)