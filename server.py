from xmlrpc.server import SimpleXMLRPCServer
import pymysql
import random
import time


IP = 'localhost'
PORT = 8000
PORT_UP = 8001
DB_SERVER = 'localhost'
DB_USER = 'root'
DB_PASS = ''
DB_NAME = 'sister'
server = SimpleXMLRPCServer((IP, PORT), allow_none=True)
print("Listening on port", PORT)
db = pymysql.connect(DB_SERVER, DB_USER, DB_PASS, DB_NAME)
cursor = db.cursor()


def login_admin(username, password):
    admin = []
    query = "select * from admin"
    cursor.execute(query)
    admin = cursor.fetchall()
    for i in range(len(admin)):
        if admin[i][0] == username and admin[i][1] == password:
            return True
    return False


def login_user(username, password):
    peserta = []
    query = "select * from peserta"
    cursor.execute(query)
    peserta = cursor.fetchall()
    for i in range(len(peserta)):
        if peserta[i][0] == username and peserta[i][1] == password:
            return True
    return False


def delete_soal():
    cursor.execute("delete from soal_materi")
    db.commit()
    return True

def upload_soal(data):
    isi = data.split(',')
    print(isi)
    query = "INSERT INTO `soal_materi` (`id_soal`, `soal`, `option_a`, \
    `option_b`, `option_c`, `option_d`, `kunci_jawaban`) \
    VALUES ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}', '{g}')".format(
        a=isi[0], b=isi[1], c=isi[2], d=isi[3], e=isi[4], f=isi[5], g=isi[6])
    print(query)
    cursor.execute(query)
    db.commit()
    return True


def lihat_soal():
    soal = []
    query = "select * from soal_materi"
    cursor.execute(query)
    soal = cursor.fetchall()
    return soal
def get_soal():
    query = "select * from soal_materi"
    cursor.execute(query)
    soal = cursor.fetchall()
    print('soal',soal)
    soal_peserta = []
    for i in range(0,20):
        soal_peserta.append(soal[random.randint(0,99)])
        soal_peserta[i].append("-")
    print('soal peserta0',soal_peserta[0])    
    return soal_peserta
  
def waktu_selesai():
    return time.time() + 600
  
def waktu_mulai():
    return time.time()
  
def upload_nilai(nilai,id_peserta):
    query = f"update peserta set 'nilai'={nilai} where 'id_peserta'='{id_peserta}'"
    cursor.execute(query)
    db.commit()
    
def lihat_jawaban(peserta):
    jawaban = []
    query = "select * from soal_peserta where id_peserta= %s "%peserta
    cursor.execute(query)
    jawaban = cursor.fetchall()
    return jawaban


def lihat_nilai(id):
    query = "select * from peserta where id_peserta= %s"%id
    cursor.execute(query)
    nilai = cursor.fetchone()
    return nilai[0]

def upload_soal_peserta(soal,id_peserta):
    for i in range(len(soal)):
        query = f"insert into soal_peserta values ('{soal[i][0]}_{id_peserta}','{soal[i][7]}','{id_peserta}','{soal[i][0]}')"
        cursor.execute(query)
        db.commit()

def cek_peserta(id_peserta):
    query = f"select * from soal_peserta where soal_peserta.id_peserta='{id_peserta}'"
    cursor.execute(query)
    kode_peserta = cursor.fetchall()
    return kode_peserta

def get_np(peserta):
    query = "select nama_peserta from peserta where id_peserta= %s "%peserta
    cursor.execute(query)
    tampung = cursor.fetchone()
    return tampung

def get_ad(admin):
    query = "select nama_admin from admin where id_admin= %s "%admin
    cursor.execute(query)
    tampung = cursor.fetchone()
    return tampung

def daftar(id,password):
    query = "INSERT INTO `peserta` (`id_peserta`, `nama_peserta`) \
    VALUES ('{a}', '{b}')".format(
        a=id, b=password)
    print(query)
    cursor.execute(query)
    db.commit()
    return True

server.register_function(login_admin, 'login_admin')
server.register_function(login_user, 'login_user')
server.register_function(upload_soal, 'upload_soal')
server.register_function(lihat_soal, 'lihat_soal')
server.register_function(delete_soal, 'delete_soal')
server.register_function(get_soal, 'get_soal')
server.register_function(waktu_selesai, 'waktu_selesai')
server.register_function(waktu_mulai, 'waktu_mulai')
server.register_function(upload_nilai, 'upload_nilai')
server.register_function(lihat_jawaban, 'lihat_jawaban')
server.register_function(lihat_nilai, 'lihat_nilai')
server.register_function(upload_soal_peserta, 'upload_soal_peserta')
server.register_function(cek_peserta, 'cek_peserta')
server.register_function(get_ad, 'get_ad')
server.register_function(get_np, 'get_np')
server.register_function(daftar, 'daftar')

server.serve_forever()
