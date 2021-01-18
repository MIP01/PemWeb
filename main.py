from flask import Flask, render_template
from flask import request, redirect, url_for
from mysql import connector
app = Flask(__name__)

db = connector.connect(
    host     = "localhost",
    user     = "root",
    passwd   = "",
    database = "db_list"
)

if db.is_connected():
    print("Berhasil Terhubung ke Database")
    

@app.route("/home/")
def web():
    cur = db.cursor()
    cur.execute("select * from tb_list")
    res = cur.fetchall()
    cur.close()
    return render_template('index.html', hasil=res)


@app.route('/tambah/')
def tambah_data():
    return render_template('tambah.html')

@app.route('/proses_tambah/', methods=['POST'])
def proses_tambah():
    no = request.form['uid']
    nama = request.form['nama']
    req = request.form['request']
    cur = db.cursor()
    cur.execute('INSERT INTO tb_list (uid, nama, request) VALUES (%s, %s, %s)', (no, nama, req))
    db.commit()
    return redirect(url_for('web'))

@app.route("/del/")
def admin():
    cur = db.cursor()
    cur.execute("select * from tb_list")
    res = cur.fetchall()
    cur.close()
    return render_template('del.html', hasil=res)

@app.route('/ubah/<uid>', methods=['GET'])
def ubah_data(uid):
    cur = db.cursor()
    cur.execute('select * from tb_list where uid=%s', (uid,))
    res = cur.fetchall()
    cur.close()
    return render_template('ubah.html', hasil=res)

@app.route('/proses_ubah/', methods=['POST'])
def proses_ubah():
    no_id = request.form['uid_ori']
    uid = request.form['uid']
    nama = request.form['nama']
    req = request.form['request']
    cur = db.cursor()
    sql = "UPDATE tb_list SET uid=%s, nama=%s, request=%s WHERE uid=%s"
    value = (uid, nama, req, no_id)
    cur.execute(sql, value)
    db.commit()
    return redirect(url_for('admin'))

@app.route('/hapus/<uid>', methods=['GET'])
def hapus_data(uid):
    cur = db.cursor()
    cur.execute('DELETE from tb_list where uid=%s', (uid,))
    db.commit()
    return redirect(url_for('admin'))


if __name__ == "__main__":
    app.run()
