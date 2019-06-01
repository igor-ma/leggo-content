'''
Agora com as emendas segmentadas devemos extrair informação do texto para saber à quais pontos da PL a emenda se refere (1), inserir isso no local certo da PL e comparar as distâncias com as distâncias originais, sem emendas (2)
Para:
	(1) mini-compilador
	(2) pré-processamento com NER, substituindo nomes de pessoas, locais e tempo
'''


import re
import os
import pycrfsuite
import pickle
import numpy as np



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



def conta_quantos_blocos_tem_esse_arquivo(pares_palavra_tag):
	'''
	Pra cada arquivo conta quantos blocos existem
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

	return len(documentos)
	


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



def criador_de_features(documento, posicao_do_par, pos_tags_documento):
	'''
	Dado um documento/bloco e a posição do par palavra-tag atual obtém as features desse par.
	Retorna uma lista de features.
	'''
	
	palavra = documento[posicao_do_par][0]
	tag = documento[posicao_do_par][1]
	pos_tag = pos_tags_documento[posicao_do_par][1]



	features = [ 
		'bias',
		'palavra_minusculo=' + palavra.lower(),
		'esta_em_maiusculo=%s' % palavra.isupper(),
		'e_titulo=%s' % palavra.istitle(),
		'e_digito=%s' % palavra.isdigit(),
		'pos_tag=' + pos_tag
	] #features genéricas, servem para qualquer palavra no documento/bloco, independentemente de sua posição
	


	#aqui podem ser acrescentadas features dependendo da posição da palavra no documento/bloco
	#por exemplo, palavras que estão entre as primeira e última palavras do bloco podem tomar como features as palavras ao redor
	
	if posicao_do_par > 0: #se houver palavras anteriores
		palavra_anterior = documento[posicao_do_par - 1][0]
		
		features.extend([
			'palavra_anterior_minusculo=' + palavra_anterior.lower(),
			'anterior_esta_em_maiusculo=%s' % palavra_anterior.isupper(),
			'anterior_e_titulo=%s' % palavra_anterior.istitle(),
			'anterior_e_digito=%s' % palavra_anterior.isdigit(),
			'pos_tag_ant=' + pos_tags_documento[posicao_do_par - 1][1]
		])
	else:
		features.append('BOS') #início de documento



		

	if posicao_do_par < len(documento) - 1:
		palavra_posterior = documento[posicao_do_par + 1][0]
		
		features.extend([
			'palavra_posterior_minusculo=' + palavra_posterior.lower(),
			'posterior_esta_em_maiusculo=%s' % palavra_posterior.isupper(),
			'posterior_e_titulo=%s' % palavra_posterior.istitle(),
			'posterior_e_digito=%s' % palavra_posterior.isdigit(),
			'pos_tag_post=' + pos_tags_documento[posicao_do_par + 1][1]
		])
	else:
		features.append('EOS') #fim de documento

	

	return features



def main():
	#definição dos regexes
	regex_numero_cd = re.compile('CD/[0-9][0-9][0-9][0-9][0-9]\.[0-9][0-9][0-9][0-9][0-9]-[0-9][0-9]') #CD/19369.98748-55
	regex_numero_sf = re.compile('SF/[0-9][0-9][0-9][0-9][0-9]\.[0-9][0-9][0-9][0-9][0-9]-[0-9][0-9]') #SF/19451.97508-04

	pares_palavra_tag = []
	nomes_arquivos = os.listdir('/mnt/hd0/igorma/Ágora/github_igor/leggo-content/tradador_de_segmentos/tagFiles/')
	total_blocos_por_arquivo = []
	for arquivo in nomes_arquivos: #diretório com arquivos de treino e teste
		par_palavra_tag_atual = leitura_de_dados('tagFiles/' + arquivo)
		pares_palavra_tag += par_palavra_tag_atual
		total_blocos_por_arquivo.append(conta_quantos_blocos_tem_esse_arquivo(par_palavra_tag_atual))

	documentos = separa_em_blocos(pares_palavra_tag)


	
	
	pos_tagger = pickle.load(open("tagger_portugues.pkl", "rb"))

	X = [] #lista de lista, cada lista contém as features de palavras de um mesmo documento
	y = [] #lista de lista, cada lista contém as labels de palavras de um mesmo documento
	for documento in documentos:
		Xi = [] #vetor de features, cada posição contém as features de uma palavra
		yi = [] #vetor de labels, cada posição contém as labels de uma palavra
		pos_tags_documento = pos_tagger.tag(list(zip(*documento))[0])
		for i in range(len(documento)):
			#Xi.append(criador_de_features(documento, i, doc_nlp))
			Xi.append(criador_de_features(documento, i, pos_tags_documento))
			yi.append(documento[i][1])
		X.append(Xi)
		y.append(yi)


	#roda o modelo NER obtido para o texto e substituir as palavras que forem classificadas como PESSOA, TEMPO ou LOCAL
	tagger = pycrfsuite.Tagger()
	tagger.open('modelo_NER.model')
	y_pred = [tagger.tag(unidade_x_teste) for unidade_x_teste in X] #predições
	

	documentos_formatados = []
	cont = 0
	cont_outros = 0
	for i in range(len(y_pred)):
		doc_atual = y_pred[i]
		documento = []
		for j in range(len(doc_atual)):
			if('B-PESSOA' == y_pred[i][j] or 'B-TEMPO' == y_pred[i][j] or 'B-LOCAL' == y_pred[i][j]): #se for I- (inside) deleta, se for B- (begin) substitui pela predição
				documento.append(y_pred[i][j])
				cont += 1
			else:
				if('I-PESSOA' == y_pred[i][j] or 'I-TEMPO' == y_pred[i][j] or 'I-LOCAL' == y_pred[i][j]): #nesse caso não adiciona
					cont += 1
					pass	
				else:
					documento.append(documentos[i][j][0])

			if('B-ORGANIZACAO' == y_pred[i][j] or 'B-LEGISLACAO' == y_pred[i][j] or 'B-JURISPRUDENCIA' == y_pred[i][j] or
				'I-ORGANIZACAO' == y_pred[i][j] or 'I-LEGISLACAO' == y_pred[i][j] or 'I-JURISPRUDENCIA' == y_pred[i][j]):
				cont_outros += 1 

		documentos_formatados.append(documento)
	

	#Execução dos regex
	padrao1 = re.compile(regex_numero_cd)
	padrao2 = re.compile(regex_numero_sf)
	total = 0
	for doc in documentos_formatados:
		doc_a = ' '.join(doc)
		p1 = padrao1.findall(doc_a)
		p2 = padrao2.findall(doc_a)
		total += len(p1) + len(p2)
		doc_a = re.sub(regex_numero_cd, '', doc_a)
		doc_a = re.sub(regex_numero_sf, '', doc_a)
		print(doc_a)

	#TESTES
	#print('***' + str(total))
	#print(np.array(total_blocos_por_arquivo).sum())
	#print(len(documentos_formatados))
	#print(len(documentos))
	#print(documentos[0][0])

	caminho = '/local/emendas_processadas_em_blocos/'
	indice_arquivo = 0
	indice_blocos = 0
	for arquivo in nomes_arquivos: #pra cada arquivo
		os.mkdir(caminho + arquivo) #cria um diretório com o nome DESSE ARQUIVO ATUAL
		contador_blocos_especifico = 0 #cada arquivo tem um total de blocos
		while(contador_blocos_especifico < total_blocos_por_arquivo[indice_arquivo]): #enquanto não alcançarmos esse número de blocos específico
			#transforma em texto e faz os regexes
			doc_a = ' '.join(documentos_formatados[indice_blocos])
			doc_a = re.sub(regex_numero_cd, '', doc_a)
			doc_a = re.sub(regex_numero_sf, '', doc_a)

			#cria um arquivo/bloco na PASTA DAQUELE ARQUIVO
			with open("emendas_processadas_em_blocos/" + arquivo + '/bloco_' + str(contador_blocos_especifico) + '__' + documentos[indice_blocos][0][1] , 'w') as arq: #documentos[indice_blocos][0][1] => para aquele bloco acessa uma tupla (palavra, tag) e obtém a tag
				arq.write(doc_a) #escreve a saída pré-processada
				
			contador_blocos_especifico += 1 
			indice_blocos += 1 #incremente o índice global de blocos
		indice_arquivo += 1



if __name__ == "__main__":
	main()

	
