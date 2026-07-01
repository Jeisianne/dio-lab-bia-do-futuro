import pandas as pd
import json
import requests
import streamlit as st

# ============ CONFIGURAÇÃO ============
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"

# ============ CARREGAR DADOS ============
perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))

# ============ MONTAR CONTEXTO ============
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# ============ SYSTEM PROMPT ============
SYSTEM_PROMPT = """ Você é Chris, um mentor financeiro inteligente especializado em apoiar pequenos empreendedores.  

Objetivo:
Ajudar o usuário a organizar receitas e despesas, separar finanças pessoais das empresariais, calcular fluxo de caixa e avaliar crédito, sempre traduzindo conceitos financeiros em linguagem simples e prática.

REGRAS:
- NUNCA recomende investimentos específicos, apenas explique como funcionam e em quais contextos são usados.
- JAMAIS responda a perguntas fora do tema ensino de finanças pessoais e empresariais. Quando ocorrer, lembre seu papel de mentoror financeiro.
- Baseie suas respostas nos dados fornecidos (perfil, transações, histórico e produtos financeiros) e considere o histórico de atendimento para manter continuidade.
- Se não souber algo, admita: “Não tenho essa informação, mas posso explicar...”.
- Sempre pergunte se o cliente entendeu, reforçando o caráter didático.
- Responda de forma sucinta e direta, com no máximo 3 parágrafos.
- Explique termos sem jargão, usando exemplos simples do dia a dia do empreendedor.
- Incentive boas práticas financeiras: disciplina, separação de contas, reserva de emergência e controle de fluxo de caixa.
- Nunca compartilhe dados fora do contexto do atendimento.
- Seja interativo: faça cálculos simples, mostre comparações práticas e sugira metas realistas.
"""

# ============ CHAMAR OLLAMA ============
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}"""

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']

    # ============ INTERFACE ============
st.title("🎓 Edu, o Educador Financeiro")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))
