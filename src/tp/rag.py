"""Pipeline RAG end-to-end — CHECKPOINT CLASE 6.

consulta -> recuperación (CP5) -> umbral -> contexto con presupuesto
-> prompt delimitado con citas -> generación (LLMProvider, CP3) -> registro.
"""

import re

from tp.llm.factory import get_provider
from tp.recuperacion.buscador import abrir_coleccion, buscar

# Valores elegidos en la Clase 6 (ver docs/decisiones.md)
K = 3
UMBRAL_SIMILITUD = 0.6
MAX_CARACTERES_CONTEXTO = 2600
SIN_EVIDENCIA = "No encontré evidencia suficiente en el corpus para responder esta pregunta."

SYSTEM_RAG = (
    "Sos un asistente que responde preguntas usando EXCLUSIVAMENTE la evidencia provista. "
    "No uses conocimiento propio ni inventes información que no esté en la evidencia."
)

registro_consultas = [] 


def armar_bloques_con_presupuesto(chunks, max_caracteres):
    bloques, total = [], 0
    for i, c in enumerate(chunks):
        bloque = f"[{i+1}] (fuente: {c['fuente']}) {c['texto']}"
        if total + len(bloque) > max_caracteres:
            if not bloques:
                bloques.append(bloque[:max_caracteres])
            break
        bloques.append(bloque)
        total += len(bloque)
    return bloques


def armar_prompt(consulta, contexto):
    return f"""<evidencia>
{contexto}
</evidencia>

<pregunta>
{consulta}
</pregunta>

Respondé la pregunta usando solo la evidencia. Si la evidencia no alcanza, decilo explícitamente.
Citá la evidencia usada con su número entre corchetes, ej. [1]."""


def citas_invalidas(respuesta, fuentes):
    """Números citados en la respuesta ([1] o [1, 3]) que no existen en las fuentes."""
    refs_validas = [f["ref"] for f in fuentes]
    invalidas = []
    for grupo in re.findall(r"\[([\d,\s]+)\]", respuesta):
        for n in grupo.split(","):
            if n.strip() and int(n) not in refs_validas:
                invalidas.append(int(n))
    return invalidas


def rag(consulta, coleccion=None, llm=None, k=K, umbral_similitud=UMBRAL_SIMILITUD,
        max_caracteres_contexto=MAX_CARACTERES_CONTEXTO) -> dict:
    if coleccion is None:
        coleccion = abrir_coleccion()
    if llm is None:
        llm = get_provider()

    recuperados = buscar(consulta, coleccion, k=k)
    relevantes = [c for c in recuperados if c["similitud"] >= umbral_similitud]

    if not relevantes:
        respuesta = SIN_EVIDENCIA
        fuentes = []
    else:
        bloques = armar_bloques_con_presupuesto(relevantes, max_caracteres_contexto)
        usados = relevantes[:len(bloques)]
        prompt = armar_prompt(consulta, "\n\n".join(bloques))
        respuesta = llm.generate(prompt, system=SYSTEM_RAG, temperature=0.0)
        fuentes = [{"ref": i + 1, "chunk_id": c["chunk_id"], "fuente": c["fuente"]}
                   for i, c in enumerate(usados)]

    registro_consultas.append({
        "consulta": consulta,
        "chunks_recuperados": [c["chunk_id"] for c in recuperados],
        "similitudes": [round(c["similitud"], 3) for c in recuperados],
        "chunks_usados_en_contexto": [f["chunk_id"] for f in fuentes],
        "citas_invalidas": citas_invalidas(respuesta, fuentes),
    })
    return {"respuesta": respuesta, "fuentes": fuentes}
