# Importação das bibliotecas utilizadas no backend
from flask import Blueprint, render_template, request, jsonify, send_file
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
from models.tables import funcionario, epi, Registros
from database import get_db_connection
from datetime import datetime, timedelta, date
import json
import os
import re
from dotenv import load_dotenv
from twilio.rest import Client

# Carrega variáveis do ambiente
load_dotenv()

# Blueprint para agrupar rotas da API
api_routes = Blueprint('api_routes', __name__)

def formatar_para_twilio(telefone_raw):
    if not telefone_raw:
        return ""
    # Remove qualquer caractere que não seja número
    numeros = re.sub(r'\D', '', str(telefone_raw))

    # Formata número brasileiro
    if len(numeros) == 11:
        return f"+55{numeros}"
    # Formata número já com código do país
    elif len(numeros) == 13:
        return f"+{numeros}"

    # Retorna como está caso não tenha padrão
    return numeros

def parse_data_sqlite(data):
    """Função auxiliar para tratar datas retornadas como string pelo SQLite."""
    if not data:
        return None
    if isinstance(data, str):
        return data[:10]  # Pega apenas YYYY-MM-DD
    return data.strftime('%Y-%m-%d')

def parse_datetime_sqlite(data):
    """Função auxiliar para tratar datetimes retornados como string."""
    if not data:
        return None
    if isinstance(data, str):
        return data
    return data.strftime('%Y-%m-%d %H:%M:%S')


