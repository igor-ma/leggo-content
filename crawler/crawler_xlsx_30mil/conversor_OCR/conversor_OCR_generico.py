import io
from PIL import Image
import pytesseract
from wand.image import Image as wi
import os

def obtem_txts():
	arquivos = os.listdir('pdfs_para_extrair/')

	for nome_arq in arquivos:
		pdf = wi(filename = "pdfs_para_extrair/" + nome_arq, resolution = 300)
		pdfImage = pdf.convert('jpeg')

		imageBlobs = []

		for img in pdfImage.sequence:
			imgPage = wi(image = img)
			imageBlobs.append(imgPage.make_blob('jpeg'))

		recognized_text = ""
		for imgBlob in imageBlobs:
			im = Image.open(io.BytesIO(imgBlob))
			text = pytesseract.image_to_string(im, lang = 'por')
			recognized_text += text

		#print(recognized_text)
		with open("pdfs_convertidos/" + nome_arq + '.txt', 'w') as arq:
			arq.write(recognized_text)
	




def main():
	obtem_txts()


if __name__ == "__main__":
	main()
