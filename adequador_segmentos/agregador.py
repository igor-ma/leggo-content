import string
import re
import os
import sys


def obtem_lista_termos(arqv):
        '''
                Lê de um arquivo processado pelo adequador os termos, que estão contidos entre os tokens de separação '%$#@!' e '!@#$%'
                Retorna a lista dos termos
        '''

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
                'inciso': 1,
                'alinea': 2,
                'paragrafo': 3
        }

        pasta = os.listdir(sys.argv[1])

        for arqv in pasta:
                termos_em_ordem = obtem_lista_termos(arqv)
                #print(termos_em_ordem)
                todos_conjuntos_termos = []
                
                
                i = 0
                if termos_em_ordem[i].split('_')[0] == 'artigo':
                        comecou_artigo = True
                else:  
                        comecou_artigo = False

                if comecou_artigo: #o fluxo muda dependendo se a enumeração começa com artigo ou não
                        conjunto_atual = [''] * TAMANHO_OPCOES_CONJUNTO #uma posição para cada termo possível
                        conjunto_atual[i] = termos_em_ordem[i]
                        i += 1

                        while i < len(termos_em_ordem):
                                
                                
                                termo_atual = termos_em_ordem[i].split('_')[0]
                                termo_anterior = termos_em_ordem[i - 1].split('_')[0]
                                if hierarquia[termo_atual] > hierarquia[termo_anterior]: #ou seja, se o termo atual estiver abaixo na hierarquia ou no mesmo nível do último termo
                                        conjunto_atual[hierarquia[termo_atual]] = termos_em_ordem[i]
                                else: #senão, isso indica o fim de um conjunto fechado de termos
                                        todos_conjuntos_termos.append(conjunto_atual) #salva o conjunto
                                        #print(len(todos_conjuntos_termos))
                                        #print((todos_conjuntos_termos))
                                        print(conjunto_atual)
                                        for j in range(hierarquia[termo_atual], len(conjunto_atual)): #limpa o vetor a partir da posição em que o termo atual entraria
                                                conjunto_atual[j] = ''
                                        conjunto_atual[hierarquia[termo_atual]] = termos_em_ordem[i] #deixa os termos acima na hierarquia ainda salvos, mas substitui o atual

                                i += 1
                '''

                i = 0
                if termos_em_ordem[i].split('_')[0] == 'artigo':
                        comecou_artigo = True
                else:  
                        comecou_artigo = False

                if comecou_artigo: #o fluxo muda dependendo se a enumeração começa com artigo ou não
                conjunto_atual = [''] * TAMANHO_OPCOES_CONJUNTO #uma posição para cada termo possível
                conjunto_atual[i] = termos_em_ordem[i]
                i += 1

                i = 0
                while i <= len(termos_em_ordem):
                        if termos_em_ordem[i].split('_')[0] == 'artigo':
                                conjunto_atual = [''] * TAMANHO_OPCOES_CONJUNTO
                                conjunto_atual[i] = termos_em_ordem[i]
                                pass
                        else: 
                                termo_atual = termos_em_ordem[i].split('_')[0]
                                termo_anterior = termos_em_ordem[i - 1].split('_')[0]
                                if hierarquia[termo_atual] > hierarquia[termo_anterior]: #ou seja, se o termo atual estiver abaixo na hierarquia ou no mesmo nível do último termo
                                        conjunto_atual[hierarquia[termo_atual]] = termos_em_ordem[i]
                                else: #senão, isso indica o fim de um conjunto fechado de termos
                                        todos_conjuntos_termos.append(conjunto_atual) #salva o conjunto
                                        for j in range(hierarquia[termo_atual], len(conjunto_atual)): #limpa o vetor a partir da posição em que o termo atual entraria
                                                conjunto_atual[j] = ''
                                        conjunto_atual[hierarquia[termo_atual]] = termos_em_ordem[i] #deixa os termos acima na hierarquia ainda salvos, mas substitui o atual

                        i += 1
                '''

        
                #for conj in todos_conjuntos_termos:
                        #print(conj)
                #print(termos_em_ordem)
                #print(len(termos_em_ordem))
                


        #print(todos_conjuntos_termos) #TODO: consertar bug (só fica salvo o último conjunto e várias repetições dele) 


if __name__ == "__main__":
        main()
