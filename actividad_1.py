# Para ejecutar: streamlit run .\Actividad_CND_E1.py
import streamlit as st
import pandas as pd
import time

# Configuración de la página a pantalla completa (modo wide)
st.set_page_config(
    page_title="Actividad - CND E1",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos personalizados con animaciones fluidas y transiciones estilo Wayground
st.markdown("""
    <style>
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes popIn {
        0% { transform: scale(0.95); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    @keyframes crownPulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    .main-title {
        color: #1E3A8A;
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
        animation: fadeInUp 0.6s ease-out;
    }
    .subtitle {
        color: #4B5563;
        font-size: 18px;
        text-align: center;
        margin-bottom: 35px;
        animation: fadeInUp 0.8s ease-out;
    }
    .pregunta-container {
        animation: popIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
    }
    .etapa-header {
        background-color: #1E3A8A;
        color: white;
        padding: 14px 24px;
        border-radius: 12px 12px 0 0;
        font-weight: bold;
        font-size: 20px;
        margin-top: 15px;
    }
    .etapa-body {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-top: none;
        padding: 28px;
        border-radius: 0 0 12px 12px;
        margin-bottom: 20px;
        box-shadow: 0 10px 15px -3px rgba(30, 58, 138, 0.05);
    }
    .pregunta-txt {
        font-size: 18px;
        font-weight: 600;
        color: #1F2937;
        margin-bottom: 15px;
    }
    code {
        background-color: #EDF2F7;
        padding: 4px 8px;
        border-radius: 6px;
        font-family: 'Courier New', Courier, monospace;
        color: #B7791F;
        font-weight: bold;
    }
    pre code { color: #2D3748; font-weight: normal; }
    
    /* Botones */
    div.stButton > button {
        background-color: #1E3A8A !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.2s ease-in-out !important;
    }
    div.stButton > button:hover {
        background-color: #2563EB !important;
        transform: translateY(-2px) !important;
    }
    .btn-siguiente div.stButton > button {
        background-color: #10B981 !important;
    }
    .btn-siguiente div.stButton > button:hover {
        background-color: #059669 !important;
    }
    .btn-bloqueado div.stButton > button {
        background-color: #9CA3AF !important;
        cursor: not-allowed !important;
    }
    
    /* Ganador destacado */
    .ganador-destacado {
        background-color: #FEF3C7 !important;
        border: 2px solid #F59E0B !important;
        font-weight: bold;
    }
    .corona-icon {
        display: inline-block;
        animation: crownPulse 1.5s infinite ease-in-out;
    }
    </style>
""", unsafe_allow_html=True)

# --- ALMACENAMIENTO DE RANKING GLOBAL (COMPARTIDO ENTRE PESTAÑAS) ---
@st.cache_resource
def obtener_ranking_global():
    return {}

ranking_global = obtener_ranking_global()

# Inicializar estados individuales por pestaña de alumno
if "usuario" not in st.session_state:
    st.session_state.usuario = ""
if "pregunta_actual" not in st.session_state:
    st.session_state.pregunta_actual = 1
if "validado" not in st.session_state:
    st.session_state.validado = False
if "correcto" not in st.session_state:
    st.session_state.correcto = False
if "puntaje" not in st.session_state:
    st.session_state.puntaje = 0
if "penalizacion_activa" not in st.session_state:
    st.session_state.penalizacion_activa = False

# Título Principal fijo
st.markdown("<div class='main-title'>🚀 Desafío CND - Encuentro 1</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Demuestra tus conocimientos y compite por el primer lugar en el podio.</div>", unsafe_allow_html=True)

# --- PANTALLA 1: REGISTRO DE NOMBRE ---
if st.session_state.usuario == "":
    st.markdown("<div class='pregunta-container'>", unsafe_allow_html=True)
    st.markdown("<div class='etapa-header'>👋 ¡Bienvenidos al Desafío en Vivo!</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("""
        <div class='etapa-body'>
            <p class='pregunta-txt'>Antes de comenzar a responder, ingresa tu nombre o alias para registrarte en la tabla de posiciones:</p>
        </div>
        """, unsafe_allow_html=True)
        
        nombre_ingresado = st.text_input("Tu nombre/alias:", placeholder="Ej. Licha DataScience", label_visibility="collapsed")
        
        if st.button("Ingresar al Desafío"):
            if nombre_ingresado.strip() != "":
                st.session_state.usuario = nombre_ingresado.strip()
                if st.session_state.usuario not in ranking_global:
                    ranking_global[st.session_state.usuario] = 0
                st.rerun()
            else:
                st.warning("Por favor, introduce un nombre válido para poder armar el ranking.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- PANTALLA 2: JUEGO ACTIVO ---
else:
    preguntas = {
        1: {
            "titulo": "📍 1: El inicio del identificador",
            "pregunta": "¿Cuál de las siguientes opciones es una variable declarada correctamente?",
            "opciones": ["3_usuarios", "usuarios_3"],
            "correcta": "usuarios_3",
            "feedback_ok": "🎉 ¡Excelente! 'usuarios_3' es totalmente válido porque los números se permiten si no están al inicio.",
            "feedback_error": "❌ ¡Casi! Recuerda que el nombre de una variable NO puede empezar con un número. (Penalización de 5s)"
        },
        2: {
            "titulo": "📍 2: Uniendo palabras",
            "pregunta": "Queremos guardar el costo final de un producto. ¿Qué opción es válida?",
            "opciones": ["precio_total", "precio-total"],
            "correcta": "precio_total",
            "feedback_ok": "🎉 ¡Perfecto! Usar guión bajo (precio_total) es la forma correcta de separar palabras en Python.",
            "feedback_error": "❌ ¡Oh no! El guión medio (-) no está permitido en Python. (Penalización de 5s)"
        },
        3: {
            "titulo": "📍 3: El peligro de los espacios",
            "pregunta": "¿Cómo escribirías una variable para almacenar la edad de un cliente?",
            "opciones": ["mi variable = 10", "mi_variable = 10"],
            "correcta": "mi_variable = 10",
            "feedback_ok": "🎉 ¡Así se hace! Mantener todo junto o usar snake_case evita los espacios prohibidos.",
            "feedback_error": "❌ ¡Cuidado! Los espacios en blanco rompen la lectura de sintaxis. (Penalización de 5s)"
        },
        4: {
            "titulo": "📍 4: Palabras con superpoderes",
            "pregunta": "Si necesitas guardar un mensaje de texto para mostrarlo después, ¿cuál deberías elegir?",
            "opciones": ["texto_imprimir = 'Resultado'", "print = 'Resultado'"],
            "correcta": "texto_imprimir = 'Resultado'",
            "feedback_ok": "🎉 ¡Brillante! 'texto_imprimir' resguarda la función incorporada de salida.",
            "feedback_error": "❌ ¡Alerta! Si usas 'print' vas a sobreescribir e inutilizar la función original. (Penalización de 5s)"
        },
        5: {
            "titulo": "📍 5: Tipos de Datos y Conversión",
            "pregunta": 'Si ejecutamos el código <code>valor = int("25")</code>, ¿de qué tipo de dato terminará siendo la variable <code>valor</code>?',
            "opciones": ["String (str)", "Entero (int)", "Flotante (float)"],
            "correcta": "Entero (int)",
            "feedback_ok": "🎉 ¡Correcto! La función int() se utiliza para transformar una cadena de caracteres numérica válida en un número entero.",
            "feedback_error": "❌ ¡Incorrecto! La función int() convierte activamente el texto a entero. (Penalización de 5s)"
        },
        6: {
            "titulo": "📍 6: Operadores y Aritmética",
            "pregunta": "¿Cuál es el resultado matemático de la siguiente operación en Python?: <code>resultado = 11 % 3</code>",
            "opciones": ["3", "2", "1"],
            "correcta": "2",
            "feedback_ok": "🎉 ¡Acertaste! El operador de porcentaje (%) devuelve el residuo o resto de la división entera.",
            "feedback_error": "❌ ¡Inténtalo de nuevo! Recuerda que % calcula el resto sobrante de la división. (Penalización de 5s)"
        },
        7: {
            "titulo": "📍 7: Control de Flujos Condicionales",
            "pregunta": "¿Qué bloque se ejecutará si declaramos <code>puntaje = 65</code> en la siguiente estructura?<br><br><pre><code>if puntaje >= 90:\n    print('Excelente')\nelif puntaje >= 70:\n    print('Aprobado')\nelse:\n    print('Repasar')</code></pre>",
            "opciones": ["Excelente", "Aprobado", "Repasar"],
            "correcta": "Repasar",
            "feedback_ok": "🎉 ¡Muy bien pensado! Como 65 no cumple los primeros límites numéricos, cae en el bloque 'else'.",
            "feedback_error": "❌ ¡Casi! Revisa con cuidado las condiciones. El valor 65 no cumple con los primeros límites establecidos. (Penalización de 5s)"
        },
        8: {
            "titulo": "📍 8: Bucles Iterativos con For",
            "pregunta": "¿Cuántas veces se imprimirá la palabra 'Hola' al ejecutar este fragmento de código?<br><br><pre><code>for i in range(3):\n    print('Hola')</code></pre>",
            "opciones": ["3 veces", "4 veces", "2 veces"],
            "correcta": "3 veces",
            "feedback_ok": "🎉 ¡Perfecto! La función range(3) genera los índices 0, 1 y 2, completando un ciclo exacto de 3 iteraciones.",
            "feedback_error": "❌ ¡Error! Recuerda que range(N) genera una secuencia que va desde 0 hasta N-1. (Penalización de 5s)"
        },
        9: {
            "titulo": "📍 9: Control de Ciclos con While",
            "pregunta": "¿Qué sucedería con la ejecución del programa si el bloque de código se define exactamente así?<br><br><pre><code>numero = 1\nwhile numero < 5:\n    print(numero)</code></pre>",
            "opciones": ["Imprime números del 1 al 4 y termina", "Se genera un ciclo infinito porque la variable 'numero' nunca cambia", "Muestra un error de sintaxis en la consola"],
            "correcta": "Se genera un ciclo infinito porque la variable 'numero' nunca cambia",
            "feedback_ok": "🎉 ¡Exacto! Al no modificar el valor de la variable de control, la condición siempre será verdadera.",
            "feedback_error": "❌ ¡Cuidado! Mira detalladamente la estructura interna del bucle. ¿Hay algo que altere el valor? (Penalización de 5s)"
        }
    }

    current_step = st.session_state.pregunta_actual

    # Layout de columnas: Izquierda para juego, Derecha para el Ranking en vivo
    col_juego, col_ranking = st.columns([2, 1])

    with col_juego:
        if current_step <= len(preguntas):
            datos = preguntas[current_step]
            
            st.markdown(f"<div class='pregunta-container'>", unsafe_allow_html=True)
            st.markdown(f"<div class='etapa-header'>{datos['titulo']} (Jugador: {st.session_state.usuario})</div>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown(f"""
                <div class='etapa-body'>        
                    <p class='pregunta-txt'>{datos['pregunta']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                seleccion = st.radio(
                    f"Opciones {current_step}:",
                    datos["opciones"],
                    key=f"radio_{current_step}",
                    label_visibility="collapsed",
                    disabled=st.session_state.penalizacion_activa
                )
                
                # Botón de Validar común
                if st.button("Validar", key=f"val_{current_step}"):
                    st.session_state.validado = True
                    if seleccion == datos["correcta"]:
                        st.session_state.correcto = True
                        st.session_state.puntaje += 1
                        ranking_global[st.session_state.usuario] = st.session_state.puntaje
                    else:
                        st.session_state.correcto = False
                
                st.markdown("</div>", unsafe_allow_html=True)

            # Lógica de Feedbacks y Penalización de 5 segundos
            if st.session_state.validado:
                if st.session_state.correcto:
                    st.success(datos["feedback_ok"])
                    st.markdown("<div class='btn-siguiente'>", unsafe_allow_html=True)
                    if st.button("Siguiente ➡️", key=f"sig_{current_step}"):
                        st.session_state.pregunta_actual += 1
                        st.session_state.validado
