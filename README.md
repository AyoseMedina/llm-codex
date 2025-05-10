![LLM Codex Logo](llm-codex.png)

# 🧠 llm-codex

**`llm-codex`** es una CLI inteligente para generar, editar y ejecutar código fuente desde lenguaje natural usando tu modelo local en LLM Studio (como LLaMA 3, Qwen o DeepSeek).

---

## 🚀 ¿Qué hace?

✅ Genera código desde prompts en lenguaje natural  
✅ Edita archivos existentes con ayuda de IA  
✅ Guarda backups automáticos y logs  
✅ Ejecuta scripts `.py` y `.sh`  
✅ Se puede usar desde cualquier carpeta (proyecto agnóstico)  
✅ 100% en consola, sin navegador

---

## ⚙️ Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/AyoseMedina/llm-codex.git
cd llm-codex
```

2. Crea un entorno virtual (opcional pero recomendado):

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instala en modo editable:

```bash
pip install -e .
```

---

## 💡 Requisitos

- Python 3.7+
- `requests`
- Tener un modelo local ejecutándose en:  
  `http://127.0.0.1:1234/v1/completions`

(LLM Studio debe estar activo y escuchar por ese puerto.)

---

## 🛠️ Comandos disponibles

### 1. 🆕 Generar código

```bash
llm-codex "crear una función en Python que calcule el factorial"
```

📝 Crea un archivo con nombre automático como:  
`crear_una_función_en.py`

---

### 2. 💾 Guardar en archivo específico

```bash
llm-codex "crear script para conectarse a PostgreSQL" conexion.py
```

---

### 3. ✏️ Editar archivo existente

```bash
llm-codex --edit script.py "mejora este código y añade logs"
```

📌 Crea un backup automático como:  
`script.py.bak_20250510_141530`

---

### 4. 🗂 Ver historial de uso

```bash
llm-codex --log
```

🧠 Muestra `.llm_codex_logs/codex_log.txt`

---

### 5. 📁 Listar archivos del proyecto

```bash
llm-codex --list
```

---

## ✅ Ejemplo completo

```bash
llm-codex "crear función que calcule si un número es primo"
# → guarda crear_funcion_que.py
# → pregunta si quieres ejecutarlo

llm-codex --edit crear_funcion_que.py "optimiza el algoritmo"
llm-codex --log
```

---

## 📦 Estructura del proyecto

```
.
├── crear_funcion_que.py
├── cualquier_otro.py
└── .llm_codex_logs/
    └── codex_log.txt
```

---

## 🛡️ Seguridad

No ejecuta código automáticamente a menos que lo confirmes.  
Los archivos modificados siempre se respaldan primero.

---

💬 Modo Chat Interactivo (--chat)
Ahora puedes interactuar con llm-codex en modo chat usando:

bash
Copiar
Editar
llm-codex --chat
¿Cómo funciona?
Te pide instrucciones en lenguaje natural (como en un chat).

Genera solo el código limpio a partir de cada entrada.

Muestra el resultado y pregunta si deseas guardarlo.

Si respondes s, se guarda con un nombre inteligente y se registra en el log.

Puedes salir en cualquier momento escribiendo :exit o :salir.

Ejemplo:
bash
Copiar
Editar
llm-codex --chat
🧠 Modo Chat Codex activado. Escribe ':exit' para salir.
🟡 Tú: crea una función en Python que invierta una cadena
💾 ¿Deseas guardar este código? [s/n]: s

---

## 🧑‍💻 Autor

Desarrollado por Ayose Medina  
2025 · IT Director · Python + LLM + Business Intelligence

