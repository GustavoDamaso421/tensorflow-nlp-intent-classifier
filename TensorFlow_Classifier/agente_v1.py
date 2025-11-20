# agente_v1.py - Fundação do Agente Expresso Chicken

import os
import sys # Usaremos sys.exit() para parar se a chave não for encontrada
from langchain_google_genai import ChatGoogleGenerativeAI

print("--- Iniciando Agente V1.0 ---")

# --- 1. Carregando a Chave de API Secreta ---
# Usamos os.getenv para ler a variável de ambiente que configuramos
google_api_key = os.getenv("GOOGLE_API_KEY")

# Verificação de Segurança Crucial!
if not google_api_key:
    print("\n!!! ERRO CRÍTICO !!!")
    print("A variável de ambiente GOOGLE_API_KEY não foi encontrada.")
    print("Por favor, siga os passos para configurá-la nas variáveis de ambiente do Windows e REINICIE o VS Code.")
    sys.exit(1) # Para o script imediatamente
else:
    # Apenas para confirmação (NUNCA imprima a chave inteira em logs reais!)
    print("Chave de API do Google encontrada com sucesso! (Primeiros 5 caracteres:", google_api_key[:5], "...)")


# --- 2. Inicializando o "Cérebro" (O LLM Gemini) ---
try:
    # Criamos uma instância do modelo de chat do Google, passando nossa chave
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key,
                               temperature=0.1) # temperature baixa para respostas mais diretas

    print("Conexão com o modelo Gemini estabelecida com sucesso!")

    # --- Teste Rápido de Conversa (Opcional, mas útil) ---
    print("\n--- Testando o Cérebro ---")
    resposta_teste = llm.invoke("Olá! Quem é você?")
    print("Resposta do Gemini:", resposta_teste.content)

except Exception as e:
    print("\n!!! ERRO AO CONECTAR COM O GEMINI !!!")
    print(f"Detalhes do erro: {e}")
    print("Verifique sua chave de API e sua conexão com a internet.")
    sys.exit(1)


print("\n--- Fundação do Agente V1.0 Pronta! ---")

# Aqui virá o resto do código (ferramentas, prompt, executor...) na próxima etapa.