def buscarPanel():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*) AS total
    FROM epi
    WHERE DATE(validade_certificado_aprovacao) = DATE('now', 'localtime')
    """)
    row = cursor.fetchone()
    vencendoHoje = row["total"] if row else 0

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM registros
        WHERE DATE(data_entrega) = DATE('now', 'localtime')
    """)
    row = cursor.fetchone()
    entregasHoje = row["total"] if row else 0

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM epi
        WHERE DATE(validade_certificado_aprovacao) < DATE('now', 'localtime')
    """)
    row = cursor.fetchone()
    vencidos = row["total"] if row else 0

    cursor.close()
    conn.close()

    return {
        "vencimentos_hoje" : vencendoHoje,
        "entregas_hoje" : entregasHoje,
        "vencidos" : vencidos
    }

def buscarDashboard():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Total de EPIs
    cursor.execute("SELECT COUNT(*) AS total FROM epi")
    total_epi = cursor.fetchone()["total"]

    # registros criados hoje
    cursor.execute("SELECT COUNT(*) AS total FROM registros WHERE DATE(data_entrega) = DATE('now', 'localtime')")
    registros_hoje = cursor.fetchone()['total']

    # Total de funcionários
    cursor.execute("SELECT COUNT(*) AS total FROM funcionarios")
    total_funcionarios = cursor.fetchone()["total"]

    # EPIs vencendo em 7 dias
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM epi
        WHERE DATE(validade_certificado_aprovacao)
        BETWEEN DATE('now', 'localtime')
        AND DATE('now', 'localtime', '+7 days')
    """)
    vencendo7 = cursor.fetchone()["total"]

    # EPIs vencendo em 30 dias
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM epi
        WHERE DATE(validade_certificado_aprovacao)
        BETWEEN DATE('now', 'localtime')
        AND DATE('now', 'localtime', '+30 days')
    """)
    vencendo30 = cursor.fetchone()["total"]

    # Últimos registros
    cursor.execute("""
        SELECT
            f.nome_funcionario,
            e.nome_epi,
            r.data_entrega,
            r.data_troca
        FROM registros r
        INNER JOIN funcionarios f
            ON r.matricula_funcionario = f.matricula_funcionario
        INNER JOIN epi e
            ON r.ca_EPI = e.certificado_aprovacao_epi
        ORDER BY r.data_entrega DESC,
         r.matricula_funcionario DESC,
         r.ca_EPI DESC
        LIMIT 10
    """)

    ultimos_registros = [dict(row) for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return {
        "total_epi": total_epi,
        "total_funcionarios": total_funcionarios,
        "vencendo_30_dias": vencendo30,
        "vencendo_7_dias": vencendo7,
        "ultimos_registros": ultimos_registros
    }

@api_routes.route('/teste-dashboard')
def teste_dashboard():
    return jsonify(buscarDashboard())


# ============ CREATE ============

@api_routes.route('/api/funcionario', methods=['POST'])
def cadastrar_funcionario():
    conn = None
    cursor = None
    try:
        dados = request.get_json(silent=True)
        if not dados:
            dados = request.form.to_dict()

        func = funcionario(
            dados['matricula_funcionario'],
            dados['nome_funcionario'],
            dados['cpf_funcionario'],
            dados['setor_funcionario'],
            dados['funcao_funcionario'],
            dados['data_admissao_funcionario'],
            dados['telefone'],
            dados['email'],
            dados['whatsapp']
        )

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO funcionarios (matricula_funcionario, nome_funcionario, cpf_funcionario, setor_funcionario, funcao_funcionario, data_admissao_funcionario, telefone, email, whatsapp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(sql, (func.matricula_funcionario, func.nome_funcionario, func.cpf_funcionario, func.setor_funcionario, func.funcao_funcionario, func.data_admissao_funcionario, func.telefone, func.email, func.whatsapp))

        conn.commit()
        return jsonify({'message': 'Funcionário cadastrado com sucesso'}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@api_routes.route('/api/epi', methods=['POST'])
def cadastrar_epi():
    conn = None
    cursor = None
    try:
        dados = request.get_json()

        novo_epi = epi(
            dados['nome_epi'],
            dados['tipo_epi'], 
            dados['certificado_aprovacao_epi'], 
            dados['validade_certificado_aprovacao']
        )

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO epi (nome_epi, tipo_epi, certificado_aprovacao_epi, validade_certificado_aprovacao) VALUES (?, ?, ?, ?)"
        cursor.execute(sql, (novo_epi.nome_epi, novo_epi.tipo_epi, novo_epi.certificado_aprovacao_epi, novo_epi.validade_certificado_aprovacao))

        conn.commit()
        return jsonify({'message': 'EPI cadastrado com sucesso'}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@api_routes.route('/api/registro', methods=['POST'])
def cadastrar_registro():
    conn = None
    cursor = None
    try:
        dados = request.get_json()

        matricula = dados.get('matricula_funcionario')
        ca_epi = dados.get('ca_EPI')
        data_devolucao = dados.get('data_devolucao')
        data_entrega = date.today().isoformat()

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO registros (matricula_funcionario, ca_EPI, data_entrega, data_devolucao) VALUES (?, ?, ?, ?)"
        cursor.execute(sql, (matricula, ca_epi, data_entrega, data_devolucao))

        conn.commit()
        return jsonify({'message': 'Registro cadastrado com sucesso'}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# ============ GET ============

@api_routes.route('/api/funcionario/', methods=['GET'])
def buscar_funcionario():
    matricula = request.args.get("matricula")
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if matricula:
            cursor.execute("SELECT * FROM funcionarios WHERE matricula_funcionario = ?", (matricula,))
            row = cursor.fetchone()
            resultado = [dict(row)] if row else []
        else:
            cursor.execute("SELECT * FROM funcionarios")
            resultado = [dict(row) for row in cursor.fetchall()]

        for func in resultado:
            func['data_admissao_funcionario'] = parse_data_sqlite(func.get('data_admissao_funcionario'))
        
        # Se filtrou por matrícula e achou, retorna o objeto em vez da lista para manter compatibilidade com sua versão anterior
        if matricula and resultado:
            return jsonify(resultado[0])
            
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@api_routes.route('/api/epi/', methods=['GET'])
def buscar_epi():
    ca = request.args.get("ca")
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if ca:
            cursor.execute("SELECT * FROM epi WHERE certificado_aprovacao_epi = ?", (ca,))
            row = cursor.fetchone()
            resultado = [dict(row)] if row else []
        else:
            cursor.execute("SELECT * FROM epi")
            resultado = [dict(row) for row in cursor.fetchall()]

        for e in resultado:
            e['validade_certificado_aprovacao'] = parse_data_sqlite(e.get('validade_certificado_aprovacao'))

        if ca and resultado:
            return jsonify(resultado[0])

        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@api_routes.route('/api/registro/', methods=['GET'])
def buscar_registro():
    matricula = request.args.get("matricula")
    ca = request.args.get("ca")
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if matricula:
            cursor.execute("SELECT * FROM registros WHERE matricula_funcionario = ?", (matricula,))
        elif ca:
            cursor.execute("SELECT * FROM registros WHERE ca_EPI = ?", (ca,))
        else:
            cursor.execute("SELECT * FROM registros")
            
        resultado = [dict(row) for row in cursor.fetchall()]

        for registro in resultado:
            registro['data_entrega'] = parse_data_sqlite(registro.get('data_entrega'))
            registro['data_devolucao'] = parse_data_sqlite(registro.get('data_devolucao'))
            registro['data_troca'] = parse_data_sqlite(registro.get('data_troca'))
            
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# ============ UPDATE ============

@api_routes.route('/api/funcionario/<matricula>', methods=['PUT'])
def atualizar_funcionario(matricula):
    conn = None
    cursor = None
    try:
        dados = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM funcionarios WHERE matricula_funcionario = ?", (matricula,))
        funcionario_atual = cursor.fetchone()

        if not funcionario_atual:
            return jsonify({'erro': 'Funcionário não encontrado'}), 404

        # Como row é Indexável no SQLite
        sql = """UPDATE funcionarios 
                 SET nome_funcionario = ?, cpf_funcionario = ?, setor_funcionario = ?, 
                     funcao_funcionario = ?, data_admissao_funcionario = ?, telefone = ?, email = ?, whatsapp = ? 
                 WHERE matricula_funcionario = ?"""
        cursor.execute(sql, (
            dados.get('nome_funcionario', funcionario_atual['nome_funcionario']), 
            dados.get('cpf_funcionario', funcionario_atual['cpf_funcionario']), 
            dados.get('setor_funcionario', funcionario_atual['setor_funcionario']), 
            dados.get('funcao_funcionario', funcionario_atual['funcao_funcionario']), 
            dados.get('data_admissao_funcionario', funcionario_atual['data_admissao_funcionario']), 
            dados.get('telefone', funcionario_atual['telefone']),
            dados.get('email', funcionario_atual['email']),
            dados.get('whatsapp', funcionario_atual['whatsapp']), 
            matricula
        ))

        conn.commit()
        return jsonify({'message': 'Funcionário atualizado com sucesso'}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@api_routes.route('/api/epi/<ca_epi>', methods=['PUT'])
def atualizar_epi(ca_epi):
    conn = None
    cursor = None
    try:
        dados = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM epi WHERE certificado_aprovacao_epi = ?", (ca_epi,))
        epi_atual = cursor.fetchone()

        if not epi_atual:
            return jsonify({'erro': 'EPI não encontrado'}), 404

        sql = """UPDATE epi 
                 SET nome_epi = ?, tipo_epi = ?, validade_certificado_aprovacao = ? 
                 WHERE certificado_aprovacao_epi = ?"""
        cursor.execute(sql, (
            dados.get('nome_epi', epi_atual['nome_epi']), 
            dados.get('tipo_epi', epi_atual['tipo_epi']), 
            dados.get('validade_certificado_aprovacao', epi_atual['validade_certificado_aprovacao']), 
            ca_epi
        ))

        conn.commit()
        return jsonify({'message': 'EPI atualizado com sucesso'}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@api_routes.route('/api/registro/<matricula>/<ca_epi>', methods=['PUT'])
def atualizar_registro(matricula, ca_epi):
    conn = None
    cursor = None
    try:
        dados = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM registros WHERE matricula_funcionario = ? AND ca_EPI = ?", (matricula, ca_epi))
        registro_atual = cursor.fetchone()

        if not registro_atual:
            return jsonify({'erro': 'Registro não encontrado'}), 404

        sql = """UPDATE registros 
                 SET data_entrega = ?, data_devolucao = ?, data_troca = ?, motivo_devolucao = ? 
                 WHERE matricula_funcionario = ? AND ca_epi = ?"""
        cursor.execute(sql, (
            dados.get('data_entrega', registro_atual['data_entrega']), 
            dados.get('data_devolucao', registro_atual['data_devolucao']), 
            dados.get('data_troca', registro_atual['data_troca']), 
            dados.get('motivo_devolucao', registro_atual['motivo_devolucao']), 
            matricula, ca_epi
        ))

        conn.commit()
        return jsonify({'message': 'Registro atualizado com sucesso'}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# ============ DELETE ============

@api_routes.route('/api/funcionario/<matricula>', methods=['DELETE'])
def deletar_funcionario(matricula):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM funcionarios WHERE matricula_funcionario = ?"
        cursor.execute(sql, (matricula,))
        conn.commit()
        return jsonify({'message': 'Funcionário deletado com sucesso'}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@api_routes.route('/api/epi/<ca_epi>', methods=['DELETE'])
def deletar_epi(ca_epi):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM epi WHERE certificado_aprovacao_epi = ?"
        cursor.execute(sql, (ca_epi,))
        conn.commit()
        return jsonify({'message': 'EPI deletado com sucesso'}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@api_routes.route('/api/registro/<matricula>/<ca_epi>', methods=['DELETE'])
def deletar_registro(matricula, ca_epi):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM registros WHERE matricula_funcionario = ? AND ca_epi = ?"
        cursor.execute(sql, (matricula, ca_epi))
        conn.commit()
        return jsonify({'message': 'Registro deletado com sucesso'}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# ============ NOTIFICAÇÕES DE VENCIMENTO ============

@api_routes.route('/api/notificacoes/verificar', methods=['POST'])
def verificar_vencimentos():
    conn = None
    cursor = None
    try:
        dados = request.get_json(silent=True) or {}
        dias_alerta = int(dados.get('dias_alerta', 30))

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                r.matricula_funcionario,
                r.ca_EPI,
                e.nome_epi,
                e.tipo_epi,
                e.validade_certificado_aprovacao
            FROM registros r
            JOIN epi e ON r.ca_EPI = e.certificado_aprovacao_epi
            WHERE e.validade_certificado_aprovacao IS NOT NULL
        """)

        registros_epi = [dict(row) for row in cursor.fetchall()]
        notificacoes_criadas = 0
        data_hoje = datetime.now().date()

        for reg in registros_epi:
            data_vencimento = reg['validade_certificado_aprovacao']
            if not data_vencimento:
                continue

            # Conversão segura do SQLite String para Datetime
            if isinstance(data_vencimento, str):
                try:
                    data_vencimento = datetime.strptime(data_vencimento[:10], '%Y-%m-%d').date()
                except ValueError:
                    continue

            dias_para_vencimento = (data_vencimento - data_hoje).days

            if dias_para_vencimento < 0 or dias_para_vencimento > dias_alerta:
                continue

            cursor.execute("""
                SELECT id
                FROM notificacoes_vencimento
                WHERE ca_epi = ?
                  AND matricula_funcionario = ?
                  AND enviado = FALSE
            """, (reg['ca_EPI'], reg['matricula_funcionario']))

            if cursor.fetchone():
                continue

            cursor.execute("""
                INSERT INTO notificacoes_vencimento
                (ca_epi, matricula_funcionario, dias_para_vencimento, data_verificacao, enviado)
                VALUES (?, ?, ?, DATETIME('now', 'localtime'), FALSE)
            """, (reg['ca_EPI'], reg['matricula_funcionario'], dias_para_vencimento))
            
            notificacoes_criadas += 1

        conn.commit()
        return jsonify({
            'message': f'{notificacoes_criadas} notificação(ões) de vencimento criada(s)',
            'notificacoes_criadas': notificacoes_criadas,
            'dias_alerta': dias_alerta
        }), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@api_routes.route('/api/notificacoes/pendentes', methods=['GET'])
