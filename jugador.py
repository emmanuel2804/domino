import random
from collections import Counter
from itertools import groupby
from random import shuffle


class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.cant_move = []
        self.fichas = []
        self.points = 0

    def jugar(self, extremo1, extremo2, *cant_move):
        # print('Jugando %s extremo1=%s extremo2=%s' %(self.nombre, extremo1, extremo2))
        no_llevo = True

        if extremo1 == -1 and extremo2 == -1:
            no_llevo = False
        else:
            for ficha in self.fichas:
                if ficha[0] == extremo1 or ficha[0] == extremo2 or \
                        ficha[1] == extremo1 or ficha[1] == extremo2:
                    no_llevo = False

        if no_llevo:
            # print('no llevo')
            if extremo1 == extremo2:
                self.cant_move.append(extremo1)
            else:
                self.cant_move.append(extremo1)
                self.cant_move.append(extremo2)
            return False, -1

        ficha, extremo = self.escoger_ficha(extremo1, extremo2, *cant_move)

        self.fichas.remove(ficha)
        return ficha, extremo

    def escoger_ficha(self, extremo1, extremo2, *cant_move) -> tuple:
        pass

    def repartiendo(self, ficha):
        self.fichas.append(ficha)

    def sum(self):
        result = 0
        for ficha in self.fichas:
            result += ficha[0] + ficha[1]

        return result


class BotaGorda(Jugador):
    def __init__(self, nombre):
        Jugador.__init__(self, nombre)

        self.nombre = 'BotaGorda_' + nombre

    def escoger_ficha(self, extremo1, extremo2, *cant_move):
        _sum = 0
        _ficha = 0

        for ficha in self.fichas:
            if ficha[0] == extremo1 or ficha[0] == extremo2 or \
                    ficha[1] == extremo1 or ficha[1] == extremo2 and \
                    ficha[0] + ficha[1] > _sum:
                _ficha = ficha
                _sum = ficha[0] + ficha[1]
            elif extremo1 == -1 and extremo2 == -1 and ficha[0] + ficha[
                1] > _sum:
                _ficha = ficha
                _sum = ficha[0] + ficha[1]

        return _ficha, -1


class Aleatorio(Jugador):
    def __init__(self, nombre):
        Jugador.__init__(self, nombre)

        self.nombre = 'Aleatorio_' + nombre

    def escoger_ficha(self, extremo1, extremo2, *cant_move):
        viables = []

        for ficha in self.fichas:
            if ficha[0] == extremo1 or ficha[0] == extremo2 or \
                    ficha[1] == extremo1 or ficha[1] == extremo2 or \
                    (extremo1 == -1 and extremo2 == -1):
                viables.append(ficha)

        for i in range(5):
            random.shuffle(viables)

        return viables.pop(0), -1


'''
Este jugador escoge de entre las posibles jugadas,
la ficha que, entre las dos partes de ella, tenga
mayor cantidad de fichas iguales en la mano
'''


class Cantidad(Jugador):
    def __init__(self, nombre):
        Jugador.__init__(self, nombre)

        self.nombre = 'Cantidad_' + nombre

    def escoger_ficha(self, extremo1, extremo2, *cant_move):
        viables = []

        for ficha in self.fichas:
            if ficha[0] == extremo1 or ficha[0] == extremo2 or \
                    ficha[1] == extremo1 or ficha[1] == extremo2 or \
                    (extremo1 == -1 and extremo2 == -1):
                viables.append(ficha)

        _ficha = 0
        _sum = 0

        for candidata in viables:
            temp_sum = 0
            for ficha in self.fichas:
                if candidata[0] == ficha[0] or candidata[0] == ficha[1] or \
                        candidata[1] == ficha[0] or candidata[1] == ficha[1]:
                    temp_sum += 1

            if temp_sum > _sum:
                _ficha = candidata
                _sum = temp_sum

        return _ficha, -1


