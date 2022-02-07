import PyPDF2
import pdfplumber
import re
from pathlib import Path


# path = r'C:\Users\2104819624\Downloads\Safra VV Todos 2603.pdf'
# Salve = 'C:\ELAW\PDF'
# nosso_numero = '6001464461' '6001461411'

def Arquivo_existe(path):
    try:
        # path = r'C:\ELAW\PDF\PDF Bancos\26.03 - Copy\Bradesco_26032021_070351.PDF'
        fileName = path
        fileObj = Path(fileName)
        return fileObj.is_file()
    except:
        return False


def Criar_PDF(path, pages, nosso_numero, new_path):
    if Arquivo_existe(path):
        pdf_file_path = path
        file_base_name = pdf_file_path.replace('.pdf', '')

        pdf = PyPDF2.PdfFileReader(pdf_file_path, 'r')
        msg = ""

        try:
            # pages = [0, 2, 4]  # page 1, 3, 5
            pdfWriter = PyPDF2.PdfFileWriter()

            for page_num in pages:
                pdfWriter.addPage(pdf.getPage(page_num))

            with open(new_path + '\\' + nosso_numero + '.pdf'.format(file_base_name), 'wb') as f:
                pdfWriter.write(f)
                f.close()
            print("Arquivo PDF gerado com sucesso!")
            msg = "Processo executado com sucesso!"

        except Exception as ex:
            msg = ex
            print("Error: " + ex)

        finally:
            return msg
    else:
        msg = "Caminho informado não existe ou acesso está bloqueado"
        return msg


def Criar_PDF_Unico(path, pages, docN, new_path):
    if Arquivo_existe(path):
        pdf_file_path = path
        file_base_name = pdf_file_path.replace('.pdf', '')

        pdf = PyPDF2.PdfFileReader(pdf_file_path, 'r')
        msg = ""

        try:
            # pages = [0, 2, 4]  # page 1, 3, 5
            pdfWriter = PyPDF2.PdfFileWriter()
            pdfWriter.addPage(pdf.getPage(pages))

            with open(new_path + '\\' + docN + '.pdf'.format(file_base_name), 'wb') as f:
                pdfWriter.write(f)
                f.close()
            # print(f"Arquivo PDF: {docN} gerado com sucesso!")
            msg = "Processo executado com sucesso!"

        except Exception as ex:
            msg = ex
            print("Error: " + ex)

        finally:
            return msg
    else:
        msg = "Caminho informado não existe ou acesso está bloqueado"
        return msg


def Localizar_Pagina(path, nosso_numero):
    wpages = []

    cont = 0
    # string_pdf[string_pdf.find('Comprovante de pagamento eletrônico'):-601].replace('Comprovante de pagamento eletrônico 0,00','').replace('\n','')
    if Arquivo_existe(path):
        try:
            with pdfplumber.open(path) as pdf:
                pages = pdf.pages
                for i, pg in enumerate(pages):
                    first_page = pdf.pages[i]
                    string_pdf = first_page.extract_text()

                    if string_pdf.find(nosso_numero) > -1:
                        num_page = i
                        wpages.append(num_page)
                        cont = cont + 1
                        break
                        # print(string_pdf)

            print("Total de pagins localizads no arquivo: " + str(path) + " - paginas: " + str(cont))

            return wpages, nosso_numero, cont

        except Exception as ex:
            print("Error: " + ex)
    else:
        msg = "Caminho informado não existe ou acesso está bloqueado"
        return msg

# Teste_PDF(fnPDF_FindText())

