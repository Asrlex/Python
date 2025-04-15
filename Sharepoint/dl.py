import pandas as pd
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
import configparser
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory


def generateContext():
    config = configparser.ConfigParser()
    config.read('config.ini')

    sp_url = config.get('SharePoint', 'url')
    username = config.get('SharePoint', 'username')
    password = config.get('SharePoint', 'password')

    if not sp_url or not username or not password:
        print('No se han encontrado las credenciales en el fichero config.ini')
        decision = input('¿Desea introducir los datos manualmente? (s/n): ')
        if decision == 's':
            sp_url = input('Introduce la URL de SharePoint: ')
            username = input('Introduce el nombre de usuario: ')
            password = input('Introduce la contraseña: ')
        else:
            print('Saliendo del programa...')
            exit()

    credentials = UserCredential(username, password)
    ctx = ClientContext(sp_url).with_credentials(credentials)

    return ctx

def read_excel_file():
    Tk().withdraw()
    excel_file = askopenfilename()

    df = pd.read_excel(excel_file, sheet_name=None)

    urls = []
    filenames = []
    for sheet_name, sheet_data in df.items():
        for index, row in sheet_data.iterrows():
            urls.append(row['Ruta_documento'])
            filenames.append(row['Nombre_documento'])

    return urls, filenames


def list_files(ctx, urls):
    try:
        for url in urls:
            files = ctx.web.get_folder_by_server_relative_url(url).files
            ctx.load(files)
            ctx.execute_query()

            for file in files:
                print("Nombre: {0}".format(file.properties['Name']))

    except Exception as e:
        print('Error: {0}'.format(e))


def download_files(ctx, urls, filenames, ):
    path = askdirectory(title='Select Folder where files will be downloaded')
    if not path:
        path = './'
    try:
        for i in range(len(urls)):
            url = urls[i]
            filename = filenames[i]
            file = ctx.web.get_file_by_server_relative_url(url + '/' + filename)
            ctx.load(file)
            ctx.execute_query()

            with open('{0}/{1}'.format(path, filename), 'wb') as local_file:
                file.download(local_file)
                print('[{0}] Archivo {1} descargado'.format(i+1, filename))

    except Exception as e:
        print('Error: {0}'.format(e))


if __name__ == '__main__':
    context = generateContext()

    urls, filenames = read_excel_file()

    seleccion_listar = input('¿Desea listar los archivos? (s/n): ')
    if seleccion_listar == 's':
        list_files(context, urls)

    seleccion_descargar = input('¿Desea descargar los archivos? (s/n): ')
    if seleccion_descargar == 's':
        path = input('Introduce la ruta donde se guardarán los archivos: (Por defecto: ./)')
        download_files(context, urls, filenames)
    