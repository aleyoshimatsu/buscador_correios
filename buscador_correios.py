# encoding: utf-8
import requests
from lxml import html
from models import ResultadoBusca


class BuscadorCorreios(object):
    SUCESSO = "'DADOS ENCONTRADOS COM SUCESSO.'"
    NAO_ENCONTRADO = "'LOGRADOURO NAO ENCONTRADO.'"

    @staticmethod
    def busca_cep(uf, localidade, tipo, logradouro, numero):
        headers = {}
        data = {}
        url = "http://www.buscacep.correios.com.br/sistemas/buscacep/buscaCep.cfm"
        r_get = requests.get(url, data=data, headers=headers)

        data = {'UF': uf, 'Localidade': localidade, 'Tipo': tipo, 'Logradouro': logradouro, 'Numero': numero}
        url = 'http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaCep.cfm'
        r_post = requests.post(url, data=data, headers=headers, cookies=r_get.cookies)
        tree = html.fromstring(r_post.content)

        return BuscadorCorreios._parse_tree(tree)

    @staticmethod
    def busca_endereco(cep):
        headers = {}
        data = {}
        url = "http://www.buscacep.correios.com.br/sistemas/buscacep/BuscaEndereco.cfm"
        r = requests.get(url, data=data, headers=headers)

        data = {'CEP': cep}
        url = 'http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaEndereco.cfm'
        r = requests.post(url, data=data, headers=headers, cookies=r.cookies)
        tree = html.fromstring(r.content)

        return BuscadorCorreios._parse_tree(tree)

    @staticmethod
    def busca_cep_endereco(relaxation, tipoCEP, semelhante):
        headers = {}
        data = {}
        url = "http://www.buscacep.correios.com.br/sistemas/buscacep/BuscaCepEndereco.cfm"
        r = requests.get(url, data=data, headers=headers)

        data = {'relaxation': relaxation, 'tipoCEP': tipoCEP, 'semelhante': semelhante}
        url = 'http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaCepEndereco.cfm'
        r = requests.post(url, data=data, headers=headers, cookies=r.cookies)
        tree = html.fromstring(r.content)

        return BuscadorCorreios._parse_tree(tree)

    @staticmethod
    def _parse_tree(tree):
        b_nao_encontrado = tree.xpath("//p/text()=" + BuscadorCorreios.NAO_ENCONTRADO)

        result = []

        if b_nao_encontrado:
            return result

        b_sucesso = tree.xpath("//p/text()=" + BuscadorCorreios.SUCESSO)
        # p = tree.xpath("//*[text()="+ + BuscadorCorreios.SUCESSO+"]")

        if b_sucesso:
            # table = tree.xpath("//table[contains(@class, 'tmptabela')]")
            for row in tree.xpath("//table[contains(@class, 'tmptabela')]/tr"):
                td_list = row.xpath('td')

                if len(td_list) == 0:
                    continue

                for i in range(len(td_list)):
                    a_list = td_list[i].xpath('a/text()')
                    text_list = td_list[i].xpath('text()')

                    if i == 0:
                        if len(a_list) > 0:
                            logradouro = "{0} - {1}".format(a_list[0], a_list[1])
                        else:
                            logradouro = text_list[0]
                    elif i == 1:
                        bairro = text_list[0]
                    elif i == 2:
                        localidade_UF = text_list[0]
                    elif i == 3:
                        cep = text_list[0]

                resultado_busca = ResultadoBusca(logradouro, bairro, localidade_UF, cep)
                result.append(resultado_busca)

        return result