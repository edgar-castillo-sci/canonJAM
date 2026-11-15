# canonJAM
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23471387.svg)](https://doi.org/10.5281/zenodo.23471387)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
[![Tests](https://github.com/edgar-castillo-sci/canonJAM/actions/workflows/tests.yml/badge.svg)](https://github.com/edgar-castillo-sci/canonJAM/actions/workflows/tests.yml)
![License](https://img.shields.io/badge/license-MIT-green)

*[Read in English](README.md)*

Canonicalización de cadenas JAM (opciones 1–8) para detección de
duplicados en estructuras laminares. Implementa la instancia JAM del
marco de columnar G-sets (`P = S₃`, `K = ℤ/2`, `r = 3`, `k ≥ 2`); **no**
implementa el marco general. Depende solo de `numpy` en runtime.

## Autor

Edgar Castillo (Investigador independiente)

## Base científica

La notación JAM se describe en:

> Arcudia, J., Ortiz-Chi, F., Sanchez-Valenzuela, A., Aspuru-Guzik, A.,
> Merino, G. (2023). "Joining and arrangement of multilayers: A string
> representation for honeycomb layered materials." *Matter*, 6(5),
> 1503–1513. doi: [10.1016/j.matt.2023.02.014](https://doi.org/10.1016/j.matt.2023.02.014)

## Instalación

```bash
pip install -e .
pip install -e ".[tests]"   # para la suite de pruebas
```

## Inicio rápido

```python
from canonjam import canonical_key, canonical_key_fast, filter_duplicates
import numpy as np

# Una estructura de 3 capas
a = np.array([['+0', '+j', '+j'],
              ['+0', '+j', '+j'],
              ['+0', '+j', '+j']])

# Cómputo literal: 12 evaluaciones del grupo
print(canonical_key(a, optionx=1))

# Cómputo óptimo: 2 evaluaciones, O(k)
print(canonical_key_fast(a, optionx=1))

# Filtrar una lista de estructuras en O(m) en lugar de O(m²)
unique = filter_duplicates([a, a, a], optionx=1)
print(len(unique))   # 1
```

## API pública

| Función | Propósito |
|---|---|
| `canonical_key(a, option)` | Definición literal: mínimo sobre los 12 elementos del grupo |
| `canonical_key_fast(a, option)` | Cómputo óptimo: ordenamiento de columnas, 2 evaluaciones |
| `filter_duplicates(list, option)` | Deduplicar una lista mediante claves canónicas |
| `rows_for_option(option)` | Filas válidas de una capa para las opciones 1–8 |
| `rot`, `transp`, `flip`, `sign`, `sort_cols`, `elements_S3` | Operaciones del grupo |
| `array_to_chain`, `chain_to_array` | Conversión entre matriz y cadena JAM |

La superficie completa de la API está en [`DESIGN.md`](DESIGN.md#public-api-surface).

## Autocontenido vs. `xjam2`

`canonJAM` **no** depende de `xjam2`, y **no** vendoriza ni modifica su
código. Solo dos lugares usan `xjam2`, y ambos son opcionales:

- `tests/comparison/` — validación manual contra el método de pares
  original. Requiere `xjam2`; falla con un mensaje claro si falta.
- `examples/x_canonical.py` — ejemplo de integración opcional
  (monkey-patch de la API pública de `xjam2`).

Véase [`tests/comparison/README.md`](tests/comparison/README.md) para
instrucciones de instalación.

## Contenido del repositorio

| Directorio | Propósito |
|---|---|
| `canonjam/` | El paquete |
| `tests/` | Suite formal de pruebas (pytest) |
| `tests/comparison/` | Validación manual contra `xjam2` (opcional) |
| `reproducibility/` | Scripts que reproducen conteos y formas cerradas publicadas |
| `examples/` | Ejemplos de uso |
| `historical/` | Scripts de descubrimiento y auditoría (no mantenidos) |
| `docs/` | ADRs y convenciones |

## Artefactos relacionados

- Artículo: *Canonical Forms and Burnside Enumeration for Columnar
  G-Sets* — en preparación.
- Formalización en Lean 4: `columnar-gsets` — en preparación.

## Citar este repositorio

Véase [`CITATION.cff`](CITATION.cff). El DOI de concepto
[10.5281/zenodo.23471387](https://doi.org/10.5281/zenodo.23471387)
siempre resuelve a la última versión.

## Licencia

MIT (véase [`LICENSE`](LICENSE)).
