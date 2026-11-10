# Actividad — Matriz de selección de modelos

Duración estimada: 25 minutos, en grupos de 2-3 personas.

## Contexto

Recordá el objetivo del [Trabajo Práctico Final Integrador](../proyecto-integrador/README.md): un sistema RAG + flujo con agentes, sobre un corpus de documentación técnica, expuesto vía API.

Antes de programar nada, hay que decidir **qué modelos usar** — no es una decisión trivial ni única: hace falta un modelo para generación/agentes y otro (o el mismo proveedor) para embeddings.

## Consigna

El curso es agnóstico de proveedor (Anthropic, OpenAI, Google, AWS Bedrock o modelos abiertos vía Ollama son todas opciones válidas para el TP). En grupo, completen la siguiente matriz comparando **al menos 3 modelos de al menos 2 proveedores distintos** (incluyendo al menos uno propietario y uno abierto), evaluando cada uno para dos roles distintos dentro del TP:

1. Como modelo de **generación / agente** (el que responde y decide qué herramienta invocar).
2. Como modelo de **embeddings** (el que vectoriza el corpus para la recuperación semántica).

### Plantilla

| Modelo (proveedor) | Rol (generación / embeddings) | Propietario / Abierto | Calidad esperada para la tarea | Costo relativo | Latencia esperada | Privacidad / dónde procesa los datos | Funciones disponibles (tool calling, structured outputs, streaming) | ¿Lo elegirían para el TP? ¿Por qué? |
|---|---|---|---|---|---|---|---|---|
| Gemini 3.5-flash-lite (Google) | generación | Propietario: el modelo es de Google, no se puede descargar, se usa por internet con una API key| Alta: en la Clase 3 entendió y clasificó bien preguntas mal escritas | Bajo: Flash-lite es la versión económica de Gemini, pensada para muchas consultas | Baja: ~1 s por respuesta corta (medido en Clases 2 y 3: entre 0,6 y 1,5 s) | En la nube de Google: las preguntas y los textos del corpus salen de la compu y se procesan en servidores de Google | Las tres: salida estructurada, tool calling y streaming (probadas en la Clase 3, celdas 15, 25 y 50) | Sí: buena calidad, rápido y barato; además uso el mismo proveedor y la misma API key para generación y embeddings |
| gemini-embedding-001 (Google) | embeddings | Propietario: es de Google, no se puede descargar, se usa por internet con la misma API key | Alta esperada: distingue documento y consulta (task_type), lo que mejora la búsqueda; se valida con búsquedas reales en las Clases 5 y 8 | Bajo: el corpus (1118 chunks) se embebe una sola vez al indexar; después es 1 llamada corta por pregunta | Todavía no medida: embeber una pregunta es 1 llamada corta; se mide en la Clase 5 | En la nube de Google: los textos del corpus y las preguntas se procesan en servidores de Google | No aplican (tool calling, salida estructurada y streaming son de generación); sí tiene task_type y dimensión elegible (uso 768 de 3072) | Sí: mismo proveedor y API key que la generación; con 768 dimensiones el índice ocupa 4 veces menos que con 3072 |
| Llama 3.2 3B (Meta, vía Ollama) | generación | Abierto: Meta publica el modelo; lo descargué (2 GB) y corre en mi compu con Ollama, sin API key | Media-baja esperada: es un modelo chico (3 mil millones de parámetros); sigue peor las instrucciones y el formato JSON que Gemini | Gratis por consulta: no se paga API; el costo es el hardware propio | No medida: en mi PC falló al correr (Ollama no funciona con mi placa de video, una AMD de 2013); un modelo local depende del hardware propio | Local: nada sale de la compu; es la opción si los datos son confidenciales | Las tres, vía Ollama: tool calling, salida estructurada y streaming | No para este TP: Gemini responde mejor y ya está integrado; sí si el corpus fuera confidencial |


### Preguntas guía

- ¿Qué modelo usarían si el corpus del TP tuviera datos confidenciales que no pueden salir de la infraestructura de la organización?
- Si el volumen de consultas esperado fuera muy alto (miles por día), ¿cómo cambia la decisión de costo/latencia?
- ¿Hay algún caso en el que convenga usar un modelo distinto para generación y para embeddings, en vez del mismo proveedor para ambos?

## Entregable

No hay entrega formal para esta actividad — es preparatoria para justificar, en la documentación final del TP (Clase 12), la elección de modelos que hizo el grupo durante toda la cursada. Guardar la matriz completada: se va a reutilizar como base del informe final.

## Criterio de éxito

La matriz está completa si cada celda tiene una justificación concreta (no solo "sí"/"no"), y el grupo puede explicar en una frase por qué eligieron el modelo de generación y el de embeddings que van a usar de acá en adelante en el curso.

**Respuestas**

1. **Datos confidenciales:** usaría un modelo abierto que corra en servidores propios, como Llama vía Ollama, porque los datos nunca salen de la organización. Con Gemini, todo lo que se pregunta y el corpus se procesan en servidores de Google. La contra: hace falta hardware adecuado (en mi PC Ollama ni siquiera pudo correr el modelo).
2. **Miles de consultas por día:** con Gemini se paga por token, así que el costo crece con cada consulta; conviene un modelo económico como Flash, prompts cortos y pocos chunks por pregunta. La latencia (~1 s) alcanza. Los embeddings del corpus se pagan una sola vez; por consulta solo se embebe la pregunta. Un modelo local no cobra por consulta, pero necesita servidores que aguanten muchos pedidos a la vez.
3. **Modelo distinto para generación y embeddings:** sí, por ejemplo si otro proveedor tiene embeddings mejores o más baratos para el idioma del corpus. Además, el modelo de embeddings es difícil de cambiar (obliga a re-embeber todo el corpus), mientras que el de generación se cambia sin tocar el índice. En mi TP uso Gemini para los dos por simplicidad: un solo proveedor y una sola API key.