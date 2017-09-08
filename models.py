# encoding: utf-8


class ResultadoBusca(object):

    def __init__(self, logradouro, bairro, localidade_UF, cep):
        self.logradouro = logradouro
        self.bairro = bairro
        self.localidade_UF = localidade_UF
        self.cep = cep

    def __str__(self):
        return "{logradouro} / {bairro} / {localidade_UF} / {cep}".format(logradouro=self.logradouro,
                                                                          bairro=self.bairro,
                                                                          localidade_UF=self.localidade_UF,
                                                                          cep=self.cep)