def all_pages_pdf_safra(path, new_path):
    count = 0
    # path = r'C:\ELAW\PDF\PDF Bancos\06.07\422_Safra_1.pdf'
    # new_path = r'C:\ELAW\PDF\PDF Bancos\06.07\Safra Pages'
    doc = ''
    docN = ''

    if Arquivo_existe(path):
        try:
            with pdfplumber.open(path) as pdf:
                pages = pdf.pages
                for i, pg in enumerate(pages):
                    first_page = pdf.pages[i]
                    string_pdf = first_page.extract_text()

                    if string_pdf is not None:

                        if string_pdf.find('Comprovante de Pagamento | BOLETO BANCÁRIO') > -1:
                            doc = string_pdf[string_pdf.find('BLQ'):string_pdf.find('Uso do Banco')]
                            docN = re.findall('\d+', doc)

                        elif string_pdf.find('Comprovante de Pagamento | TED') > -1 and string_pdf.find(
                                'DADOS DA OPERAÇÃO') == -1:
                            doc = string_pdf[string_pdf.find('N° Documento'):-601]
                            docN = doc[52:doc.find('TED')]
                            docN = re.findall('\d+', docN)

                        elif string_pdf.find('DADOS DA OPERAÇÃO') > -1:

                            if string_pdf.find('Transf. entre contas') > -1:
                                doc = string_pdf[string_pdf.find('Valor') + 17:string_pdf.find('Transf. entre contas')]
                                docN = doc
                                docN = re.findall('\d+', docN)

                            else:
                                doc = string_pdf[string_pdf.find('Valor') + 17:-901]
                                docN = doc
                                docN = re.findall('\d+', docN)

                        Criar_PDF_Unico(path, i, docN[0], new_path)
                        count = count + 1

            print("Total de arquivos Banco Safra gerados na pasta : " + str(new_path) + " - Arquivos: " + str(count))

        except Exception as ex:
            print("Error: " + ex)
    else:
        msg = "Caminho informado não existe ou acesso está bloqueado"
        return msg


def all_pages_pdf_bb(path, new_path):
    count = 0
    # path = r'C:\ELAW\PDF\PDF Bancos\05.07\001_Banco do Brasil_1.pdf'
    # new_path = r'C:\ELAW\PDF\PDF Bancos\05.07\BB Pages'
    doc = ''
    docN = ''

    if Arquivo_existe(path):
        try:
            with pdfplumber.open(path) as pdf:
                pages = pdf.pages

                for i, pg in enumerate(pages):
                    first_page = pdf.pages[i]
                    string_pdf = first_page.extract_text()

                    if string_pdf.find('001 - BANCO DO BRASIL S.A.') > -1:
                        doc = string_pdf[string_pdf.find('Descrição da Guia: '):string_pdf.find('Agência')]
                        docN = re.findall('\d+', doc)

                    Criar_PDF_Unico(path, i, docN[0], new_path)
                    count = count + 1

            print(
                "Total de arquivos Banco do Brasil gerados na pasta : " + str(new_path) + " - Arquivos: " + str(count))

        except Exception as ex:
            print("Error: " + ex)
    else:
        msg = "Caminho informado não existe ou acesso está bloqueado"
        return msg


def all_pages_pdf_bradesco(path, new_path):
    count = 0
    # path = r'C:\ELAW\PDF\PDF Bancos\05.07\237_Bradesco_1.pdf'
    # new_path = r'C:\ELAW\PDF\PDF Bancos\05.07\Bradesco Pages'
    doc = ''
    docN = ''

    if Arquivo_existe(path):
        try:
            with pdfplumber.open(path) as pdf:
                pages = pdf.pages

                for i, pg in enumerate(pages):
                    first_page = pdf.pages[i]
                    string_pdf = first_page.extract_text()

                    if string_pdf.find('Comprovante de Transação Bancária') > -1:
                        doc = string_pdf[string_pdf.find('barras: '):string_pdf.find('Empresa / Órgão:')]
                        docN = re.findall('\d+', doc)

                    Criar_PDF_Unico(path, i, docN[6][3:], new_path)
                    count = count + 1

            print("Total de arquivos Banco Bradesco gerados na pasta : " + str(new_path) + " - Arquivos: " + str(count))

        except Exception as ex:
            print("Error: " + ex)
    else:
        msg = "Caminho informado não existe ou acesso está bloqueado"
        return msg