def obter_notificacoes_pendentes():
    conn = None
    cursor = None
    try:
        matricula = request.args.get('matricula')
        conn = get_db_connection()
        cursor = conn.cursor()

        base_query = """
            SELECT
                n.id,
                n.ca_epi,
                n.matricula_funcionario,
                n.dias_para_vencimento,
                n.data_verificacao,
                n.enviado,
                n.data_envio,
                e.nome_epi,
                e.tipo_epi,
                e.validade_certificado_aprovacao,
                f.nome_funcionario,
                f.telefone,
                f.whatsapp
            FROM notificacoes_vencimento n
            JOIN epi e ON n.ca_epi = e.certificado_aprovacao_epi
            JOIN funcionarios f ON n.matricula_funcionario = f.matricula_funcionario
            WHERE n.enviado = FALSE
        """

        if matricula:
            cursor.execute(base_query + " AND n.matricula_funcionario = ? ORDER BY n.dias_para_vencimento ASC, n.data_verificacao DESC", (matricula,))
        else:
            cursor.execute(base_query + " ORDER BY n.dias_para_vencimento ASC, n.data_verificacao DESC")

        notificacoes = [dict(row) for row in cursor.fetchall()]

        for notif in notificacoes:
            notif['data_verificacao'] = parse_datetime_sqlite(notif.get('data_verificacao'))
            notif['data_envio'] = parse_datetime_sqlite(notif.get('data_envio'))
            notif['validade_certificado_aprovacao'] = parse_data_sqlite(notif.get('validade_certificado_aprovacao'))

        return jsonify({
            'total': len(notificacoes),
            'notificacoes': notificacoes
        }), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@api_routes.route('/api/notificacoes/marcar-enviado/<int:notificacao_id>', methods=['PUT'])
