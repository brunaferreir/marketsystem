class UserDomain:
    def __init__(self, name, email, password, cnpj, number):
        self.name = name
        self.email = email
        self.password = password
        self.cnpj = cnpj
        self.number = number

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "CNPJ": self.cnpj,
            "number": self.number
        }