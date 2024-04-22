import paramiko
import os
import csv
import pyodbc
import pandas as pd
import time
import random
from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


##########################################################################################################################################
# EXTRAI ARQUIVOS DO FTP
##########################################################################################################################################
# Configurações do SFTP
sftp_host = '179.190.19.180'
sftp_port = 4444
sftp_user = 'sftp.weopen'
sftp_pass = '5X7>usbv8:&{2>-Q@1TP'

# Conectar ao servidor SFTP
transport = paramiko.Transport((sftp_host, sftp_port))
transport.connect(username=sftp_user, password=sftp_pass)
sftp = paramiko.SFTPClient.from_transport(transport)

# Configurações do destino local
local_destination = r'\\192.168.60.14\\backup\\Kainos_Ativo_Vendas\\Via_Varejo\\Analitico_VIA'

# Data anterior
today = datetime.now()
one_days_ago = today - timedelta(days=1)


# Listar os arquivos no diretório FTP
remote_directory = '/WEOPEN/Via/'
files = sftp.listdir(remote_directory)
recent_files = [file for file in files if file.startswith("arquivo_via_analitico_") and sftp.stat(os.path.join(remote_directory, file)).st_mtime >= one_days_ago.timestamp()]

# Definindo a palavra-chave desejada
palavra_chave = 'novo'

# Baixar os arquivos localmente
for file in recent_files:
    # Verificando se a palavra-chave está presente no nome do arquivo
    if palavra_chave in file:
        remote_path = os.path.join(remote_directory, file)
        local_path = os.path.join(local_destination, file)
        sftp.get(remote_path, local_path)

# Fechar a conexão SFTP
sftp.close()
transport.close()


##########################################################################################################################################
# EXECUÇÃO PROCEDURE
##########################################################################################################################################

# Configurações do SQL Server
server = '192.168.60.14'
database = 'KAINOS_ATIVO_VENDAS'
username = 'integracao'
password = '@ntegr@c@o'

# Conectar ao banco de dados SQL Server
connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(connection_string)

# Executar uma consulta de inserção no banco de dados
cursor = conn.cursor()
cursor.execute("EXEC dbo.STP_ATUALIZA_ANALITICO_VIA")
conn.commit()

# Fechar a conexão com o banco de dados
conn.close()
