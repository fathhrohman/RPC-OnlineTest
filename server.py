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
    soal_peserta = []
    idx = [i for i in range(0,100)]
    urutan = random.sample(idx,20)
    for i in range(0,20):
        soal_peserta.append(soal[urutan[i]])
    print(soal_peserta)
    return soal_peserta
  
def waktu_selesai():
    return time.time() + 600
  
def waktu_mulai():
    return time.time()
  
def upload_nilai(nilai,id_peserta,pwd):
    query = f"update peserta set nilai={nilai} where peserta.id_peserta='{id_peserta}'"
    #query = f"insert into peserta values ('{id_peserta}','{pwd}',{nilai})"
    print(query)
    cursor.execute(query)
    db.commit()
    
def lihat_jawaban(peserta):
    jawaban = []
    query = "select * from soal_peserta where id_peserta= %s "%peserta
    cursor.execute(query)
    jawaban = cursor.fetchall()
    return jawaban

def get_np(peserta):
    query = "select nama_peserta from peserta where id_peserta= %s "%peserta
    cursor.execute(query)
    nama = cursor.fetchone()
    return nama[0]

def get_nama_admin(admin):
    query = "select nama_admin from admin where id_admin= %s "%admin
    cursor.execute(query)
    nama = cursor.fetchone()
    return nama[0]  

def upload_soal_peserta(soal,id_peserta,jawab):
    for i in range(len(soal)):
        id_soal_peserta = soal[i][0]+"_"+id_peserta
        query = f"insert into soal_peserta values ('{id_soal_peserta}','{jawab[i]}','{id_peserta}','{soal[i][0]}')"
        cursor.execute(query)
        db.commit()

def cek_peserta(id_peserta):
    query = "select * from soal_peserta"
    cursor.execute(query)
    kode_peserta = cursor.fetchall()
    for i in kode_peserta:
        if i[2] == id_peserta :
            return True
    return False



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
server.register_function(upload_soal_peserta, 'upload_soal_peserta')
server.register_function(cek_peserta, 'cek_peserta')
server.register_function(get_np, 'get_np')

server.serve_forever()