def marcar_notificacao_enviada(notificacao_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE notificacoes_vencimento
            SET enviado = TRUE, data_envio = DATETIME('now', 'localtime')
            WHERE id = ?
        """, (notificacao_id,))

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"erro": "Notificação não encontrada"}), 404

        return jsonify({'message': 'Notificação marcada como enviada'}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@api_routes.route('/api/notificacoes/status', methods=['GET'])
def status_notificacoes():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as pendentes FROM notificacoes_vencimento WHERE enviado = FALSE")
        pendentes = cursor.fetchone()['pendentes']

        cursor.execute("SELECT COUNT(*) as enviadas FROM notificacoes_vencimento WHERE enviado = TRUE")
        enviadas = cursor.fetchone()['enviadas']

        cursor.execute("""
            SELECT COUNT(*) as criticos FROM notificacoes_vencimento
            WHERE enviado = FALSE AND dias_para_vencimento <= 7
        """)
        criticos = cursor.fetchone()['criticos']

        return jsonify({
            'pendentes': pendentes,
            'enviadas': enviadas,
            'criticos': criticos
        }), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@api_routes.route('/api/notificacoes/enviar', methods=['POST'])
def enviar_notificacoes():
    dados = request.get_json(silent=True) or {}
    tipo_envio = dados.get('tipo', 'sms').lower()

    if tipo_envio not in ('sms', 'whatsapp'):
        return jsonify({"erro": "tipo deve ser 'sms' ou 'whatsapp'"}), 400

    return _enviar_notificacoes_por_tipo(tipo_envio, dados)


def _enviar_notificacoes_por_tipo(tipo_envio, dados=None):
    conn = None
    cursor = None
    try:
        if dados is None:
            dados = request.get_json(silent=True) or {}

        matricula = dados.get('matricula')
        destinatario = dados.get('destinatario')
        content_sid = dados.get('content_sid') or os.getenv('TWILIO_CONTENT_SID')

        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        sms_from = os.getenv('TWILIO_PHONE_NUMBER')
        whatsapp_from = os.getenv('TWILIO_WHATSAPP_NUMBER')

        if not account_sid or not auth_token:
            return jsonify({"erro": "Credenciais do Twilio não configuradas"}), 500

        if tipo_envio == 'whatsapp' and not whatsapp_from:
            return jsonify({"erro": "Número do WhatsApp não configurado"}), 500

        if tipo_envio == 'sms' and not sms_from:
            return jsonify({"erro": "Número do SMS não configurado"}), 500

        client = Client(account_sid, auth_token)

        conn = get_db_connection()
        cursor = conn.cursor()

        base_query = """
            SELECT
                n.id,
                n.ca_epi,
                n.matricula_funcionario,
                n.dias_para_vencimento,
                e.nome_epi,
                e.validade_certificado_aprovacao,
                f.nome_funcionario,
                f.telefone,
                f.whatsapp
            FROM notificacoes_vencimento n
            JOIN epi e ON n.ca_epi = e.certificado_aprovacao_epi
            JOIN funcionarios f ON n.matricula_funcionario = f.matricula_funcionario
            WHERE n.enviado = FALSE
        """

        if matricula:
            cursor.execute(base_query + " AND n.matricula_funcionario = ? ORDER BY n.dias_para_vencimento ASC", (matricula,))
        else:
            cursor.execute(base_query + " ORDER BY n.dias_para_vencimento ASC")

        notificacoes = [dict(row) for row in cursor.fetchall()]
        contador_sucesso = 0

        for notif in notificacoes:
            telefone_destino = formatar_para_twilio(
                destinatario or notif.get('whatsapp') or notif.get('telefone')
            )

            if not telefone_destino:
                continue

            validade_str = parse_data_sqlite(notif.get('validade_certificado_aprovacao'))

            mensagem = (
                f"Olá {notif['nome_funcionario']}, o EPI {notif['nome_epi']} "
                f"({notif['ca_epi']}) vence em {notif['dias_para_vencimento']} dias. "
                f"Validade: {validade_str}"
            )

            if tipo_envio == 'whatsapp':
                payload = {
                    'from_': f"whatsapp:{whatsapp_from}",
                    'to': f"whatsapp:{telefone_destino}"
                }

                if content_sid:
                    payload['content_sid'] = content_sid
                    payload['content_variables'] = json.dumps({
                        '1': validade_str,
                        '2': str(notif['dias_para_vencimento'])
                    })
                else:
                    payload['body'] = mensagem

                client.messages.create(**payload)
            else:
                client.messages.create(
                    body=mensagem,
                    from_=sms_from,
                    to=telefone_destino
                )

            cursor.execute("""
                UPDATE notificacoes_vencimento
                SET enviado = TRUE, data_envio = DATETIME('now', 'localtime')
                WHERE id = ?
            """, (notif['id'],))
            contador_sucesso += 1

        conn.commit()
        return jsonify({
            'message': f'Processamento concluído. {contador_sucesso} notificação(ões) enviada(s) por {tipo_envio}',
            'enviadas': contador_sucesso,
            'tipo': tipo_envio,
            'destinatario': destinatario
        }), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# ============ ROTAS DE HTML ============

@api_routes.route('/')
def index():
    dashboard = buscarDashboard()
    panel = buscarPanel()
    return render_template('index.html', dashboard=dashboard, panel=panel)

@api_routes.route('/cadastro-funcionario')
def cadastro_funcionario():
    return render_template('cadastrar-funcionario.html')

@api_routes.route('/funcionarios')
def funcionarios():
    return render_template('funcionarios.html')

@api_routes.route('/epis')
def epis():
    return render_template('epis.html')

@api_routes.route('/cadastro-epi')
def cadastro_epi():
    return render_template('cadastrar-epi.html')

@api_routes.route('/criar-registro')
def criar_registro():
    return render_template('criar-registro.html')   

@api_routes.route('/registros')
def registros():
    return render_template('registros.html')

@api_routes.route('/atualizar-cadastros')
def atualizar_cadastros():
    return render_template('atualizar-cadastros.html')

# ============ GERAÇÃO DE GRÁFICOS ============

@api_routes.route('/api/graficos/light')
def gerarGrafico():
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM registros WHERE data_troca IS NOT NULL")
        devolvidos = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM registros WHERE data_troca IS NULL")
        nao_devolvidos = cursor.fetchone()[0]

        fig, ax = plt.subplots(figsize=(6, 4), facecolor='#f8f7ff')
        ax.set_facecolor('#f8f7ff')

        ax.pie(
            [devolvidos, nao_devolvidos],
            labels=['Devolvidos', 'Não devolvidos'],
            autopct='%1.1f%%',
            startangle=90,
            colors=['#7d6cfd', '#f59e0b'],
            wedgeprops={'edgecolor': '#f8f7ff', 'linewidth': 1.5},
            textprops={'color': '#042016', 'fontsize': 10}
        )

        ax.set_title('Situação dos EPIs', color='#042016', fontsize=12, pad=12)
        ax.axis('equal')

        buffer = BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
        buffer.seek(0)
        plt.close(fig)

        return send_file(
            buffer,
            mimetype='image/png'
        )
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()