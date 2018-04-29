import xmlrpc.client
import getpass
import os
import time

SERVER_IP = 'localhost'
SERVER_PORT = '8000'
server = xmlrpc.client.ServerProxy(
    'http://{ip}:{port}'.format(ip=SERVER_IP, port=SERVER_PORT)
)

def menu_awal():
    os.system('clear')
    print("SELAMAT DATANG DI \nKUIS ONLINE BAHASA INGGRIS")
    print("MENU ADMIN")
    print("1. Login")
    print("0. Keluar")
    return eval(input("Masukkan pilihan"))

def menu_admin():
    os.system('clear')
    print('1. Upload Soal')
    print('2. Lihat Soal')
    print('3. Delete Soal')
    print('0. Keluar')
    return eval(input("Masukkan pilihan"))
    

while True:
    if menu_awal() == 1:
        adm_user = input('Username :')
        adm_pass = getpass.getpass('Password :')
        if server.login_admin(adm_user, adm_pass) == True:
            print('Berhasil login sebagai admin')
            time.sleep(0.5)
            if menu_admin() == 1:
                nama_file = input('Masukan nama file (format.csv)')
                print('Uploading...')
                lines = [line.rstrip('\n') for line in open(nama_file)]
                for i in range(len(lines)):
                    server.upload_soal(lines[i])
                print('Upload berhasil.')
                time.sleep(0.5)
            if menu_admin() == 2:
                soal = server.lihat_soal()
                for i in range(len(soal)):
                    print(soal[i], '\n')
                input('Tekan enter / karakter apapun untuk lanjut')
            if menu_admin() == 3:
                print('Mendelete soal...')
                server.delete_soal()
                input('Tekan enter / karakter apapun untuk lanjut')
        else:
            print('Salah username / password')
            time.sleep(0.5)
            os.symtem('clear')
            

            
    elif (menu_awal() == 0):
        break