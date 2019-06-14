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
def separa_em_blocos(pares_palavra_tag, tamanho_janela = 1):
	'''
	Separa o documento em diferentes blocos/segmentos.
	Retorna uma lista de documentos/blocos, lista de lista de tuplas.
	'''

	'''
	documentos = []
	documentos.append([pares_palavra_tag[0], pares_palavra_tag[1]]) #primeiro bloco possui apenas a primeira palavra e a segunda
	for i in range(1, len(pares_palavra_tag) - 1):
		documentos.append([pares_palavra_tag[i - 1], pares_palavra_tag[i], pares_palavra_tag[i + 1]]) #os blocos centrais possuem a palavra central + as palavras de borda
	documentos.append([pares_palavra_tag[len(pares_palavra_tag) - 2], pares_palavra_tag[len(pares_palavra_tag) - 1]]) #último bloco possui apenas a última palavra e a panúltima
	'''


	documentos = []
	for i in range(tamanho_janela):
		documentos.append(pares_palavra_tag[0:i] + [pares_palavra_tag[i]] + pares_palavra_tag[(i + 1):(i + 1 + tamanho_janela)]) 
	for i in range(tamanho_janela, len(pares_palavra_tag) - tamanho_janela):
		documentos.append(pares_palavra_tag[(i - tamanho_janela):i] + [pares_palavra_tag[i]] + pares_palavra_tag[(i + 1):(i + 1 + tamanho_janela)]) #os blocos centrais possuem a palavra central + as palavras de borda
	for i in range(len(pares_palavra_tag) - tamanho_janela, len(pares_palavra_tag)):
		documentos.append(pares_palavra_tag[(i - tamanho_janela):i] + [pares_palavra_tag[i]] + pares_palavra_tag[(i + 1):(i + tamanho_janela)])


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
	'''
		Abrindo arquivos e formatando
	'''
	lista_arquivos = os.listdir('/local/textos_pec6/')

	#nlp = spacy.load('pt_core_news_sm')
	pares_palavra_tag = []
	contador_blocos_documento = []
	for arquivo in lista_arquivos:
		#print(arquivo)
		documento_atual = []
		with open('textos_pec6/' + arquivo, 'r') as arq:
			texto = arq.read()
			#doc = nlp(texto)
			#for token in doc:
			#	print(token.text, token.pos_, token.dep_)
			texto = texto.split()
			for palavra in texto:
				documento_atual.append((palavra, 'tag_auxiliar'))
		contador_blocos_documento.append(len(documento_atual))
		pares_palavra_tag += documento_atual
	documentos = separa_em_blocos(pares_palavra_tag, 4)
	#for doc in documentos[:5]:
		#print(doc)
	#print(len(documentos))
	#exit(0)

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


	#tenho milhares de blocos
	#cada arquivo tem um número de blocos salvo em contador_blocos_documento
	#então pra cada valor nessa lista de tamanhos
		#itera, lendo os N próximos elementos de X (sendo N o tamanho dos blocos)
			#pega a classificação, adiciona na string de saída
		#salva a saída no arquivo de predição daquela emenda
		#continua pro próximo arquivo


	iterador_X_global = 0
	contador_arquivos = 0
	for num_blocos_atual in contador_blocos_documento:
		saida_arq = ""
		for i in range(num_blocos_atual):
			unidade_x_teste = X[iterador_X_global]
			#e aqui a avaliação do que vai ser feito depende da localização do bloco. No caso, o tamanho da janela é 4 SEMPRE.
			#assim sendo, os 4 primeiros são casos de borda. os demais são simples de serem tratados
			
			
			tag_pred = tagger.tag(unidade_x_teste) #taggea todo o bloco, mas queremos apenas a palavra que nos interessa e isso depende se ela é caso de borda ou não
			print(tag_pred)
			aux = 4 if (i >= 4) else i
			print(unidade_x_teste[aux][1].split('=')[1] + ' ' + str(aux))
			if(i >= 4): #se for um bloco não de borda
				saida_arq += unidade_x_teste[4][1].split('=')[1] + ' ' + tag_pred[4] + '\n' #a tag que nos interessa é a da palavra central, na quarta posição
			else: #se for um bloco de borda de início
				saida_arq += unidade_x_teste[i][1].split('=')[1] + ' ' + tag_pred[i] + '\n' #a tag que nos interessa é indexada pelo contador i se ela for borda de início

			print(num_blocos_atual)
			print(iterador_X_global)
			print(len(X))


			iterador_X_global += 1

		with open('pec6_predicao_em_arquivos/' + lista_arquivos[contador_arquivos] + '_predito.txt', 'w') as arq:
			arq.write(saida_arq)

		contador_arquivos += 1




if __name__ == "__main__":
	main()



















