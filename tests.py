# encoding: utf-8
from buscador_correios import BuscadorCorreios


def test_busca_cep():
    uf = "SP"
    localidade = "São Paulo"
    tipo = "Avenida"
    logradouro = "otacilio tomanik"
    numero = "350"

    resultado = BuscadorCorreios.busca_cep(uf, localidade, tipo, logradouro, numero)
    assert resultado[0].cep == "05363-000"

def test_buscador_endereco_05588000():
    cep = "05588000"
    resultado = BuscadorCorreios.busca_endereco(cep)
    assert resultado[0].cep == "05588-000"


def test_busca_cep_endereco_05588000():
    relaxation = "05588000"
    # "LOG" - Localidade/Logradouro
    # "PRO" - CEP Promocional
    # "CPC" - Caixa Postal Comunitária
    # "GRU" - Grande Usuário
    # "UOP" - Unidade Operacional
    # "ALL" - Todos
    tipoCEP = "ALL"
    semelhante = "N"
    resultado = BuscadorCorreios.busca_cep_endereco(relaxation, tipoCEP, semelhante)
    assert resultado[0].cep == "05588-000"


def test_busca_cep_endereco_otacilio_tomanik():
    relaxation = "otacilio tomanik"
    # "LOG" - Localidade/Logradouro
    # "PRO" - CEP Promocional
    # "CPC" - Caixa Postal Comunitária
    # "GRU" - Grande Usuário
    # "UOP" - Unidade Operacional
    # "ALL" - Todos
    tipoCEP = "ALL"
    semelhante = "N"
    resultado = BuscadorCorreios.busca_cep_endereco(relaxation, tipoCEP, semelhante)
    assert len(resultado) > 0
