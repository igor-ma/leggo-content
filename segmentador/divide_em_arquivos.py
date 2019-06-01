'''
	Pra cada arquivo de emenda
		Cria uma pasta com o nome dele
		Pra cada bloco (função separa_em_blocos)
			Cria um arquivo contendo somente esse bloco e salva ele nessa pasta
'''
import os



def leitura_de_dados(arquivo_de_entrada):
	'''
	Lê o arquivo com os dados o qual contém, em cada linha, um par palavra-tag.
	Retorna uma lista de pares palavra-tag.
	'''

	with open(arquivo_de_entrada, 'r') as arquivo:
		linhas = arquivo.readlines()

	pares_palavra_tag = []
	for linha in linhas:
		tupla = tuple(linha.split())
		#print(tupla)
		pares_palavra_tag.append(tupla)

	return pares_palavra_tag


def separa_em_blocos(pares_palavra_tag):
	'''
	Separa o documento em diferentes blocos/segmentos.
	Retorna uma lista de documentos/blocos.
	'''

	documentos = [] 
	documento = []
	for i in range(len(pares_palavra_tag)):
		documento.append(pares_palavra_tag[i])
		if('B-' in pares_palavra_tag[i][1] and len(documento) > 1): #se encontrar um Begin (depois de uma sequência de Outs ou NÃO logo após um End, len(documento) > 1) 
			aux = documento.pop()
			documentos.append(documento)
			documento = []
			documento.append(aux)
		else:
			if('E-' in pares_palavra_tag[i][1]): #se encontrar um End
				documentos.append(documento)
				documento = []

	return documentos




def main():
	'''
	Função principal
	'''

	caminho = "/local_para_salvar/emendas_em_blocos/"

	for arquivo in os.listdir('tagFiles/'): #diretório com arquivos de treino e teste
		pares_palavra_tag_arquivo = leitura_de_dados('tagFiles/' + arquivo)
		blocos_arquivo = separa_em_blocos(pares_palavra_tag_arquivo)
		os.mkdir(caminho + arquivo)

		i = 0
		for bloco in blocos_arquivo:
			with open("emendas_em_blocos/" + arquivo + '/bloco_' + str(i) + '__' + bloco[0][1] , 'w') as arq:
				arq.write(' '.join(item[0] for item in bloco))
			i += 1

	


if __name__ == "__main__":
	main()
