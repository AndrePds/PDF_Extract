from datetime import datetime, timedelta
import pandas as pd
from PDF_Work import Criar_PDF, Localizar_Pagina, all_pages_pdf_safra, all_pages_pdf_bb, all_pages_pdf_bradesco
import os


class Pesquisa_Arquivo:

    # Metodos de leitura para os arquivos Config e arquivos a serem processado
    @staticmethod
    def ler_arquivo():
        caminho_arquivo = 'C:\\ELAW\Arquivo de pesquisa\\Pesquisa_ID.csv'
        config = pd.read_csv(caminho_arquivo, delimiter=";", encoding='latin1', index_col=False)
        return config

    def arquivo_campo(name_var):
        df = Pesquisa_Arquivo.ler_arquivo()
        dff = df.dropna(axis=0, how='all')
        index = int(str(dff.loc[dff['Name'] == name_var, 'Value'])[0])
        value = str(dff.loc[dff['Name'] == name_var, 'Value'][index])
        value = value.strip()

        return value

    def ler_todos_pdf(caminho):

        try:
            arr = os.listdir(caminho)
            # print(arr)
            return arr
        except Exception as ex:
            print(ex)

    def calcula_dia_hora(dia, hora, operacao, format):

        data = datetime.now()

        try:
            if data.strftime('%A') == 'Monday':
                data = datetime.now() - timedelta(hours=hora) - timedelta(days=3)
                return data.strftime(format)

            elif data.strftime('%A') == 'Sunday':
                data = datetime.now() - timedelta(hours=hora) - timedelta(days=2)
                return data.strftime(format)

            elif data.strftime('%A') == 'Saturday':
                data = datetime.now() - timedelta(hours=hora) - timedelta(days=1)
                return data.strftime(format)

            elif operacao == 'soma':
                data = data + timedelta(hours=hora) + timedelta(days=dia)
                return data.strftime(format)

            elif operacao == 'sub':
                data = data - timedelta(hours=hora) - timedelta(days=dia)
                return data.strftime(format)

        except Exception as ex:
            print(ex)

    def cria_arquivo_log_txt(caminho, nomeArquivo):

        try:
            nome = caminho + nomeArquivo + ".txt"
            arquivo = open(nome, "w")
            arquivo.write("Gerado")
            arquivo.close()
            print("Arquivo de log criado com sucesso!")

        except (Exception) as error:
            print(error)

    # @staticmethod
    # def Cria_Novo_PDF():
    #
    #     caminho = Pesquisa_Arquivo.arquivo_campo("Arquivo PDF")
    #     texto = Pesquisa_Arquivo.arquivo_campo("Id")
    #     salvar = Pesquisa_Arquivo.arquivo_campo("Salvar arquivo")
    #
    #     if caminho != "" and texto != "" and salvar != "":
    #         pdf_info = Localizar_Pagina(caminho, texto)
    #         x = pdf_info[2]
    #         if x > 0:
    #             process = Criar_PDF(caminho, pdf_info [0], pdf_info [1], salvar)
    #             print(process)
    #         else:
    #             print("Não foi possivel localizar paginas para o texto informado")
    #     else:
    #         print("Via Bot Informa", "Todos os campos devem estar preenchidos")
    #         print("Campo em branco!")

    @staticmethod
    def Cria_Novo_PDF():

        caminho = Pesquisa_Arquivo.arquivo_campo("Arquivo PDF")
        texto = Pesquisa_Arquivo.arquivo_campo("Id")
        salvar = Pesquisa_Arquivo.arquivo_campo("Salvar arquivo")
        frmPgto = Pesquisa_Arquivo.arquivo_campo("FrmPgto")

        lista_pdf = Pesquisa_Arquivo.ler_todos_pdf(caminho)

        if caminho != "" and texto != "" and salvar != "" and frmPgto != "":

            if frmPgto == 'B' or frmPgto == 'U':

                for file in lista_pdf:

                    if file.find('Safra') > -1:

                        arquivo = caminho + str(file)
                        pdf_info = Localizar_Pagina(arquivo, texto)
                        x = pdf_info[2]

                        if x > 0:
                            process = Criar_PDF(arquivo, pdf_info[0], pdf_info[1], salvar)
                            print(process)
                            break

            if frmPgto == 'T':

                for file in lista_pdf:

                    if file.find('Brasil') > -1:

                        arquivo = caminho + str(file)
                        pdf_info = Localizar_Pagina(arquivo, texto)
                        x = pdf_info[2]

                        if x > 0:
                            process = Criar_PDF(arquivo, pdf_info[0], pdf_info[1], salvar)
                            print(process)
                            break

            if frmPgto == 'TB':

                for file in lista_pdf:

                    if file.find('Bradesco') > -1:

                        arquivo = caminho + str(file)
                        pdf_info = Localizar_Pagina(arquivo, texto)
                        x = pdf_info[2]

                        if x > 0:
                            process = Criar_PDF(arquivo, pdf_info[0], pdf_info[1], salvar)
                            print(process)
                            break

        else:
            print("Via Bot Informa", "Todos os campos devem estar preenchidos")
            print("Campo em branco!")

    @staticmethod
    def Cria_Todos_PDF():

        log = 'C:\\ELAW\\Message\\'
        mes_br = ['JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO',
                  'NOVEMBRO', 'DEZEMBRO']

        raiz = '\\\\nas01.via.varejo.corp\\share_lv\\cont_pagar\\ELAW_ROBÔ'
        ano = Pesquisa_Arquivo.calcula_dia_hora(1, 0, 'sub', '%Y')
        mes_dia = Pesquisa_Arquivo.calcula_dia_hora(1, 0, 'sub', '%d.%m')
        mes = mes_br[int(mes_dia[3:]) - 1]

        salvar = 'C:\\ELAW\\PDF'
        caminho = raiz + '\\' + ano + '\\' + mes + '\\' + mes_dia
        lista_pdf = Pesquisa_Arquivo.ler_todos_pdf(caminho)

        try:
            if caminho != "":

                for file in lista_pdf:

                    if file.find('Safra') > -1 or file.find('SAFRA') > -1:
                        arquivo = caminho + '\\' + str(file)
                        all_pages_pdf_safra(arquivo, salvar)

                    if file.find('Brasil') > -1 or file.find('BRASIL') > -1:
                        arquivo = caminho + '\\' + str(file)
                        all_pages_pdf_bb(arquivo, salvar)

                    if file.find('Bradesco') > -1 or file.find('BRADESCO') > -1:
                        arquivo = caminho + '\\' + str(file)
                        all_pages_pdf_bradesco(arquivo, salvar)

                Pesquisa_Arquivo.cria_arquivo_log_txt(log, 'PDF gerados com sucesso')

            else:
                Pesquisa_Arquivo.cria_arquivo_log_txt(log, 'Não foi possivel gerar os arquivos PDF')
                print("Via Bot Informa", "Todos os campos devem estar preenchidos")
                print("Campo em branco!")

        except Exception as ex:
            Pesquisa_Arquivo.cria_arquivo_log_txt(log, 'Não foi possivel gerar os arquivos PDF')
            print(ex)



