'''
	Dado um diretório com arquivos de textos
	Para cada arquivo
		1. Tokeniza o arquivo
			1.1. Coloca um tag auxiliar para cada token (apenas para fins de formatação), pois é esperado uma lista de tuplas [(p1, t1), ..., (p2, t2)]
		2. Obtém a lista de features (X)
		3. Usa o classificador para segmentar o arquivo
		4. Cria uma pasta com o nome do arquivo
		5. Escreve cada bloco em um arquivo (usando a tag obtida na classificação no nome do arquivo para identificar o tipo de bloco)

'''


import os
import pickle
import pycrfsuite
#import spacy


'''
	Funções auxiliares
'''
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
	'''
		Abrindo arquivos e formatando
	'''
	lista_arquivos = os.listdir('/local/textos_pec6/')

	#nlp = spacy.load('pt_core_news_sm')
	documentos = []
	for arquivo in lista_arquivos:
		print(arquivo)
		documento_atual = []
		with open('textos_pec6/' + arquivo, 'r') as arq:
			texto = arq.read()
			#doc = nlp(texto)
			#for token in doc:
			#	print(token.text, token.pos_, token.dep_)
			texto = texto.split()
			for palavra in texto:
				documento_atual.append((palavra, 'tag_auxiliar'))
		documentos.append(documento_atual)


	'''
		Obtendo as features
	'''

	tagger = pickle.load(open("tagger_portugues.pkl", "rb"))


	X = [] #lista de lista, cada lista contém as features de palavras de um mesmo documento
	for documento in documentos:
		Xi = [] #vetor de features, cada posição contém as features de uma palavra
		pos_tags_documento = tagger.tag(list(zip(*documento))[0])
		for i in range(len(documento)):
			Xi.append(criador_de_features(documento, i, pos_tags_documento))
		X.append(Xi)



	'''
		Classificando
	'''

	tagger = pycrfsuite.Tagger()
	tagger.open('modelo.model')

	conta_arq = 0
	for unidade_x_teste in X:
		saida_arq = ""
		tag_pred = tagger.tag(unidade_x_teste)
		print(len(tag_pred))
		print(len(unidade_x_teste))
		print(range(len(unidade_x_teste)))
		for i in range(len(unidade_x_teste)):
			#print(unidade_x_teste[i][1].split('=')[1] + ' ' + tag_pred[i] + '\n')
			saida_arq += unidade_x_teste[i][1].split('=')[1] + ' ' + tag_pred[i] + '\n'
		with open('pec6_predicao_em_arquivos/' + lista_arquivos[conta_arq] + '_predito.txt', 'w') as arq:
			arq.write(saida_arq)

		conta_arq += 1
	


if __name__ == "__main__":
	main()






