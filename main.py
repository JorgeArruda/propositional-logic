# -*- coding: utf-8 -*-
# Autor: Jorge de Arruda Martins


class Logica(object):
    def __init__(self, sentenca=''):
        self.sentenca = sentenca
        self.sentenca_f = ''
        self.num_var = 0
        self.variaveis = []
        self.tabela = []
        self.tipo = ''

        self.__get_n_var()
        self.__gerar_tabela()
        self.__resolver_sentenca()
        self.__resolver_tabela()
        self.tipo = self.verificar_tipo(self.tabela)

    def __get_n_var(self):
        self.variaveis = []
        for x in self.sentenca:
            if x.isalpha() and x.isupper() and not (x in self.variaveis):
                self.variaveis.append(x)
        self.num_var = len(self.variaveis)
        return self.variaveis

    def __gerar_tabela(self):
        self.tabela = []
        linha01 = self.variaveis + [self.sentenca]
        self.tabela = [linha01] + [[bool(True) for x in range(0, self.num_var + 1)]
                                   for i in range(0, 2 ** self.num_var)]
        for y in range(1, self.num_var + 1):
            padrao = 2 ** (self.num_var - y)
            valor = True
            for x in range(1, len(self.tabela) - (padrao - 1), padrao):
                for z in range(0, padrao):
                    self.tabela[x + z][y-1] = valor
                valor = not valor
        return self.tabela

    def __resolver_sentenca(self):
        if not ('->' in self.sentenca and '(' in self.sentenca):
            self.sentenca_f = self.se_entao(self.sentenca)
            print(self.sentenca_f)
            self.sentenca_f = self.ou_e_nao(self.sentenca_f)
            print(self.sentenca_f)
        else:
            self.sentenca_f = self.resolver_partes(self.sentenca)
            self.sentenca_f = self.se_entao(self.sentenca_f)
            self.sentenca_f = self.ou_e_nao(self.sentenca_f)
        return self.sentenca_f

    def __resolver_tabela(self):
        for x in range(1, len(self.tabela)):
            sentenca = self.sentenca_f
            for y in range(0, len(self.tabela[0]) - 1):
                sentenca = sentenca.replace(
                    self.tabela[0][y], str(self.tabela[x][y]))
            self.tabela[x][-1] = eval(sentenca)
        return self.tabela

    def verificar_tipo(self, tabela):
        tipo = ''
        resultado = []
        for x in range(1, len(tabela)):
            resultado.append(str(tabela[x][-1]))

        if eval(' and '.join(resultado)):
            tipo = 'Tautologia'
        elif not(eval(' or '.join(resultado))):
            tipo = 'Contradicao'
        else:
            tipo = 'Mista'
        return tipo

    def resolver_partes(self, sentenca, inicio=0):
        ok = False
        while ('(' in sentenca) and not ok:
            x = inicio
            nova_sentenca = ''
            while x < len(sentenca):
                if sentenca[x] == '(':
                    y = x + 1
                    while y < len(sentenca):
                        if sentenca[y] == ')':
                            parte00 = sentenca[:x]
                            parte01 = sentenca[x+1:y]
                            parte02 = sentenca[y+1:]

                            parte01 = self.se_entao(parte01)
                            parte01 = self.ou_e_nao(parte01)
                            ok = True
                            sentenca = parte00 + \
                                ' ( ' + parte01 + ' ) ' + parte02
                            break
                        elif sentenca[y] == '(':
                            nova_sentenca = sentenca[:y] + self.resolver_partes(
                                sentenca[y:], 0)
                            y = len(nova_sentenca) - 2
                            sentenca = nova_sentenca

                        y += 1
                    x = y
                x += 1
        return sentenca

    def ou_e_nao(self, sentenca):
        return sentenca.replace('v', 'or').replace('^', 'and').replace('~', ' not ')

    def se_entao(self, sentenca):
        while '->' in sentenca:
            indice = -1
            for x in range(len(sentenca)-1, -1, -1):
                if sentenca[x] == '>':
                    indice = x
                    break
            if indice == -1:
                break
            parte1, parte2 = (sentenca[0:x-1], sentenca[x+1:])
            sentenca = ' ~(' + parte1 + ') v ' + parte2 + ' '

        return sentenca

    def print_tabela(self):
        print('\n\tTabela Verdade - ' + self.tipo)
        for x in self.tabela[0][0:-1]:
            print(x, end='\t')
        print('\t', self.tabela[0][-1])
        for x in self.tabela[1:]:
            for y in x[0:-1]:
                print(y, end='\t')
            print('\t', x[-1])


if __name__ == '__main__':
    # sentenca = '(A -> B) -> (A -> B)'
    # sentenca = '(A -> B) -> (~B -> ~A)'
    sentenca = 'A -> B v C'
    # sentenca = '(A -> (B -> A) -> A)'

    logica = Logica(sentenca)
    print('\nSentenca: ', sentenca, '  N. de var: ', logica.num_var)
    logica.print_tabela()
