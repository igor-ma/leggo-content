import os

arquivos_com_pdf = os.listdir('teores_pdf_e_temas')

with open('emendas_tab.tsv', 'r') as arquivo:
		linhas = arquivo.readlines()

for linha in linhas[1:]:
	try:
		campos = linha.split('\t') #separa em campos
	

		nome_arquivo = campos[2] #para salvar o teor da emenda
		assunto = campos[12]


		nome_arquivo = nome_arquivo.replace('/', '___').replace(' ', '_')
		nome_arquivo += '.pdf'

		if nome_arquivo in arquivos_com_pdf:
			os.rename('teores_pdf_e_temas/' + nome_arquivo, 'teores_pdf_e_temas/setor_' + assunto + "_" + nome_arquivo)

	except:
		pass



arquivos_com_pdf = os.listdir('teores_pdf_e_temas')

print(len(arquivos_com_pdf))
#exit(0)
for arquivo in arquivos_com_pdf:
	if 'setor' not in arquivo:
		os.remove('teores_pdf_e_temas/' + arquivo)
