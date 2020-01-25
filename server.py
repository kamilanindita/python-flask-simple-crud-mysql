from flask import Flask,render_template, request, url_for, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_DB"]="website_crud"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql = MySQL(app)



@app.route("/")
def index():
    title="Index"
    return render_template("index.html",title=title)
    
@app.route("/buku")
def buku():
    title="Buku"
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM buku")
    data = cur.fetchall()
    cur.close()
    return render_template("buku.html",data=data,title=title)
    
@app.route("/buku/add")
def add():
    title="Tambah"
    return render_template("tambah.html",title=title)
   
@app.route("/buku/tambah/save",methods=["POST"])
def save():
    penulis=request.form["penulis"]
    judul=request.form["judul"]
    kota=request.form["kota"]
    penerbit=request.form["penerbit"]
    tahun=request.form["tahun"]
    
    data=(penulis,judul,kota,penerbit,tahun)
    query="INSERT INTO buku (penulis,judul,kota,penerbit,tahun) VALUES (%s,%s,%s,%s,%s)"
    cur = mysql.connection.cursor()
    cur.execute(query,data)
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('buku'))
  

@app.route("/buku/edit/<id>")
def edit(id):
    title="Edit"
    query="SELECT * FROM buku WHERE id={}".format(id)
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return render_template("edit.html",data=data,title=title)


   
@app.route("/buku/update/<id>",methods=["POST"])
def update(id):
    penulis=request.form["penulis"]
    judul=request.form["judul"]
    kota=request.form["kota"]
    penerbit=request.form["penerbit"]
    tahun=request.form["tahun"]
    
    data_update=(penulis,judul,kota,penerbit,tahun,id)
    query="UPDATE buku SET penulis = %s, judul = %s, kota = %s, penerbit = %s, tahun = %s WHERE id = %s"
    cur = mysql.connection.cursor()
    cur.execute(query,data_update)
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('buku'))

@app.route("/buku/delete/<id>")
def delete(id):
    query="DELETE FROM buku WHERE id={}".format(id)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('buku'))
    
if __name__ == '__main__':
    app.run(debug=True)
