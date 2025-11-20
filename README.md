# 🧠 Classificador de Intenções com TensorFlow/Keras (NLP Base)

Este projeto demonstra o entendimento dos fundamentos do Machine Learning e NLP (Processamento de Linguagem Natural) através da construção de um classificador de texto do zero.

**O problema resolvido:** Classificar as frases de clientes do Expresso Chicken (mais de 300 exemplos) em 9 intenções de atendimento diferentes.

## ⚙️ Arquitetura e Fundamentos

* **Modelo:** Rede Neural Sequencial com camadas de `Embedding`, `GlobalAveragePooling` e `Dense`.
* **Treinamento:** Modelo treinado do zero com 300 épocas, utilizando `sparse_categorical_crossentropy` e otimizador `Adam`.
* **Conceitos Chave:** Tokenização, Padding, Dropout (mecanismo anti-decoreba).

## 🛠️ Como Rodar (Teste)

1.  Clone o repositório.
2.  Instale as dependências: `pip install -r requirements.txt`
3.  Execute o script de treinamento: `python train_classifier.py`
4.  O script irá treinar o modelo e salvar o **Cérebro V9** (`.keras`) e os **Tradutores** (`.pickle`) na pasta.

---
*Este projeto prova o conhecimento do ciclo completo de treinamento de Machine Learning.*