import os


def salva_em_blocos_2():
	arquivos = os.listdir('pec6_predicao_em_arquivos/')

	for arq in arquivos:
		print(arq)
		os.mkdir('pec6_em_blocos_preditos/' + arq)
		with open('pec6_predicao_em_arquivos/' + arq, 'r') as atual:
			texto = atual.readlines()


		cont_bloco = 1
		bloco_atual = []
		i = 0
		while i < len(texto):
			print(i)
			try:
				tag = texto[i].split()[1]
			except: #alguns raros casos possuem uma linha em branco contendo apenas a tag, devemos apenas ignorar estas linhas
				i += 1
				pass
			if tag == 'O':
				bloco_atual.append(texto[i])
			else: #se for I
				with open('pec6_em_blocos_preditos/' + arq + '/bloco_' + str(cont_bloco), 'w') as arq_bloco:
					for token in bloco_atual:
						arq_bloco.write(token)
				bloco_atual = []
				bloco_atual.append(texto[i])					
				cont_bloco += 1
			i += 1
		with open('pec6_em_blocos_preditos/' + arq + '/bloco_' + str(cont_bloco), 'w') as arq_bloco:
				for token in bloco_atual:
					arq_bloco.write(token)
				





def main():
	salva_em_blocos_2()



if __name__ == "__main__":
	main()

