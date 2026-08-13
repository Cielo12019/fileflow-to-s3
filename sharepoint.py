"""Módulo de conexión a SharePoint para FERROANDES Perú

Permite la autenticación y descarga de archivos desde los repositorios
de documentos de SharePoint utilizados en los procesos logísticos de FERROANDES.
"""

from shareplum import Site, Office365
from shareplum.site import Version

import json, os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = '\\'.join([ROOT_DIR, 'config.json'])


# Cargar configuración de autenticación
with open(config_path) as config_file:
    config = json.load(config_file)
    config = config['share_point']

USERNAME = config['user']
PASSWORD = config['password']
SHAREPOINT_URL = config['url']
SHAREPOINT_SITE = config['site']
SHAREPOINT_DOC = config['doc_library']

class RepositorioDocumentalFerroandes:
    """Cliente de conexión a SharePoint especializado para FERROANDES.
    
    Proporciona métodos para autenticación, navegación de carpetas y descarga
    de archivos desde el repositorio documental de FERROANDES.
    """
    
    def auth(self):
        """Autentica contra el servidor Office365 de FERROANDES."""
        self.authcookie = Office365(SHAREPOINT_URL, username=USERNAME, password=PASSWORD).GetCookies()
        self.site = Site(SHAREPOINT_SITE, version=Version.v365, authcookie=self.authcookie)

        return self.site

    
    def conectar_carpeta(self, nombre_carpeta):
        """Conecta con una carpeta específica en el repositorio de FERROANDES.
        
        Args:
            nombre_carpeta: Ruta de la carpeta dentro del repositorio documental
        """
        self.auth_site = self.auth()

        self.sharepoint_dir = ''.join([SHAREPOINT_DOC, nombre_carpeta])
        self.folder = self.auth_site.Folder(self.sharepoint_dir)

        return self.folder

    def descargar_archivo(self, nombre_archivo, nombre_carpeta):
        """Descarga un archivo específico de una carpeta del repositorio FERROANDES.
        
        Args:
            nombre_archivo: Nombre del archivo a descargar
            nombre_carpeta: Carpeta donde se encuentra el archivo
        """
        carpeta = self.conectar_carpeta(nombre_carpeta)
        return carpeta.get_file(nombre_archivo)

    def _obtener_lista_archivos(self, nombre_carpeta):
        """Obtiene la lista de archivos disponibles en una carpeta.
        
        Args:
            nombre_carpeta: Carpeta a listar
        """
        carpeta = self.conectar_carpeta(nombre_carpeta)
        return carpeta.files

    def descargar_archivos(self, nombre_carpeta):
        """Descarga todos los archivos de una carpeta específica.
        
        Args:
            nombre_carpeta: Carpeta de donde descargar los archivos
        """
        archivos_lista = self._obtener_lista_archivos(nombre_carpeta)
        return archivos_lista