class Cantidad2(Jugador):
    def __init__(self, nombre):
        super().__init__(nombre)

        self.nombre = 'Cantidad_' + nombre
        self.max_ficha = 0

    def escoger_ficha(self, extremo1, extremo2, *cant_move):
        viables = []

        for ficha in self.fichas:
            if ficha[0] == extremo1 or ficha[0] == extremo2 or \
                    ficha[1] == extremo1 or ficha[1] == extremo2 or \
                    (extremo1 == -1 and extremo2 == -1):
                viables.append(ficha)

        _ficha = 0
        _sum = 0

        for candidata in viables:
            temp_sum = 0
            cabeza1 = 0
            cabeza2 = 0
            _ficha_h = True
            for ficha in self.fichas:
                if candidata[0] == ficha[0] or candidata[0] == ficha[1]:
                    cabeza1 += 1
                if candidata[1] == ficha[0] or candidata[1] == ficha[1]:
                    cabeza2 += 1

            if cabeza2 > cabeza1:
                temp_sum += cabeza2
                _ficha_h = False
            else:
                temp_sum += cabeza1

            if temp_sum > _sum:
                _ficha = candidata
                _sum = temp_sum

        if _ficha[0]:
            return _ficha


class Cantidad3(Jugador):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.nombre = 'Cantidad_' + nombre

    def escoger_ficha(self, extremo1, extremo2, *cant_move):
        if extremo1 == -1 and extremo2 == -1:
            most_repeated, value = self.most_repeated(self.fichas)
            for f in most_repeated:
                if f[0] == f[1]:
                    return f, -1
            for f in self.fichas:
                if f[0] == f[1] and self.more_one(f[0]):
                    return f, -1
            for f in most_repeated:
                if f[0] == value and self.more_one(f[1]):
                    return f, -1
                elif f[1] == value and self.more_one(f[0]):
                    return f, -1
            shuffle(self.fichas)
            return self.fichas[0], -1

        viables = []

        for ficha in self.fichas:
            if ficha[0] == extremo1 or ficha[0] == extremo2 or \
                    ficha[1] == extremo1 or ficha[1] == extremo2 or \
                    (extremo1 == -1 and extremo2 == -1):
                viables.append(ficha)

        if extremo1 in cant_move:
            candidatas = [x for x in viables if
                          x[0] == extremo2 or x[1] == extremo2]
            if candidatas:
                subcandidatas = []
                flag = False
                for f in candidatas:
                    for n in cant_move:
                        if extremo1 in f or n in f:
                            flag = True
                            break
                    if flag:
                        subcandidatas.append(f)
                if subcandidatas:
                    return self.most_repeated(subcandidatas)[0][0], extremo2
                else:
                    return self.most_repeated(candidatas)[0][0], extremo2
        elif extremo2 in cant_move:
            candidatas = [x for x in viables if
                          x[0] == extremo1 or x[1] == extremo1]
            if candidatas:
                subcandidatas = []
                flag = False
                for f in candidatas:
                    for n in cant_move:
                        if extremo2 in f or n in f:
                            flag = True
                            break
                    if flag:
                        subcandidatas.append(f)
                if subcandidatas:
                    return self.most_repeated(subcandidatas)[0][0], extremo1
                else:
                    return self.most_repeated(candidatas)[0][0], extremo1
        most_repeated, value = self.most_repeated(self.fichas)

        for f in most_repeated:
            if (f[0] == value and f[1] == extremo1) or (
                    f[1] == value and f[0] == extremo1):
                return f, extremo1
            elif (f[0] == value and f[1] == extremo2) or (
                    f[1] == value and f[0] == extremo2):
                return f, extremo2
        return self.most_repeated(viables)[0][0], -1

    @classmethod
    def most_repeated(cls, fichas: list):
        h1 = []
        h2 = []
        for value in fichas:
            h1.append(value[0])
            h2.append(value[1])
        c_h1 = Counter(h1)
        c_h2 = Counter(h2)
        t = c_h1 + c_h2
        for x in fichas:
            if x[0] == x[1]:
                t -= Counter({x[0], 1})
        most_common = t.most_common(1)[0][0]
        result = []
        for x in fichas:
            if most_common in x:
                result.append(x)
        return result, most_common

    def more_one(self, param):
        h1 = []
        h2 = []
        for value in self.fichas:
            h1.append(value[0])
            h2.append(value[1])
        c_h1 = Counter(h1)
        c_h2 = Counter(h2)
        t = c_h1 + c_h2
        for x in self.fichas:
            if x[0] == x[1]:
                t -= Counter({x[0], 1})
        if t[param] > 1:
            return True
        return False
