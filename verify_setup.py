#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script de verificación de configuración - FERROANDES Perú

Valida que todas las dependencias y configuraciones están correctas
antes de ejecutar el sistema de sincronización.

Uso: python verify_setup.py
"""

import os
import sys
import json
from pathlib import Path

COLOR_RESET = '\033[0m'
COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_RED = '\033[91m'
COLOR_CYAN = '\033[96m'

def print_header():
    print(f"{COLOR_CYAN}" + "="*60)
    print("VERIFICACIÓN DE CONFIGURACIÓN - FERROANDES PERÚ")
    print("Sistema de Sincronización Documental SharePoint - S3")
    print("="*60 + f"{COLOR_RESET}\n")

def print_success(message):
    print(f"{COLOR_GREEN}✓ {message}{COLOR_RESET}")

def print_warning(message):
    print(f"{COLOR_YELLOW}⚠ {message}{COLOR_RESET}")

def print_error(message):
    print(f"{COLOR_RED}✗ {message}{COLOR_RESET}")

def check_python_version():
    """Verifica versión de Python."""
    print("\n[1] Verificando versión de Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} (Compatible)")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} (Se requiere 3.8+)")
        return False

def check_files():
    """Verifica existencia de archivos requeridos."""
    print("\n[2] Verificando archivos del proyecto...")
    required_files = [
        'project.py',
        'sharepoint.py',
        'config.json',
        'requirements.txt',
        'README.md'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print_success(f"Encontrado: {file}")
        else:
            print_error(f"No encontrado: {file}")
            all_exist = False
    
    return all_exist

def check_dependencies():
    """Verifica instalación de dependencias."""
    print("\n[3] Verificando dependencias de Python...")
    required_packages = [
        'boto3',
        'botocore',
        'shareplum',
        'requests',
        'requests-ntlm'
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package)
            print_success(f"Instalado: {package}")
        except ImportError:
            print_error(f"No instalado: {package}")
            all_installed = False
    
    return all_installed

def check_config():
    """Verifica archivo de configuración."""
    print("\n[4] Verificando archivo de configuración...")
    
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print_success("Archivo JSON válido")
        
        # Verificar secciones
        required_sections = ['share_point', 'aws_bucket']
        for section in required_sections:
            if section in config:
                print_success(f"Sección encontrada: {section}")
            else:
                print_error(f"Sección faltante: {section}")
                return False
        
        # Verificar valores en SharePoint
        sp_config = config['share_point']
        if sp_config['user'] and sp_config['password']:
            print_success("Credenciales SharePoint configuradas")
        else:
            print_warning("Credenciales SharePoint vacías (será necesario completarlas)")
            return False
        
        # Verificar valores en AWS
        aws_config = config['aws_bucket']
        if aws_config['aws_access_key_id'] and aws_config['aws_secret_access_key']:
            print_success("Credenciales AWS configuradas")
        else:
            print_warning("Credenciales AWS vacías (será necesario completarlas)")
            return False
        
        print_success("Bucket S3 configurado: " + aws_config['bucket_name'])
        return True
        
    except FileNotFoundError:
        print_error("Archivo config.json no encontrado")
        return False
    except json.JSONDecodeError:
        print_error("Archivo config.json contiene JSON inválido")
        return False
    except Exception as e:
        print_error(f"Error al verificar config: {e}")
        return False

def check_aws_connectivity():
    """Intenta conectar con AWS S3."""
    print("\n[5] Verificando conectividad a AWS S3...")
    
    try:
        import boto3
        
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            aws_config = config['aws_bucket']
        
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_config['aws_access_key_id'],
            aws_secret_access_key=aws_config['aws_secret_access_key']
        )
        
        # Intentar listar buckets
        response = s3_client.list_buckets()
        print_success(f"Conectado a AWS S3 - {len(response['Buckets'])} bucket(s) accesibles")
        
        # Verificar bucket específico
        if any(b['Name'] == aws_config['bucket_name'] for b in response['Buckets']):
            print_success(f"Bucket encontrado: {aws_config['bucket_name']}")
            return True
        else:
            print_warning(f"Bucket no encontrado: {aws_config['bucket_name']}")
            return False
            
    except Exception as e:
        print_warning(f"No se puede verificar AWS S3: {e}")
        return False

def check_sharepoint_connectivity():
    """Intenta conectar con SharePoint."""
    print("\n[6] Verificando conectividad a SharePoint FERROANDES...")
    
    try:
        from sharepoint import RepositorioDocumentalFerroandes
        
        repo = RepositorioDocumentalFerroandes()
        repo.auth()
        print_success("Conectado exitosamente a SharePoint de FERROANDES")
        return True
        
    except Exception as e:
        print_warning(f"No se puede conectar a SharePoint: {e}")
        print_warning("Verificar credenciales y URL en config.json")
        return False

def main():
    print_header()
    
    checks = [
        ("Versión de Python", check_python_version),
        ("Archivos del proyecto", check_files),
        ("Dependencias", check_dependencies),
        ("Configuración", check_config),
        ("Conectividad AWS S3", check_aws_connectivity),
        ("Conectividad SharePoint", check_sharepoint_connectivity)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"Error al ejecutar verificación: {e}")
            results.append((name, False))
    
    # Resumen
    print(f"\n{COLOR_CYAN}" + "="*60)
    print("RESUMEN DE VERIFICACIÓN")
    print("="*60 + f"{COLOR_RESET}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{COLOR_GREEN}✓{COLOR_RESET}" if result else f"{COLOR_RED}✗{COLOR_RESET}"
        print(f"{status} {name}")
    
    print(f"\nResultado: {passed}/{total} verificaciones pasadas")
    
    if passed == total:
        print_success("\n¡Sistema listo! Puede proceder con la sincronización.")
        print(f"\nPróximo paso: python project.py <carpeta> <destino> <archivo> <patrón>")
        print(f"Ejemplo: python project.py 'Documentos/2024' 'C:/descargas' 'None' 'None'\n")
        return 0
    else:
        print_error(f"\nAbsolver los {total - passed} problema(s) antes de continuar.\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
