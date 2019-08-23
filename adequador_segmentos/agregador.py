import string
import re
import os
import sys


def obtem_lista_termos(arqv):
        termos_em_ordem = []
        with open(sys.argv[1] + '/' + arqv, 'r') as arquivo:
                texto = arquivo.readlines()
                adicionar = False
                for linha in texto:
                        linha = linha.replace('\n', '')
                        if linha == '%$#@!':
                                adicionar = False

                        if adicionar and linha != '':
                                termos_em_ordem.append(linha)

                        if linha == '!@#$%':
                                adicionar = True
        
        return termos_em_ordem



def main():
        TAMANHO_OPCOES_CONJUNTO = 4

        hierarquia = {
                'artigo': 0,
                'paragrafo': 1,
                'inciso': 2,
                'alinea': 3
        }

        pasta = os.listdir(sys.argv[1])

        for arqv in pasta:
                termos_em_ordem = obtem_lista_termos(arqv)
                todos_conjuntos_termos = []
                
                
                i = 0
                if termos_em_ordem[i].split('_')[0] == 'artigo':
                        comecou_artigo = True
                else:  
                        comecou_artigo = False

                if comecou_artigo: #o fluxo muda dependendo se a enumeração começa com artigo ou não

                        #...

                        conjunto_atual = [''] * TAMANHO_OPCOES_CONJUNTO #uma posição para cada termo possível
                        conjunto_atual[i] = termos_em_ordem[i]
                        i += 1

                        termo_atual = termos_em_ordem[i].split('_')[0]
                        termo_anterior = termos_em_ordem[i - ].split('_')[0]
                        if hierarquia[termo_atual] > hierarquia[termo_anterior]: #ou seja, se o termo atual estiver abaixo na hierarquia ou no mesmo nível do último termo
                                conjunto_atual[hierarquia[termo_atual]] = termos_em_ordem[i]
                        else:
                                todos_conjuntos_termos.append(conjunto_atual)
                                for j in range(hierarquia[termo_atual], len(conjunto_atual)):
                                        conjunto_atual[j] = ''



                print(termos_em_ordem)
                print(len(termos_em_ordem))
                





if __name__ == "__main__":
        main()
