no_students = 0
def generate_student_name():
    no_students += 1
    name = "Necunoscut_" + str(no_students)
    return name


class Elev:
    """ Clasa care memoreaza datele unui elev """
    def __init__(self, nume = "", sanatate = 90, inteligenta = 20, oboseala = 0, buna_dispozitie = 100):
        self.nume = generate_student_name() if nume == "" else nume
        self.sanatate = sanatate
        self.inteligenta = inteligenta
        self.oboseala = oboseala
        self.buna_dispozitie = buna_dispozitie
        #  Chestii necesare in rezolvarea cerintelor
        self.dictionar = {}
        self.activitate_curenta = None
        self.timp_executat_activ = 0
        self.stare_finala = 0  # 1 = absolvire scoala, 2 = spital


    def desfasoara_activitate(self, activitate_curenta, timp_executat_activ):
        self.activitate_curenta = activitate_curenta
        self.timp_executat_activ = timp_executat_activ
        self.dictionar[activitate_curenta] = 0



    def trece_ora(self):
        self.timp_executat_activ += 1
        self.dictionar[self.activitate_curenta] += 1
        if self.activitate_curenta.durata <= self.timp_executat_activ:
            return True
        else:
            return False


    def testeaza_final(self):
        if self.stare_finala != 0:
            return True
        return False


    def afiseaza_raport(self):
        print("Raport de activitate pentru " + str(nume) + ":")
        for activitate in self.dictionar:
            print(str(activitate.nume) + ": " + self.dictionar[activitate] + "h")




class Activitate:
    """ Clasa care memoreaza datele unei activitati """
    def __init__(self, nume, factor_sanatate, factor_inteligenta, factor_oboseala, factor_dispozitie, durata):
        self.nume = nume
        self.factor_sanatate = factor_sanatate
        self.factor_inteligenta = factor_inteligenta
        self.factor_oboseala = factor_oboseala
        self.factor_dispozitie = factor_dispozitie
        self.durata = durata


