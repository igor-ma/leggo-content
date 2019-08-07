



def temNumero(palavra):
        return any(char.isdigit() for char in palavra)



def comecaComTermo(termos_de_interesse, palavra):
        i = 0
        for termo in termos_de_interesse: #para cada palavra confere se é um termo de interesse
                if palavra.startswith(termo):
                        return [True, i] #se começa com um dos termos de interesse, retorna verdadeiro e a posição
                i += 1

        return [False, -1] #senão, retorna falso e uma posição inválida



def main():
        #with open('emendas_em_blocos/7909365.pdf_teor.tags/bloco_1__B-SUP', 'r') as arquivo:
        with open('teste.txt', 'r') as arquivo:
                texto = arquivo.read()


        texto = ' '.join(texto.lower().split()) #deixando apenas um espaço em branco

        palavras = texto.split() #convertendo em lista de palavras
        print(palavras)

        
        termos_de_interesse = ['art', 'alin', 'alín', 'inc', 'par', '§'] #utilizado para verificar 
        dicionario_termos = { #utilizado para substituição de termos depois
                0: 'artigo', 
                1: 'alinea', 
                2: 'alinea', 
                3: 'inciso', 
                4: 'paragrafo', 
                5: 'paragrafo'
        }


        i = 0
        while True: #caminha por todas as palavras da lista
                if i == len(palavras) - 1:
                        break

                comeca_com_termo, posicao_na_lista = comecaComTermo(termos_de_interesse, palavras[i])
                if comeca_com_termo:
                        #se a palavra começa com um termo há duas opções: ou ela já possui um número/letra/algarismo romano de sua enumeração ou essa enumeração começa na próxima palavra. há a possibilidade de estar tudo junto, sem espaços. varre-se a palavra obtendo toda enumeração possível e, após o fim da palavra, continua a mesma procura nas próximas palavras até que se encontre uma palavra que possua um novo termo de interesse (ou até que o texto acabe).

                        #####################################################
                        # INÍCIO: avaliação no caso de Artigos e Parágrafos #
                        #####################################################
                        if posicao_na_lista in [0, 4]: #se estamos falando de parágrafo ou artigo então estamos buscando por números
                                termo_atual = dicionario_termos[posicao_na_lista]
                                numeros_na_enumeracao = [] #salva todos números da enumeração do termo atual

                                numero = ''
                                sem_append = True
                                for char in palavras[i]: #obtém os números na palavra atual
                                        if char.isdigit():
                                                numero += str(char)
                                                sem_append = True
                                        else: #exemplo: "art.35,57", nesse caso obteremos os dois separadamente
                                                if numero != '':
                                                        numeros_na_enumeracao.append(numero)
                                                        numero = ''
                                                        sem_append = False
                                if sem_append and numero != '':
                                        numeros_na_enumeracao.append(numero)
                                i += 1 #ao fim da avaliação da palavra atual passa para a próxima (até que se encontre um novo termo de interesse ou o fim do texto). essa redundância com o primeiro loop é devido ao fato de que alguns termos enumeram com números, outros com letras e outros com algarismos romanos. mantendo o controle da busca dentro da condição a avaliação fica mais simples.
                                comeca_com_termo, posicao_na_lista = comecaComTermo(termos_de_interesse, palavras[i])
                                while i < len(palavras) - 1 and not comeca_com_termo: #enquanto ainda for possivelmente um conteúdo da enumeração do termo atual TODO: melhorar isso, pois pode ser que estejamos pegando números que não estão em enumerações, estudar formas de consertar
                                        numero = ''
                                        sem_append = True
                                        for char in palavras[i]: #obtém os números na palavra atual
                                                if char.isdigit():
                                                        numero += str(char)
                                                        sem_append = True
                                                else: #exemplo: "art.35,57", nesse caso obteremos os dois separadamente
                                                        if numero != '':
                                                                numeros_na_enumeracao.append(numero)
                                                                numero = ''
                                                                sem_append = False
                                        if sem_append and numero != '':
                                                numeros_na_enumeracao.append(numero)
                                        i += 1
                                        comeca_com_termo, posicao_na_lista = comecaComTermo(termos_de_interesse, palavras[i])
                                i -= 1 #pode ter saído do loop ou por ter acabado o texto ou por ter encontrado um novo termo
                                pass
                        ##################################################
                        # FIM: avaliação no caso de Artigos e Parágrafos #
                        ##################################################
                        print(termo_atual)
                        print(numeros_na_enumeracao)

                        
                        ########################################
                        # INÍCIO: avaliação no caso de Incisos #
                        ########################################
                        if posicao_na_lista in [5]:

                        #####################################
                        # FIM: avaliação no caso de Incisos #
                        #####################################


                i += 1
                




'''
Transforma em minúsculo e faz split, obtendo lista de palavras
Enquanto houver palavras na lista
Se a palavra atual contiver um termo
        

'''







if __name__ == "__main__":
        main()
