"""
Clase para el uso de Assistants (Beta) con ThunderBot

En esta clase hemos creado un asistente llamado ThunderBot, y luego accedido a él para enviarle un mensaje a través de un hilo.

Después hemos ejecutado el asistente y hemos obtenido los pasos que ha realizado para responder a nuestro mensaje (incluyendo el uso de la herramienta Code Interpreter si es necesario).

Finalmente, hemos obtenido la respuesta del asistente y hemos impreso los pasos que ha realizado para responder a nuestro mensaje.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
import json
import time

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Inicializa el cliente de OpenAI con la clave API obtenida de las variables de entorno
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ID del asistente ThunderBot
assistant_id = "asst_FWAd6R3awWabwkrtbepop72k"  # Reemplaza con el ID real de tu asistente si es diferente

# Crea un nuevo hilo de conversación
thread = client.beta.threads.create()
print(f"Hilo creado con ID: {thread.id}")

# Envía un mensaje del usuario al asistente ThunderBot
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Hola ThunderBot, ¿puedes ayudarme a instalar la aplicación XYZ en mi Firestick?"
)

print("Ejecutando el asistente")
# Inicia la ejecución del asistente en el hilo creado
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id
)

# Espera a que el asistente complete la respuesta
while True:
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

    if run.status == "completed":
        print("Se completó la respuesta")
        break
    time.sleep(1)  # Espera 1 segundo antes de verificar nuevamente

# Si la ejecución se completó, procesa los pasos realizados por el asistente
if run.status == "completed":
    # Obtiene los pasos realizados durante la ejecución
    run_steps = client.beta.threads.runs.steps.list(
        thread_id=thread.id,
        run_id=run.id
    )

    # Itera sobre cada paso para identificar y procesar las llamadas a herramientas
    for step in run_steps:
        if step.step_details.type == "tool_calls":
            for tool_call in step.step_details.tool_calls:
                if tool_call.type == "code_interpreter":
                    print("Código Python ejecutado por el asistente:")
                    print(tool_call.code_interpreter.input)
    
    # Obtiene el último mensaje del asistente en el hilo
    messages = client.beta.threads.messages.list(
        thread_id=thread.id,
        order="desc",
        limit=1
    )
    for msg in messages:
        if msg.role == "assistant":
            for content_block in msg.content:
                print("\nRespuesta del asistente:")
                print(content_block.text.value)
