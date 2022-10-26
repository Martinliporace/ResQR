"""Definition of User class"""


class User:
    def __init__(self, id='', email='', password='', name='', document='', country='',
                 birthday='', sex='', pregnant='', blood='', diabetes='', diabetes_tipo='',
                 insulina='', marcapasos='', desfibrilador='', stent='', bypass='',
                 asma= '', epoc='', oxig='', vascu='', anaf='', edema='', services='', contacts='', pathologies='',
                 medication='', others=''):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.document = document
        self.country = country
        self.birthday = birthday
        self.sex = sex
        self.pregnant = pregnant
        self.blood = blood
        self.diabetes = diabetes
        self.diabetes_tipo = diabetes_tipo
        self.insulina = insulina
        self.marcapasos = marcapasos
        self.desfibrilador = desfibrilador
        self.stent = stent
        self.bypass = bypass
        self.vascu = vascu
        self.anaf = anaf
        self.edema = edema
        self.asma = asma
        self.epoc = epoc
        self.oxig = oxig
        self.services = services
        self.contacts = contacts
        self.pathologies = pathologies
        self.medication = medication
        self.others = others

    def toDBCollection(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'name': self.name,
            'document': self.document,
            'country': self.country,
            'birthday': self.birthday,
            'sex': self.sex,
            'pregnant': self.pregnant,
            'blood': self.blood,
            'diabetes': self.diabetes,
            'diabetes_tipo': self.diabetes_tipo,
            'insulina': self.insulina,
            'marcapasos': self.marcapasos,
            'desfibrilador': self.desfibrilador,
            'stent': self.stent,
            'bypass': self.bypass,
            'vascu' : self.vascu,
            'anaf' : self.anaf,
            'edema' : self.edema,
            'asma': self.asma,
            'epoc': self.epoc,
            'oxig': self.oxig,
            'services': self.services,
            'contacts': self.contacts,
            'pathologies': self.pathologies,
            'medication': self.medication,
            'others': self.others
        }
