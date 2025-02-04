import time

print("start")
start = time.time()

import sys
import json
from whatsapp_api_client_python import API
import google.generativeai as genai
import os
from datetime import datetime, timedelta

# Configuração das APIs
ID_INSTANCE = os.getenv("ID_INSTANCE")
API_TOKEN_INSTANCE = os.getenv("API_TOKEN_INSTANCE")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Inicialização das APIs
greenAPI = API.GreenApi(ID_INSTANCE, API_TOKEN_INSTANCE)
genai.configure(api_key=GEMINI_API_KEY)

today = datetime.now()
previous_day = today - timedelta(days=1)

# Função para obter mensagens não lidas de um grupo específico
def get_unread_messages(group_id):
	notifications = greenAPI.journals.getChatHistory(group_id, 200)
	messages = []	
	for notification in notifications.data:
		dt = datetime.fromtimestamp(notification['timestamp'])
		if 'textMessage' not in notification:
			continue 
		if dt > previous_day and dt < today:
			messages.append(str(dt)+":"+notification['textMessage'])

	return messages

# Função para resumir mensagens usando a API do Gemini
def summarize_messages(messages):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = "Resuma as seguintes mensagens retornando os topicos mais importantes:\n" + "\n".join(messages)
    response = model.generate_content(prompt)
    return response.text

# Função para enviar mensagem via Green API
def send_message(to, message):
    result = greenAPI.sending.sendMessage(f"{to}@c.us", message)
    return result

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Uso: <group_id> <phone_number>")
		sys.exit(1)

	GROUP_ID = sys.argv[1]  # ID do grupo passado como argumento
	PHONE_NUMBER = sys.argv[2]  # Número de telefone para receber o resumo

	print("Grupo ID:", GROUP_ID)
	print("Número de telefone:", PHONE_NUMBER)
    # Passo 1: Obter mensagens não lidas do grupo
	unread_messages = get_unread_messages(GROUP_ID)
	if unread_messages:
		# Passo 2: Resumir mensagens usando Gemini
		summary = summarize_messages(unread_messages)
		# Passo 3: Enviar resumo para o número especificado via WhatsApp
		send_result = send_message(PHONE_NUMBER, summary)

		print("Resumo enviado com sucesso:", send_result)
	else:
		print("Nenhuma mensagem não lida encontrada no grupo.")

#print with 2 decimal places
print("finished||elapsed time: ", round(time.time()-start, 2)," s")
