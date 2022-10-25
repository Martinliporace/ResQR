from flask import Flask, render_template, request, redirect, session, flash, Response, url_for, jsonify
import database as dbase
from user import User
from qr_generator import create_qr
import bcrypt
import uuid

app = Flask(__name__)
db = dbase.dbConnection()
app.secret_key = b'\xaa\xe4V}y~\x84G\xb5\x95\xa0\xe0\x96\xca\xa7\xe7'


# Definición de rutas


# Protegida. Solo pueden entrar los que han iniciado sesión


@app.route("/user_form")
def user_form():

    return render_template("user_form.html")


@app.route('/adduser', methods=['POST'])
def addUser():
    users = db['users']
    correo = session['usuario']
    user = users.find_one({'email': correo})
    id = user["id"]
    email = user["email"]
    password = user["password"]
    serviceList = ['emergency', 'mutualist']
    contactsList = ['contact1', 'contact2']
    pathologiesList = ['alzheimer', 'epilepsia', 'neuropatias',                                                 'traumatismos', 'tumor_cer', 'infeccion_card',
                       'miocardiopatia', 'valvulas', 'operacion_card', 'paro',
                       'bypass', 'cancer_pulmonar', 'asma', 'epoc',
                       'oxig', 'contactantes', 'inhal', 'ingest', 'vascu',
                       'anaf', 'edema']

    name = request.form['name-input']
    document = request.form['document']
    country = request.form['pais']
    birthday = request.form['BirthDate']
    sex = request.form['sexo']
    pregnant = request.form['pregnant']
    blood = request.form['sangre']
    diabetes = request.form['diabetes']
    diabetes_tipo = request.form['diabetes_tipo']
    insulina = request.form['insulina']
    pathologies = {}
    medicationDict = {}
    servicesDict = {}
    contacts = []

    for service in serviceList:
        checkService = request.form.getlist(service)

        if len(checkService) > 1:
            servicesDict[checkService[0]] = checkService[1]

    for contact in contactsList:
        checkContacts = request.form.getlist(contact)
        if len(checkContacts) > 1:
            contacts.append(checkContacts[0])
            contacts.append(checkContacts[1])
            contacts.append(checkContacts[2])

    for pathology in pathologiesList:
        checkPathologies = request.form.getlist(pathology)

        if len(checkPathologies) > 1:
            pathologies[checkPathologies[0]] = checkPathologies[1]
    for x in range(11):
        checkMedication = request.form.getlist("medicacion" + str(x))

        if len(checkMedication) > 1:
            medicationDict[checkMedication[0]] = checkMedication[1]
    medication = []
    for key, value in medicationDict.items():
        if value != '':
            medication.append(key+' :'+value+'\n')
    services = []
    for key, value in servicesDict.items():
        if value != '':
            services.append(key+' :'+value+'\n')


    if name and document:
        user = User(id, email, password, name, document, country,
                 birthday, sex, pregnant, blood, diabetes, diabetes_tipo,
                 insulina, services, contacts, pathologies, medication)
        users.update_one({'id': id},
                         {'$set': {'id' : id,
                                   'email' : email,
                                   'password' : password,
                                   'name' : name,
                                   'document' : document,
                                   'country' : country,
                                   'birthday' : birthday,
                                   'sex' : sex,
                                   'pregnant' : pregnant,
                                   'blood' : blood,
                                   'diabetes' : diabetes,
                                   'diabetes_tipo' : diabetes_tipo,
                                   'insulina' : insulina,
                                   'services' : services,
                                   'contacts' : contacts,
                                   'pathologies' : pathologies,
                                   'medication' : medication,
                                   }})

        create_qr(data=id)
        return (redirect(url_for('qr_create', user_id=id)))
    else:
        return 'notFound()'

# QR generate
@app.route('/qr/<string:user_id>')
def qr_create(user_id):
    users = db['users']
    id = user_id
    userReceived = users.find({"id": user_id})
    return render_template("download-qr.html", users=userReceived)


# Method Put
@app.route('/edit/<string:user_id>', methods=['POST'])
def edit(user_id):
    users = db['users']
    id = user_id
    name = request.form['name']
    document = request.form['document']
    mutualism = request.form['mutualism']
    tel_mutualism = request.form['tel_mutualism']
    emergency = request.form['emergency']
    tel_emergency = request.form['tel_emergency']
    contact = request.form['contact']
    tel_contact = request.form['tel_contact']
    alergies = request.form['alergies']
    pathologies = request.form['pathologies']
    medication = request.form['medication']

    if name and document:
        users.update_one({'id': user_id},
                         {'$set': {'id': id,
                                   'name': name,
                                   'document': document,
                                   'mutualism': mutualism,
                                   'tel_mutualism': tel_mutualism,
                                   'emergency': emergency,
                                   'tel_emergency': tel_emergency,
                                   'contact': contact,
                                   'tel_contact': tel_contact,
                                   'alergies': alergies,
                                   'pathologies': pathologies,
                                   'medication': medication
                                   }})
        response = jsonify({'message': 'Usuario ' + name +
                            ' actualizado correctamente'})
        return redirect(url_for('control_panel', user_id=id))
    else:
        return notFound()


# Method Get
@app.route('/user_profile/<string:user_id>', methods=['GET'])
def control_panel(user_id):
    users = db['users']
    id = user_id
    userReceived = users.find({"id": user_id})
    return render_template('user_panel.html', users=userReceived)

# Method delete
@app.route('/delete/<string:user_id>')
def delete(user_id):
    users = db['users']
    users.delete_one({'id': user_id})
    return redirect(url_for('register'))


# Formulario para iniciar sesión


@app.route("/login")
def login():
    return render_template("login.html")

# Manejar login


@app.route("/hacer_login", methods=["POST"])
def hacer_login():
    users = db['users']

    correo = request.form["loginName"]
    palabra_secreta = request.form["loginPassword"]
    user = users.find_one({'email': correo})

    if user:
        bytes = palabra_secreta.encode('utf-8')
        salt = bcrypt.gensalt()
        id = user['id']
        password = user['password']
        print('email ', user['email'], 'pass ', user['password'])
        if bcrypt.checkpw(bytes, password):
            session["usuario"] = correo
            print('session', session['usuario'])
            return redirect(url_for('control_panel', user_id=id))

        else:
            # Si NO coincide, lo regresamos
            flash("Correo o contraseña incorrectos")
            return redirect("/login")
    else:
        return redirect("/register")




@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/newregister", methods=['POST'])
def newRegister():
    users = db['users']
    id = str(uuid.uuid4())
    correo = request.form["registerEmail"]
    password = request.form["registerPassword"]
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    print(hash)
    print(id, correo)
    user = users.find_one({'email': correo})
    if user:
        return (redirect('/login'))
    if correo and password:
        user = User(id, correo, hash)
        users.insert_one(user.toDBCollection())
    response = jsonify({'id': id,
                        'correo': correo
                        })
    session["usuario"] = correo
    return (redirect(url_for('user_form')))


# Cerrar sesión
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/login")


# Middleware
@app.before_request
def antes_de_cada_peticion():
    ruta = request.path
    # Si no ha iniciado sesión y no quiere ir a algo relacionado al login, lo redireccionamos al login
    if not 'usuario' in session and ruta != "/login" and ruta != "/hacer_login" and ruta != "/logout" and ruta != "/register"  and ruta != "/newregister"and not ruta.startswith("/static"):
        flash("Inicia sesión para continuar")
        return redirect("/login")
    # Si ya ha iniciado, no hacemos nada, es decir lo dejamos pasar

@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

# Iniciar el servidor
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
