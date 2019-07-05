import os


def salva_em_blocos():
	arquivos = os.listdir('pec6_predicao_em_arquivos/')

	for arq in arquivos:
		print(arq)
		os.mkdir('pec6_em_blocos_preditos/' + arq)
		with open('pec6_predicao_em_arquivos/' + arq, 'r') as atual:
			texto = atual.readlines()
			print(len(texto))
			
			cont_bloco = 1
			linha = 0
			while linha < (len(texto) - 2):
				doc_a = []
				print(linha)
				print(texto[linha])
				print(texto[linha + 1].split()[1])
				try:
					while(linha < len(texto) - 2 and texto[linha + 1].split()[1] == 'O'):
						doc_a.append(texto[linha])
						linha += 1
						print(linha)
					doc_a.append(texto[linha])
					linha += 1
				except: #há linhas apenas com espaço em branco e tag, devem ser ignoradas
					linha += 1
				with open('pec6_em_blocos_preditos/' + arq + '/bloco_' + str(cont_bloco), 'w') as arq_bloco:
					for token in doc_a:
						arq_bloco.write(token + '\n')
					#linha -= 1
				cont_bloco += 1

def main():
	salva_em_blocos()



if __name__ == "__main__":
	main()

