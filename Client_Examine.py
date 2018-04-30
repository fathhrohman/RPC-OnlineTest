import xmlrpc.client
import getpass
import os
import time
from prettytable import PrettyTable

SERVER_IP = 'localhost'
SERVER_PORT = '8000'
server = xmlrpc.client.ServerProxy(
    'http://{ip}:{port}'.format(ip=SERVER_IP, port=SERVER_PORT)
)
def menu_awal():
    os.system('clear')
    print("SELAMAT DATANG DI \nKUIS ONLINE BAHASA INGGRIS")
    print("MENU")
    print("1. Login User")
    print("2. Daftar User")
    print("0. Exit")
    return eval(input('Masukan pilihan : '))
def menu_user():
    os.system('cls')
    nama = server.get_np(usr_user)
    print('Log-in sebagai',nama)
    print('1. Mulai Kuis')
    print('2. Lihat Nilai')
    print('3. Lihat Jawaban')
    print('0. Log Out')
    return eval(input("Masukkan pilihan : "))

while True:
    if menu_awal() == 1:
        os.system('clear')
        usr_user = input('Username :')
        usr_pass = getpass.getpass('Password :')
        if server.login_user(usr_user, usr_pass) :
            while True :
                time.sleep(0.5)
                os.system('cls')
                if menu_user() == 1:
                     
                    if server.cek_peserta(usr_user):
                        print("Anda sudah melakukan kuis")
                        time.sleep(2)
                        break
                    else :
                        no = 1
                        print("Mulai Kuis")
                        print("Selesaikan dalam 10 menit")
                        soal = server.get_soal()
                        jawab = []
                        for i in soal :
                            if (time.time() > waktu_selesai):
                                print("Waktu habis")
                                time.sleep(3)
                                break
                            t = PrettyTable([no +"."+ i[1]])
                            t.align[i[1]] = 'l'
                            t.add_row(["a. %s"%i[3]])
                            t.add_row(["b. %s"%i[4]])
                            t.add_row(["c. %s"%i[5]])
                            t.add_row(["d. %s"%i[6]])
                            print(t)
                            # print(i[1])
                            # print("a. ",i[3])
                            # print("b. ",i[4])
                            # print("c. ",i[5])
                            # print("d. ",i[6])
                            no += 1
                            print()
                            while True:
                            jaw = input("masukkan jawaban(a/b/c/d) : ")
                            if (jaw == 'a') or (jaw == 'b') or (jaw == 'c') or (jaw == 'd'):
                                break
                            else :
                                print("jawaban tidak benar")
                            jawab.append(jaw)
                        nilai = 0

                        for i in range(len(jawab)) :
                        if (soal[i][2] == jawab[i]):
                            nilai += 5
                        print("Nilai anda adalah : ",nilai)
                        server.upload_nilai(nilai,usr_user,usr_pass)
                        print("Nilai anda sudah diupload")
                        for i in range((len(soal)-len(jawab))):
                            jawab.append('-')
                        server.upload_soal_peserta(soal,usr_user,jawab)
                elif menu_user() == 2:
                    os.system('cls')
                    nilai = server.lihat_nilai(usr_user)
                    if not nilai :
                        print(server.get_np(usr_user),", anda belum mulai kuis" )
                        time.sleep(2)
                    else :
                        print("Hai ",server.get_np(usr_user)," nilai anda adalah ",nilai)
                        print("Enter untuk lanjutkan")
                        input()
                elif menu_user() == 3:
                    os.system("cls")
                    jawaban = server.lihat_jawaban(usr_user)
                    if not jawaban :
                        print(server.get_np(usr_user),", anda belum mulai kuis" )
                        time.sleep(2)
                    else :
                        print("---Lihat Jawaban---")
                        t = PrettyTable(['Soal', 'Jawaban Anda', 'Kunci Jawaban'])
                        for isi in jawaban:
                            t.add_row(isi)
                        print(t)
                        print('Enter to lanjutkan')
                        input()
                elif menu_user() == 4:
                    valid_user == False
                    print("Log Out Successful")
                    time.sleep(0.5)
                    os.system('cls')
                    break
    elif menu_awal() == 2:
        os.system("cls")
        




    

