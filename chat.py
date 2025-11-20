# chat.py - Versão V9 (Com o Cérebro Super Treinado)

import tensorflow as tf
import numpy as np
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os
import re
import unicodedata
import sqlite3

# Suprime os avisos informativos do TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# =======================================================
# --- 1. CARREGANDO O CÉREBRO E OS TRADUTORES V9 ---
# =======================================================
try:
    # <<<--- MUDANÇA AQUI! Carregando o cérebro V9
    model = tf.keras.models.load_model('cerebro_chatbot_v9.keras')

    # <<<--- MUDANÇA AQUI! Carregando o tradutor de frases V9
    with open('tokenizer_v9.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # <<<--- MUDANÇA AQUI! Carregando o tradutor de intenções V9
    with open('label_map_v9.pickle', 'rb') as handle:
        label_map = pickle.load(handle)
except Exception as e:
    print(f"Erro ao carregar os arquivos do modelo V9: {e}")
    print("Por favor, execute o notebook 'Treinamento_Cerebro_V9.ipynb' para gerar os arquivos primeiro.")
    exit()

# --- DADOS TÉCNICOS ---
reverse_label_map = {v: k for k, v in label_map.items()}
# ATENÇÃO: Confirme no seu notebook V9 qual foi o max_length calculado na Célula 1 e ajuste aqui.
# Deve ser um número maior agora com os novos dados. Vou chutar 13 por enquanto.
max_length = 13 # <<<--- AJUSTE AQUI SE NECESSÁRIO!

# --- FUNÇÃO PARA "LIMPAR" TEXTO ---
def normalizar_texto(texto):
    nfkd = unicodedata.normalize('NFKD', texto); return u"".join([c for c in nfkd if not unicodedata.combining(c)]).lower()

# --- 2. MAPA DE RESPOSTAS ---
def obter_resposta(intencao, item_nome=None):
    # (A função obter_resposta continua a mesma, lendo do SQL)
    conn = None
    try:
        conn = sqlite3.connect('meu_banco_de_dados.db'); cursor = conn.cursor()
        if intencao == 'pedir_cardapio':
            cursor.execute("SELECT categoria, nome_item, variacao, preco FROM cardapio WHERE disponivel = 1 ORDER BY categoria, nome_item")
            items = cursor.fetchall()
            if not items: return "Cardápio vazio."
            resp = "Nosso cardápio:\n\n"; cat_atual = ""
            for item in items:
                cat, nome, var, preco = item
                if cat != cat_atual: resp += f"--- {cat.upper()} ---\n"; cat_atual = cat
                var_str = f" ({var})" if var != 'Único' else ""; resp += f"- {nome}{var_str}: R$ {preco:.2f}\n"
            return resp
        elif intencao == 'horario_funcionamento':
            cursor.execute("SELECT valor FROM configuracoes WHERE chave = 'horario_funcionamento'")
            res = cursor.fetchone(); return f"Horário: {res[0]}" if res else "Não achei o horário."
        else:
            resp_fixas = {'saudacao': "Olá! Expresso Chicken! Como ajudar?", 'fazer_pedido': "Ótimo! Qual item?", 'perguntar_tempo_preparo': "Preparo: 30-45 min.", 'confirmar_entrega': f"Ok, {item_nome if item_nome else 'item'} anotado. Entrega! Endereço?", 'confirmar_retirada': f"Ok, {item_nome if item_nome else 'item'} anotado. Retirada! Avisaremos!", 'consultar_taxa_entrega': "Taxa varia. Qual bairro?", 'perguntar_status': "Verifico. Qual nome/número?", 'despedida_agradecimento': "Agradeço! Boa noite!"}
            return resp_fixas.get(intencao, "Não entendi. Pode reformular?")
    except Exception as e: return f"Opa! Erro interno ({e})."
    finally:
        if conn: conn.close()


# --- 3. FUNÇÃO DE PREVISÃO ---
def prever_intencao(frase):
    # Normaliza a frase antes de prever, igual fazemos com os dados de treino!
    frase_normalizada = normalizar_texto(frase) # <<<--- Adicionado normalização aqui!
    sequence = tokenizer.texts_to_sequences([frase_normalizada])
    padded_sequence = pad_sequences(sequence, maxlen=max_length, padding='post')
    prediction = model.predict(padded_sequence, verbose=0)
    pred_idx = np.argmax(prediction)
    return reverse_label_map[pred_idx]

# --- FUNÇÃO PARA BUSCAR ITEM NO CARDÁPIO ---
def buscar_item_no_cardapio(frase_normalizada):
    # (A função buscar_item_no_cardapio continua a mesma)
    item_info = None; conn = None
    try:
        conn = sqlite3.connect('meu_banco_de_dados.db'); cursor = conn.cursor()
        cursor.execute("SELECT nome_item, variacao, preco FROM cardapio WHERE disponivel = 1")
        items_db = cursor.fetchall(); conn.close(); best_score = 0
        for nome, var, preco in items_db:
            nome_norm = normalizar_texto(nome); var_norm = normalizar_texto(var) if var != 'Único' else ''
            score = 0; p_item = nome_norm.split(); p_var = var_norm.split() if var_norm else []
            if all(p in frase_normalizada for p in p_item): score += 10
            elif any(p in frase_normalizada for p in p_item): score += 2
            if p_var and all(p in frase_normalizada for p in p_var): score += 5
            elif p_var and any(p in frase_normalizada for p in p_var): score += 1
            if score > best_score: best_score = score; item_info = (nome, var, preco)
    except Exception as e: print(f"Erro SQL buscar item: {e}")
    return item_info

# ==============================================================================
# --- 4. O LOOP PRINCIPAL V9 (COM CÉREBRO V9 E GERENCIADOR INTELIGENTE) ---
# ==============================================================================
print("======================================================")
print("Atendente Digital do Expresso Chicken V9 - Online")
print("Digite 'sair' a qualquer momento para encerrar.")
print("======================================================")

conversation_state = "IDLE"; pedido_atual = {}

while True:
    frase_usuario = input("> Você: ").strip()
    if not frase_usuario: continue
    frase_usuario_lower = frase_usuario.lower()
    frase_usuario_normalizada = normalizar_texto(frase_usuario) # Usamos a versão limpa

    if frase_usuario_lower == 'sair': print("> Expresso Chicken: Até a próxima!"); break

    # --- LÓGICA DE DECISÃO ---
    if conversation_state == "IDLE":
        intencao = prever_intencao(frase_usuario_lower) # IA decide no estado IDLE
        resposta = obter_resposta(intencao)
        print(f"> Expresso Chicken: {resposta}")
        if intencao == 'consultar_taxa_entrega': conversation_state = "WAITING_FOR_NEIGHBORHOOD"
        elif intencao == 'fazer_pedido': conversation_state = "WAITING_FOR_ITEM"
        pedido_atual = {}

    elif conversation_state == "WAITING_FOR_NEIGHBORHOOD":
        taxa = None; bairro_real = None; conn=None
        try:
            conn = sqlite3.connect('meu_banco_de_dados.db'); cursor = conn.cursor()
            cursor.execute("SELECT bairro, taxa FROM entregas"); entregas = cursor.fetchall(); conn.close()
            for b_db, t_db in entregas:
                if normalizar_texto(b_db) == frase_usuario_normalizada: bairro_real = b_db; taxa = t_db; break
        except Exception as e: print(f"Erro SQL taxa: {e}")
        if taxa is not None: resposta = f"Taxa para {bairro_real.title()}: R$ {taxa:.2f}."
        else:
             intencao = prever_intencao(frase_usuario_lower) # IA opina sobre a frase
             if intencao == 'consultar_taxa_entrega' or intencao == 'confirmar_entrega': # Se ainda parece ser sobre bairro/entrega
                 resposta = f"Não achei '{frase_usuario.title()}'. Pode verificar o nome do bairro?"
             else: # Mudou de assunto!
                 resposta_nova = obter_resposta(intencao)
                 resposta = f"{resposta_nova}\n> Expresso Chicken: (E sobre a taxa, qual bairro mesmo?)"
                 # Mantemos o estado!
        print(f"> Expresso Chicken: {resposta}")
        if taxa is not None: conversation_state = "IDLE" # Só sai se achou

    elif conversation_state == "WAITING_FOR_ITEM":
        item_info = buscar_item_no_cardapio(frase_usuario_normalizada)
        if item_info:
            nome, var, preco = item_info
            item_display = f"{nome.title()}" + (f" ({var})" if var != 'Único' else "")
            pedido_atual['item'] = item_display; pedido_atual['preco_item'] = preco
            resposta = f"Ok, {item_display}. Entrega ou retirada?"
            print(f"> Expresso Chicken: {resposta}")
            conversation_state = "WAITING_FOR_DELIVERY_CHOICE"
        else:
            intencao = prever_intencao(frase_usuario_lower)
            if intencao == 'pedir_cardapio' or intencao == 'consultar_taxa_entrega' or intencao == 'horario_funcionamento':
                 resposta_nova = obter_resposta(intencao)
                 print(f"> Expresso Chicken: {resposta_nova}")
                 print("> Expresso Chicken: Certo. E qual item gostaria?")
            elif intencao == 'saudacao' or intencao == 'despedida_agradecimento':
                 print(f"> Expresso Chicken: {obter_resposta(intencao)}")
                 conversation_state = "IDLE"; pedido_atual = {}
            else:
                 print("> Expresso Chicken: Hum, não encontrei. Pode dizer o nome do item?")

    elif conversation_state == "WAITING_FOR_DELIVERY_CHOICE":
        intencao = prever_intencao(frase_usuario_lower)
        item_nome = pedido_atual.get('item', 'N/A')
        if intencao == 'confirmar_entrega':
            pedido_atual['tipo'] = 'entrega'
            resposta = obter_resposta('confirmar_entrega', item_nome)
            conversation_state = "WAITING_FOR_ADDRESS"
        elif intencao == 'confirmar_retirada':
             pedido_atual['tipo'] = 'retirada'
             preco_item = pedido_atual.get('preco_item', 0)
             resposta = f"Retirada! Pedido: {item_nome}. Total: R${preco_item:.2f}. Avisaremos!"
             pedido_atual = {}; conversation_state = "IDLE"
        else: resposta = "Não entendi. Entrega ou retirada?"
        print(f"> Expresso Chicken: {resposta}")

    elif conversation_state == "WAITING_FOR_ADDRESS":
        endereco_cliente = frase_usuario; pedido_atual['endereco'] = endereco_cliente
        endereco_normalizado = normalizar_texto(endereco_cliente); bairro_encontrado = None; taxa_entrega = 0; conn = None
        try:
            conn = sqlite3.connect('meu_banco_de_dados.db'); cursor = conn.cursor()
            cursor.execute("SELECT bairro, taxa FROM entregas"); entregas = cursor.fetchall(); conn.close()
            best_match = None
            for b_db, t_db in entregas:
                if normalizar_texto(b_db) in endereco_normalizado:
                    best_match = (b_db, t_db); break
            if best_match: bairro_encontrado, taxa_entrega = best_match
        except Exception as e: print(f"Erro SQL taxa end: {e}")
        pedido_atual['bairro'] = bairro_encontrado; pedido_atual['taxa_entrega'] = taxa_entrega if bairro_encontrado else 0
        aviso = "" if bairro_encontrado else "\n> Expresso Chicken: (Atenção: Não identifiquei bairro p/ taxa.)"
        preco_item = pedido_atual.get('preco_item', 0)
        total = preco_item + taxa_entrega; pedido_atual['total'] = total
        comanda = f"\n--- PEDIDO ---\nItem: {pedido_atual.get('item', 'N/A')}\nEnd: {pedido_atual.get('endereco', 'N/A').title()}\nTaxa: R${taxa_entrega:.2f}\nTOTAL: R${total:.2f}\n------------\n"
        print(comanda);
        if aviso: print(aviso)
        resposta_final = f"Pedido OK! Total R$ {total:.2f}. Já preparando! Obrigado!"
        print(f"> Expresso Chicken: {resposta_final}")
        pedido_atual = {}; conversation_state = "IDLE"