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
    os.system('cls')
    print("SELAMAT DATANG DI \nKUIS ONLINE BAHASA INGGRIS")
    print("MENU")
    print("1. Login Admin")
    print("2. Login User")
    print("3. Exit")


def menu_admin():
    os.system('cls')
    print('1. Upload Soal')
    print('2. Lihat Soal')
    print('3. Delete Soal')
    print('4. Nanti aja ah')


def menu_user():
    os.system('cls')
    print('1. Mulai Kuis')
    print('2. Lihat Nilai')
    print('3. Lihat Jawaban')


while True:
    menu_awal()
    pilihan = eval(input('Masukan pilihan :'))
    if pilihan == 1:
        os.system('cls')
        adm_user = input('Username :')
        adm_pass = getpass.getpass('Password :')
        valid_admin = server.login_admin(adm_user, adm_pass)
        if valid_admin:
            print('Berhasil login sebagai admin')
            time.sleep(0.5)
            menu_admin()
            pilihan = eval(input('Masukkan pilihan :'))
            if pilihan == 1:
                nama_file = input('Masukkan nama file (format .csv)')
                print('uploading...')
                lines = [line.rstrip('\n') for line in open(nama_file)]
                for i in range(len(lines)):
                    server.upload_soal(lines[i])
                menu_admin()
                pilihan = eval(input('Masukkan pilihan :'))
            elif pilihan == 2:
                soal = server.lihat_soal()
                for i in range(len(soal)):
                    print(soal[i], '\n')
                print('setelah soal')
                time.sleep(5)
            elif pilihan == 3:
                server.delete_soal()


        else:
            print('Salah password/username')
            time.sleep(0.5)
            os.system('cls')

    if pilihan == 2:
        
        os.system('cls')
        usr_user = input('Username :')
        usr_pass = getpass.getpass('Password :')
        valid_user = server.login_user(usr_user, usr_pass)
        if valid_user:
            print('Berhasil login sebagai user')
            time.sleep(0.5)
            os.system('cls')
            menu_user()
            pilihan = input("Masukkan pilihan : ")
            if pilihan == "1":
                peserta = server.cek_peserta(usr_user)
                if peserta:
                    print("Anda sudah melakukan kuis")
                    time.sleep(2)
                    # break
                else:
                    soal = []
                    print("mulai kuis")
                    print("selesaikan dalam 10 menit")
                    soal = server.get_soal()
                    waktu_mulai = server.waktu_mulai()
                    waktu_selesai = server.waktu_selesai()
                    jawab = []
                    for i in soal :
                        if (time.time() > waktu_selesai):
                            print("waktu habis")
                            time.sleep(3)
                            break                    
                        print(i[1])
                        print("a. ",i[3])
                        print("b. ",i[4])
                        print("c. ",i[5])
                        print("d. ",i[6])
                        while True:
                            jaw = input("masukkan jawaban(a/b/c/d) : ")
                            if (jaw == 'a') or (jaw == 'b') or (jaw == 'c') or (jaw == 'd'):
                                break
                            else :
                                print("jawaban tidak benar")
                        jawab.append(jaw)
                    nilai = 0
                    print(jawab)
                    for i in range(len(jawab)) :
                        if (soal[i][2] == jawab[i]):
                            nilai += 5
                    print("Nilai KAMYU adalah : ",nilai)
                    server.upload_nilai(nilai,usr_user,usr_pass)
                    print("Nilai KAMYU sudah diupload")
                    for i in range((len(soal)-len(jawab))):
                        jawab.append('-')
                    server.upload_soal_peserta(soal,usr_user,jawab)
            elif pilihan == "2":
                print("lihat nilai")
            elif pilihan == "3":
                break
        else:
            print('Salah password/username')
            time.sleep(0.5)
            os.system('cls')
