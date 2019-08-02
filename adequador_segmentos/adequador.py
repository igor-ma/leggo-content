



def temNumero(palavra):
        return any(char.isdigit() for char in palavra)


def main():
        with open('emendas_em_blocos/7909365.pdf_teor.tags/bloco_1__B-SUP', 'r') as arquivo:
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
                plv = palavras[i]
                indice_termo = 0
                for termo in termos_de_interesse:
                        if plv.startswith(termo):
                                print('*** ' + plv + ' ***\n')
                                
                                if temNumero(plv): #caso o número esteja junto
                                        numero = ''
                                        for char in plv:
                                                if char.isdigit():
                                                        numero += str(char)
                                        print(numero)
                                        
                                        termo_atual = dicionario_termos[int(numero)] + '_' + numero
                                        print(termo_atual)

                                else: #senão, avalia as palavras seguintes
                                        i += 1
                                        
                        indice_termo += 1


                                
        


if __name__ == "__main__":
        main()
