# canonJAM
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23471387.svg)](https://doi.org/10.5281/zenodo.23471387)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Tests](https://img.shields.io/badge/tests-33%20passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

*[Read in English](README.md)*

Método de canonicalización para detección de duplicados en estructuras
laminadas representadas con la notación JAM.

## Autor

Edgar Castillo (Independent Researcher)

## Base científica

La notación JAM está descrita en:

> Arcudia, J., Ortiz-Chi, F., Sanchez-Valenzuela, A., Aspuru-Guzik, A.,
> Merino, G. (2023). "Joining and arrangement of multilayers: A string
> representation for honeycomb layered materials." Matter, 6(5),
> 1503–1513. doi: 10.1016/j.matt.2023.02.014

canonJAM es autocontenido: sólo depende de `numpy` en tiempo de
ejecución. **No** requiere `xjam2`, y **no** vendoriza ni modifica código
de xjam2.

`xjam2` se usa únicamente en:

- los scripts de comparación en `tests/comparison/`, que verifican el
  filtro canónico contra el método por pares original;
- el ejemplo de integración opcional `examples/x_canonical.py`.

Esos scripts fallan con un mensaje claro si `xjam2` no está instalado.

> **Nota sobre la formalización.** El PDF en `docs/` es la formalización
> inicial del método. La implementación actual refleja una corrección
> posterior (confirmada por la Dra. Jessica Arcudia): para las opciones
> con *buckling*, la simetría vertical es la composición `sign·flip`, no
> `sign` y `flip` por separado. El grupo para todas las opciones tiene
> orden 12. Ver `canonjam/canonical.py` y la sección "El grupo de
> simetría" más abajo para la versión actual.

## Instalación

```bash
pip install -e .
```

Para correr los tests formales:

```bash
pip install -e ".[tests]"
```

`xjam2` **no** está en PyPI. Los scripts de comparación y el ejemplo de
integración lo esperan en `PYTHONPATH` o instalado desde el código
fuente; ver `tests/comparison/README.md`.

## Uso

```python
from canonjam import canonical_key, canonical_key_fast, filter_duplicates
import numpy as np

# Una estructura de 3 capas
a = np.array([['+0', '+j', '+j'],
              ['+0', '+j', '+j'],
              ['+0', '+j', '+j']])

# Cómputo literal: 12 evaluaciones del grupo
key = canonical_key(a, optionx=1)
print(key)

# Cómputo óptimo: 2 evaluaciones, O(k)
key = canonical_key_fast(a, optionx=1)
print(key)

# Filtrar una lista de estructuras
unique = filter_duplicates([a, a, a], optionx=1)
print(len(unique))
```

## Qué hace

JAM genera todas las configuraciones de apilamiento posibles para un
sistema de n capas. Muchas de ellas son equivalentes bajo simetría
(rotación de columnas, intercambio de columnas, inversión de capas). El
método original detecta duplicados por comparación por pares, lo cual es
O(m²). Este paquete lo reemplaza con un diccionario de claves canónicas,
lo cual es O(m).

La clave canónica de una estructura es el mínimo lexicográfico de su
órbita bajo el grupo de simetría. Dos estructuras equivalentes producen
la misma clave.

El paquete provee dos implementaciones:

- `canonical_key`: la definición literal (mínimo sobre los 12 elementos
  del grupo). Se usa en los benchmarks para correspondencia directa con
  la teoría.
- `canonical_key_fast`: el cómputo óptimo mediante ordenamiento de
  columnas (mínimo entre las concatenaciones de columnas ordenadas de la
  cadena y de su imagen bajo `v`). O(k) con constante 2. Verificado que
  coincide con `canonical_key` para las 8 opciones y n=2,3.

## El grupo de simetría

Para la opción 1 (planar monoelemental), la opción 2 (planar binaria) y
la opción 5 (planar con un token extendido de ocupación de sitio):

    G = S3 × {e, flip}

Para las opciones 3, 4, 6, 7, 8 (variantes con *buckling* y Janus):

    G = S3 × {e, sign·flip}

En todos los casos, |G| = 12.

La simetría vertical es la composición `sign·flip` (reflexión global), no
`sign` y `flip` por separado. Esto fue confirmado por la Dra. Jessica
Arcudia.

## Contenido

- `canonjam/` — el paquete (`canonical.py`, `options.py`).
- `tests/` — suite formal de tests (`test_canonical.py`,
  `test_canonical_fast.py`) y scripts de reproducibilidad autocontenidos
  (no requieren `xjam2`).
- `tests/comparison/` — scripts que comparan contra el método por pares
  original. **Requieren `xjam2`.**
- `tests/exploration/` — scripts exploratorios para la dicotomía BPL/BU
  y la clasificación de G-conjuntos (trabajo complementario;
  autocontenidos).
- `examples/` — ejemplos de uso. `pipeline.py` es autocontenido;
  `x_canonical.py` es el ejemplo de integración y requiere `xjam2`.
- `docs/` — descripción matemática formal (PDF).

## Integración con xjam2 (monkey patching)

Si ya tienes `xjam2` instalado y quieres usar canonJAM como reemplazo
directo de su filtro por pares, `examples/x_canonical.py` muestra cómo
hacerlo. Aplica *monkey patching* a `disc_equivalents` en
`xjam.libjamstd` y `xjam.libjamtdm` para usar `filter_duplicates` de
canonJAM, y luego ejecuta `x.jam` desde el directorio actual.

```bash
# 1. Instalar xjam2 (desde el código fuente; no está en PyPI)
pip install git+https://github.com/Theochem-merida/xjam2.git
# o:  export PYTHONPATH=/path/to/xjam2:$PYTHONPATH

# 2. Desde un directorio con x.jam y JAM.inp:
python3 /ruta/a/canonJAM/examples/x_canonical.py
```

El método canónico realiza ambas pasadas (`eqnum=1` y `eqnum=2`) en una
sola llamada, por lo que `eqnum` es ignorado por el reemplazo.

**Importante:** esto es un *monkey patch* sobre la API pública de xjam2.
canonJAM no modifica ni vendoriza el código fuente de xjam2. Si la API
interna de xjam2 cambia, el parche podría requerir actualización. Ver
`examples/README.md` para detalles y advertencias.

## Reproducción de los resultados teóricos

### Autocontenidos (no requieren `xjam2`)

Estos scripts reproducen los conteos de clases, las formas cerradas, los
teoremas estructurales y la verificación κ = κ'. Sólo necesitan `numpy`
y `canonjam`.

| Script | Reproduce |
|---|---|
| `tests/validation_table1.py` | Conteo de clases contra la Tabla 1 de [Arcudia2023] para n=4,5 |
| `tests/scalability.py` | Experimento de escalabilidad para n=6,8,10,12 (planar) |
| `tests/recursion_check.py` | Formas cerradas vs. fórmulas recursivas hasta n=30 |
| `tests/burnside.py`, `tests/burnside_all.py` | Conteo de puntos fijos por clase de conjugación |
| `tests/structural.py`, `tests/structural_all.py` | Órbitas vs. multiconjuntos de columnas |
| `tests/kappa_equal_kappa_prime.py` | Cómputo literal vs. óptimo de κ |

Corre cualquiera de ellos desde la raíz del repositorio:

```bash
python3 tests/validation_table1.py
python3 tests/scalability.py
python3 tests/recursion_check.py
```

### Comparación (requieren `xjam2`)

Estos scripts verifican el filtro canónico contra el método por pares
original del marco JAM. Requieren `xjam2`; ver
`tests/comparison/README.md`.

| Script | Reproduce |
|---|---|
| `tests/comparison/validation.py` | Por pares vs. canónico, por opción y n |
| `tests/comparison/full_report.py` | Reporte detallado clave por clave |
| `tests/comparison/benchmark.py` | Comparación de tiempo de filtrado |

## Cómo correr los tests formales

```bash
pytest tests/test_canonical.py tests/test_canonical_fast.py -v
```

## Licencia

MIT (ver `LICENSE`).
