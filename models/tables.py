class epi:
    def __init__(self, nome_epi, tipo_epi, certificado_aprovacao_epi, validade_certificado_aprovacao):
        self.nome_epi = nome_epi
        self.tipo_epi = tipo_epi
        self.certificado_aprovacao_epi = certificado_aprovacao_epi
        self.validade_certificado_aprovacao = validade_certificado_aprovacao

class funcionario:
    def __init__(self,matricula_funcionario, nome_funcionario, cpf_funcionario, setor_funcionario, funcao_funcionario, data_admissao_funcionario, telefone, email, whatsapp):
        self.matricula_funcionario = matricula_funcionario
        self.nome_funcionario = nome_funcionario
        self.cpf_funcionario = cpf_funcionario
        self.setor_funcionario = setor_funcionario
        self.funcao_funcionario = funcao_funcionario
        self.data_admissao_funcionario = data_admissao_funcionario
        self.telefone = telefone
        self.email = email
        self.whatsapp = whatsapp

    
class Registros:
    def __init__(self, matricula_funcionario, ca_EPI, data_entrega=None, data_devolucao=None, data_troca=None, motivo_devolucao=None):
        self.matricula_funcionario = matricula_funcionario
        self.ca_EPI = ca_EPI
        self.data_entrega = data_entrega
        self.data_devolucao = data_devolucao
        self.data_troca = data_troca
        self.motivo_devolucao = motivo_devolucao

class notificacao:
    def __init__(self, ca_epi, matricula_funcionario, dias_para_vencimento, data_verificacao=None, enviado=False, data_envio=None):
        self.ca_epi = ca_epi
        self.matricula_funcionario = matricula_funcionario
        self.dias_para_vencimento = dias_para_vencimento
        self.data_verificacao = data_verificacao
        self.enviado = enviado
        self.data_envio = data_envio
