"""Definition of User class"""


class User:
    def __init__(self, id='', email='', password='', name='', document='', country='',
                 birthday='', sex='', pregnant='', blood='', diabetes='', diabetes_tipo='',
                 insulina='', services='', contacts='', pathologies='', medication=''):
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
        self.services = services
        self.contacts = contacts
        self.pathologies = pathologies
        self.medication = medication

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
            'services': self.services,
            'contacts': self.contacts,
            'pathologies': self.pathologies,
            'medication': self.medication
        }
