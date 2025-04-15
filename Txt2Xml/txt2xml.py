import tkinter as tk
from tkinter import filedialog
import os
import json
import xml.etree.ElementTree as ET
import py7zr
import time


def txt2xml():
    # Seleccionar circuito y tipo de exportación
    circuito = input('Seleccione circuito (físico/correo): \n')
    etiquetas = None

    # Seleccionar si se quiere convertir un archivo individual o una carpeta comprimida
    seleccion = None
    while seleccion not in ['A', 'C', 'CC']:
        seleccion = input('¿Archivo de texto individual, carpeta comprimida o carpeta completa? (A/C/CC): \n')
        seleccion = seleccion.upper()
        if seleccion not in ['A', 'C', 'CC']:
            print('Opción no válida')

    if seleccion == 'A':
        # Seleccionar fichero de texto
        root = tk.Tk()
        root.withdraw()
        path_archivo = filedialog.askopenfilename()
        extraccion = input("Tipo de extracción (01, 05, 50...): \n")
        extraccion = f'exportacion_{extraccion}'
        etiquetas = getEtiquetas(circuito, extraccion)
        procesar_archivo(etiquetas, path_archivo)
    elif seleccion == 'C':
        # Seleccionar carpeta comprimida
        root = tk.Tk()
        root.withdraw()
        path_archivo = filedialog.askopenfilename()
        etiquetas = getEtiquetas(circuito, os.path.basename(path_archivo))
        procesar_carpeta(etiquetas, path_archivo)
    elif seleccion == 'CC':
        procesar_carpeta_completa(circuito)
    else:
        input('Opción no válida')


def getEtiquetas(circuito, archivo, extraccion=None):
    if extraccion is not None:
        tipo = f'exportacion_{extraccion}'
    else:
        # Extraer el tipo de exportación del nombre del archivo
        tipo = archivo.split('-')[-1].split('.')[0]
        tipo = f'exportacion_{tipo}'
    
    with open('etiquetas.json', 'r') as f:
        etiquetas = json.load(f)

    if etiquetas[circuito][tipo] is None:
        print('No se han definido etiquetas para este tipo de exportación')

    return etiquetas[circuito][tipo]


def procesar_archivo(etiquetas, path_archivo):
    # Leer campos del fichero, quitar comillas y espacios, y ordenar en array
    # El encoding utf-8 es necesario para leer correctamente los caracteres especiales
    with open(path_archivo, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
    
    lineas = [line.replace('"', '') for line in lineas]
    campos = lineas[0].split(',')
    campos = [field.strip() for field in campos]

    # Definir nombre del fichero XML de salida. Si ya existe, se añade un número al final
    path_xml = os.path.splitext(path_archivo)[0] + '.xml'
    i = 1    
    while os.path.isfile(path_xml):
        path_xml = os.path.splitext(path_archivo)[0] + f' ({i}).xml'
        i += 1
    root = ET.Element('raiz')

    # Escribir campos en XML con las etiquetas apropiadas, si existen
    for campo in campos:
        if etiquetas[campos.index(campo)] is not None:
            ET.SubElement(root, etiquetas[campos.index(campo)]).text = campo
        else:
            ET.SubElement(root, 'campo').text = campo

    # Guardar XML
    tree = ET.ElementTree(root)
    tree.write(path_xml)

    print(f'Guardado como {os.path.basename(path_xml)}')


def procesar_carpeta(etiquetas, path_archivo):
    # Descomprimir carpeta .7z en una carpeta temporal
    with py7zr.SevenZipFile(path_archivo, mode='r') as z:
        tmp_folder = os.path.join(os.path.dirname(path_archivo), 'tmp')
        os.makedirs(tmp_folder, exist_ok=True)
        z.extractall(path=tmp_folder)
    
    # Recorrer ficheros de la carpeta temporal y convertirlos a XML
    carpeta_descomprimida = tmp_folder + '/' + path_archivo.split('/')[-1].split('.')[0]
    if not os.path.exists(carpeta_descomprimida):
        carpeta_descomprimida = tmp_folder
    for archivo in os.listdir(carpeta_descomprimida):
        if archivo.endswith('.txt'):
            print(f'Procesando {archivo}...')
            path = os.path.join(carpeta_descomprimida, archivo)
            procesar_archivo(etiquetas, path)

    # Borrar archivos txt
    for archivo in os.listdir(carpeta_descomprimida):
        if archivo.endswith('.txt'):
            os.remove(os.path.join(carpeta_descomprimida, archivo))

    # Comprimir archivos XML e imágenes en una carpeta .7z
    nombre_nuevo = path_archivo.split('.')[0] + '_xml.7z'
    with py7zr.SevenZipFile(nombre_nuevo, 'w') as z:
        z.writeall(carpeta_descomprimida, '/')
    print(f'Guardado como {nombre_nuevo}')
    
    # Borrar carpeta temporal y sus contenidos
    for archivo in os.listdir(carpeta_descomprimida):
        os.remove(os.path.join(carpeta_descomprimida, archivo))
    os.rmdir(carpeta_descomprimida)
    if tmp_folder != carpeta_descomprimida:
        os.rmdir(tmp_folder)


def procesar_carpeta_completa(circuito):
    # Seleccionar carpeta
    root = tk.Tk()
    root.withdraw()
    path_carpeta = filedialog.askdirectory()

    # Recorrer ficheros comprimidos de la carpeta y procesarlos
    for archivo in os.listdir(path_carpeta):
        if archivo.endswith('.7z') and archivo.endswith('_xml.7z') == False:
            print(f'Convirtiendo {archivo}...')
            path_archivo = os.path.join(path_carpeta, archivo)
            etiquetas = getEtiquetas(circuito, archivo)
            procesar_carpeta(etiquetas, path_archivo)


if __name__ == '__main__':
    t_inicio = time.time()
    txt2xml()
    t_fin = time.time()
    elapsed_time = t_fin - t_inicio
    print(f"\nTiempo de ejecución: {elapsed_time}s")
