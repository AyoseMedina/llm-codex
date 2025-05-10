import os
import sys
import requests
import subprocess
import re
from datetime import datetime

# Configuración del LLM local
LLM_URL = "http://192.168.1.12:1234/v1/completions"
HEADERS = {"Content-Type": "application/json"}

# Trabajar desde la carpeta actual
PROYECTO_DIR = os.getcwd()
LOG_DIR = os.path.join(PROYECTO_DIR, ".llm_codex_logs")
LOG_FILE = os.path.join(LOG_DIR, "codex_log.txt")

MODEL = "qwen2.5 coder"  # usado solo como referencia

os.makedirs(LOG_DIR, exist_ok=True)

def enviar_prompt(prompt):
    print(f"🔗 Conectando a: {LLM_URL}")
    prompt_formateado = f"[INST]\n{prompt}\n[/INST]"
    response = requests.post(LLM_URL, json={
        "prompt": prompt_formateado,
        "max_tokens": 1024,
        "temperature": 0.2
    }, headers=HEADERS)

    if not response.ok:
        raise RuntimeError(f"Error {response.status_code}: {response.text}")

    raw_output = response.json()["choices"][0]["text"]

    # Buscar y extraer solo el bloque de código si viene envuelto en markdown
    if "```" in raw_output:
        bloques = re.findall(r"```(?:\w+)?\n(.*?)```", raw_output, re.DOTALL)
        if bloques:
            return bloques[0].strip()

    # Si no hay bloque markdown, limpiamos posibles explicaciones
    cleaned = raw_output
    cleaned = re.sub(r"\[/?INST\]", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"<.*?>", "", cleaned)
    cleaned = re.sub(r"\*\*.*?\*\*", "", cleaned)
    cleaned = re.sub(r"(?i)(aquí tienes|explicación|nota|ejemplo|¡espero|😊|😉|😃|😄|😅|🙂|🤓).*", "", cleaned)
    cleaned = re.sub(r"(?i)(let me think|wait,|so,|then,|first,|what if|how to implement|okay).*", "", cleaned)

    return cleaned.strip()

def guardar_archivo(nombre_archivo, contenido):
    ruta = os.path.join(PROYECTO_DIR, nombre_archivo)
    modo = "w" if not os.path.exists(ruta) else "a"
    with open(ruta, modo) as f:
        f.write("\n\n# --- Generado por LLM Codex CLI ---\n")
        f.write(contenido)
    print(f"[OK] Código guardado en: {ruta}")
    return ruta

def guardar_log(prompt, nombre_archivo, codigo):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log:
        log.write(f"\n[{timestamp}]\n")
        log.write(f"Prompt: {prompt}\n")
        log.write(f"Archivo: {nombre_archivo}\n")
        log.write("Código generado:\n")
        log.write(codigo + "\n")
        log.write("="*60 + "\n")

def mostrar_log():
    if not os.path.exists(LOG_FILE):
        print("No hay historial aún.")
        return
    with open(LOG_FILE, "r") as log:
        print("\n--- Historial de prompts ---\n")
        print(log.read())

def listar_archivos():
    print("\n--- Archivos en la carpeta actual ---")
    archivos = os.listdir(PROYECTO_DIR)
    if not archivos:
        print("No hay archivos.")
    else:
        for f in archivos:
            if os.path.isfile(f) and not f.startswith("."):
                print(f"- {f}")

def editar_archivo(nombre_archivo, prompt):
    ruta = os.path.join(PROYECTO_DIR, nombre_archivo)
    if not os.path.exists(ruta):
        print(f"[ERROR] El archivo '{nombre_archivo}' no existe.")
        return

    with open(ruta, "r") as f:
        contenido_original = f.read()

    prompt_completo = f"Este es el contenido del archivo:\n{contenido_original}\n\n{prompt}"
    nuevo_contenido = enviar_prompt(prompt_completo)

    # Backup antes de sobrescribir
    backup = ruta + f".bak_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    with open(backup, "w") as b:
        b.write(contenido_original)
    print(f"[Backup] Se guardó una copia de seguridad en: {backup}")

    with open(ruta, "w") as f:
        f.write(nuevo_contenido)

    guardar_log(f"[MODIFICACIÓN] {prompt}", nombre_archivo, nuevo_contenido)
    print(f"[OK] Archivo '{nombre_archivo}' actualizado.")

def ejecutar_comando(comando):
    try:
        resultado = subprocess.run(comando, shell=True, check=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)
        print("[Salidas de ejecución]")
        print(resultado.stdout)
        if resultado.stderr:
            print("[Errores]")
            print(resultado.stderr)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Falló el comando: {comando}")
        print(e.stderr)

def detectar_extension(prompt):
    prompt = prompt.lower()
    if "bash" in prompt or "shell" in prompt:
        return ".sh"
    elif "html" in prompt:
        return ".html"
    elif "javascript" in prompt or "node.js" in prompt:
        return ".js"
    elif "sql" in prompt:
        return ".sql"
    elif "json" in prompt:
        return ".json"
    elif "markdown" in prompt or "readme" in prompt:
        return ".md"
    elif "c++" in prompt:
        return ".cpp"
    else:
        return ".py"


def modo_chat():
    print("🧠 Modo Chat Codex activo. Escribe ':exit' para salir.")
    while True:
        prompt = input("🟡 Tú: ").strip()
        if prompt.lower() in [":exit", ":salir", "salir"]:
            print("👋 Cerrando modo chat.")
            break
        if not prompt:
            continue
        try:
            codigo = enviar_prompt(prompt)
            print("\n--- Código generado ---\n")
            print(codigo)
            guardar = input("\n💾 ¿Deseas guardar este código? [s/n]: ").strip().lower()
            if guardar == "s":
                base = "_".join(prompt.split()[:5]).replace("/", "_")
                ext = detectar_extension(prompt)
                archivo = base + ext
                ruta = guardar_archivo(archivo, codigo)
                guardar_log(prompt, archivo, codigo)
        except Exception as e:
            print(f"⚠️ Error: {e}")

def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--log":
        mostrar_log()
        sys.exit(0)

    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        listar_archivos()
        sys.exit(0)

    if len(sys.argv) >= 4 and sys.argv[1] == "--edit":
        editar_archivo(sys.argv[2], sys.argv[3])
        sys.exit(0)

    if len(sys.argv) == 2 and sys.argv[1] == "--chat":
        modo_chat()
        sys.exit(0)

    if len(sys.argv) < 2:
        print("Uso:\n  llm-codex '<prompt>' [archivo]\n  llm-codex --log\n  llm-codex --list\n  llm-codex --edit archivo 'prompt'")
        sys.exit(1)

    prompt = sys.argv[1]

    if len(sys.argv) == 3:
        archivo = sys.argv[2]
    else:
        base = "_".join(prompt.split()[:5]).replace("/", "_")
        ext = detectar_extension(prompt)
        archivo = base + ext

    codigo = enviar_prompt(prompt)
    print("\n--- Código generado ---\n")
    print(codigo)

    ruta = guardar_archivo(archivo, codigo)
    guardar_log(prompt, archivo, codigo)

    opcion = input(f"\n¿Deseas ejecutar el archivo '{archivo}'? [s/n]: ").strip().lower()
    if opcion == "s":
        if archivo.endswith(".py"):
            ejecutar_comando(f"python3 {ruta}")
        elif archivo.endswith(".sh"):
            ejecutar_comando(f"bash {ruta}")
        else:
            print("Este tipo de archivo no se ejecuta automáticamente.")
