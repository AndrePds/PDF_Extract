from Pesquisa_PDF import Pesquisa_Arquivo as pa


def upload_pdf():

    path = r'C:\ELAW\PDF'
    all_files = pa.ler_todos_pdf(path)

    for file in all_files:

        if file.find('.pdf') > -1:
            print(file[:-4])


upload_pdf()
