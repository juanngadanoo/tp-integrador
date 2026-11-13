"""Prueba manual del buscador (evaluación manual de la Clase 5, sección 9).

Uso:
    python scripts/buscar.py "¿cómo configuro las credenciales?"
    python scripts/buscar.py "receta de empanadas" --umbral 0.5
"""

import argparse

from tp.recuperacion.buscador import abrir_coleccion, buscar


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("consulta")
    parser.add_argument("-k", type=int, default=3)
    parser.add_argument("--umbral", type=float, default=0.6)
    args = parser.parse_args()

    resultados = buscar(args.consulta, abrir_coleccion(), k=args.k, umbral_similitud=args.umbral)
    if not resultados:
        print("Sin resultados por encima del umbral.")
    for r in resultados:
        print(f"\n[{r['similitud']:.3f}] {r['chunk_id']}  ({r['fuente']})")
        print("   " + r["texto"][:300].replace("\n", " ") + ("..." if len(r["texto"]) > 300 else ""))


if __name__ == "__main__":
    main()
