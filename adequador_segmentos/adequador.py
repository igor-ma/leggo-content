



def temNumero(palavra):
        return any(char.isdigit() for char in palavra)


def main():
        #with open('emendas_em_blocos/7909365.pdf_teor.tags/bloco_1__B-SUP', 'r') as arquivo:
        with open('teste.txt', 'r') as arquivo:
                texto = arquivo.read()


        texto = ' '.join(texto.lower().split()) #deixando apenas um espaço em branco

        palavras = texto.split() #convertendo em lista de palavras


        print(palavras)
        termos_de_interesse = ['art', 'alin', 'alín', 'inc', 'par', '§']
        dicionario_termos = {
                0: 'artigo', 
                1: 'alinea', 
                2: 'alinea', 
                3: 'inciso', 
                4: 'paragrafo', 
                5: 'paragrafo'
        }

        #for i in range(len(palavras)):
        i = 0
        while True:
                if i == len(palavras) - 1:
                        break
                plv = palavras[i]
                indice_termo = 0
                fim_termo = False
                for termo in termos_de_interesse: #para cada palavra confere se é um termo de interesse
                        if plv.startswith(termo): #se for, faz algumas operações sobre as próximas palavras
                                print('*** ' + plv + ' ***\n')
                                
                                if temNumero(plv): #caso o número esteja junto
                                        numero = ''
                                        for char in plv:
                                                if char.isdigit():
                                                        numero += str(char)
                                        print(numero)
                                        
                                        termo_atual = dicionario_termos[int(indice_termo)] + '_' + numero
                                        print(termo_atual)
                                        break

                                else: #se não houver número é preciso avaliar as próximas palavras dependendo da que possui um termo de interesse, até que acabe uma enumeração ou de números (artigos e parágrafos) ou de letras (alíneas) ou de algarismos romanos (incisos)
                                        if dicionario_termos[int(indice_termo)] in ['artigo', 'paragrafo']:
                                                lista_numeros = []
                                                while True:
                                                        print(palavras[i])
                                                        i += 1
                                                        if i == len(palavras) - 1 or palavras[i] in dicionario_termos.values(): #se encontrou um novo termo, então a enumeração referente ao termo atual já acabou (tem de ser melhorado, utilizar pontuação e ligações como 'e' e 'até' para identificar o fim também)
                                                                #TODO: lista com todos termos, verificar também usando startswith com todos inícios de termo possíveis assim como feito no início do segundo loop
                                                                fim_termo = True
                                                                break
                                                        numero = ''
                                                        for char in palavras[i]:
                                                                if char.isdigit():
                                                                        numero += str(char)
                                                        if numero != '':
                                                                lista_numeros.append(numero)
                        if fim_termo:
                                print(palavras[i])
                                print(lista_numeros)
                                i -= 1
                                break
                        indice_termo += 1
                i += 1

                                
#caminhar até encontrar o próximo termo ou até ter acabado o texto (?)




'''
Transforma em minúsculo e faz split, obtendo lista de palavras
Enquanto houver palavras na lista
Se a palavra atual contiver um termo
        

'''







if __name__ == "__main__":
        main()
