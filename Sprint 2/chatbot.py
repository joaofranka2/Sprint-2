import csv
import os
import numpy as np
import pandas as pd

# Carregar dados de perguntas e respostas do CSV
def carregar_perguntas_respostas(csv_file):
    perguntas_respostas = []
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            perguntas_respostas.append({
                "pergunta": row["pergunta"],
                "resposta": row["resposta"]
            })
    return perguntas_respostas

# Função para calcular a similaridade de texto baseada em contagem de palavras
def calcular_similaridade(texto1, texto2):
    palavras1 = set(texto1.split())
    palavras2 = set(texto2.split())
    interseccao = palavras1.intersection(palavras2)
    return len(interseccao) / (len(palavras1) + len(palavras2) - len(interseccao))

# Função para detectar a intenção da pergunta
def detectar_intencao(pergunta, perguntas_respostas):
    max_similarity = 0
    best_response = "Desculpe, eu não entendi essa pergunta."
    for pr in perguntas_respostas:
        similaridade = calcular_similaridade(pergunta, pr['pergunta'])
        if similaridade > max_similarity:
            max_similarity = similaridade
            best_response = pr['resposta']
    return best_response

# Função para responder a pergunta
def responder_pergunta(pergunta, perguntas_respostas, contexto):
    resposta = detectar_intencao(pergunta, perguntas_respostas)
    if "{nome}" in resposta and "nome" in contexto:
        resposta = resposta.replace("{nome}", contexto["nome"])
    if "{area}" in resposta and "area" in contexto:
        resposta = resposta.replace("{area}", contexto["area"])
    return resposta

# Função para salvar feedback do usuário usando pandas
def salvar_feedback(pergunta, resposta, util):
    feedback = pd.DataFrame({'Pergunta': [pergunta], 'Resposta': [resposta], 'Util': [util]})
    feedback.to_csv('feedback.csv', mode='a', header=not os.path.exists('feedback.csv'), index=False)

# Carregar perguntas e respostas do CSV
perguntas_respostas = carregar_perguntas_respostas('perguntas_respostas.csv')

# Inicializar contexto da conversa
contexto = {}

# Loop principal com personalização e feedback
print("Olá! Eu sou o Chatbot. Como posso te ajudar hoje?")
while True:
    pergunta = input("Faça uma pergunta (ou digite 'sair' para encerrar): ")
    if pergunta.lower() == "sair":
        print("Até mais!")
        break
    
    # Verificar se a pergunta é sobre personalização
    if "meu nome é" in pergunta.lower():
        nome = pergunta.split("meu nome é")[-1].strip()
        contexto["nome"] = nome
        print(f"Prazer em te conhecer, {nome}!")
        continue
    elif "minha área é" in pergunta.lower():
        area = pergunta.split("minha área é")[-1].strip()
        contexto["area"] = area
        print(f"Entendi, você trabalha na área de {area}.")
        continue
    
    resposta = responder_pergunta(pergunta, perguntas_respostas, contexto)
    print(resposta)
    
    # Solicitar feedback do usuário
    util = input("Essa resposta foi útil? (sim/não): ").strip().lower()
    util = True if util == "sim" else False if util == "não" else None
    
    if util is not None:
        salvar_feedback(pergunta, resposta, util)
        print("Obrigado pelo seu feedback!")
    else:
        print("Resposta inválida. Feedback não registrado.")
