# Mapeo de diagnósticos psiquiátricos en lenguaje libre a códigos CIE-10  
**TFM – Máster en Aprendizaje Automático y Datos Masivos (UPM)**  

Este repositorio contiene todo el código, modelos y material auxiliar desarrollado para el Trabajo Fin de Máster (TFM) cuyo objetivo es **automatizar la codificación de notas clínicas de psiquiatría en español al estándar CIE-10** mediante técnicas de *Natural Language Processing* (NLP) y *Machine Learning* (ML).

---

## Tabla de contenidos
1. [Resumen del proyecto](#resumen-del-proyecto)  
2. [Estructura del repositorio](#estructura-del-repositorio)  
3. [Requisitos y entorno](#requisitos-y-entorno)  
4. [Datos](#datos)  
5. [Guía de uso rápido](#guía-de-uso-rápido)  
6. [Resultados principales](#resultados-principales)  
7. [Calidad del código](#calidad-del-código)  
8. [Contribuir](#contribuir)  
9. [Licencia](#licencia)  
10. [Cita](#cita)

---

## Resumen del proyecto
* **Problema**: Las notas médicas se escriben en texto libre y deben transformarse manualmente a códigos CIE‑10, un proceso costoso y propenso a errores.  
* **Solución**: Se comparan cinco líneas experimentales (similitud por *embeddings*, modelos clásicos, redes neuronales, clasificación jerárquica y LLMs fine‑tuned con QLoRA).  
* **Mejor compromiso coste‑rendimiento**: Pipeline `multilingual-e5-large` + **XGBoost multilabel** (F1 ≈ 0.725, 4 min de entrenamiento).  
* **Mejor rendimiento absoluto**: Ajuste completo del encoder + capa densa (F1 ≈ 0.757, 150 min).  
* **Hardware empleado**: Estación local con RTX 4090 (24 GB).

---

## Estructura del repositorio
```
.
├── data/                      # Dataset anonimizado (no incluido en el repo público)
├── graphics/                  # Figuras y gráficos generados
├── models/                    # Checkpoints entrenados y logs
├── optuna/                    # Estudios de búsqueda de hiperparámetros
├── requirements/              # Listas de dependencias segmentadas
├── utils.py                   # Funciones auxiliares comunes
├── 1_data_preprocessing.ipynb # Limpieza y normalización
├── 2_EDA.ipynb                # Análisis exploratorio
├── 3_Replace_codes_in_descriptions.ipynb
├── 4_Similarity_over_embeddings.ipynb
├── 5_Embeddings_to_classic_models.ipynb
├── 6_Embeddings_to_nn.ipynb
├── 7_Embeddings_and_classification_layer.ipynb
├── 8_Family_classification_model.ipynb
├── 9_LLM.ipynb
└── .pre-commit-config.yaml    # Hooks de calidad
```

---

## Requisitos y entorno en Windows
```bash
# 1. Crear entorno virtual
python3.11 -m venv venv
venv\Scripts\activate

# 2. Instalar dependencias
python.exe -m pip install --upgrade pip
pip install -r requirements/requirements_windows.txt

# 3. Instalar pre-commit
pre-commit install
```

## Requisitos y entorno en Linux
```bash
# 1. Crear entorno virtual
python3.11 -m venv venv
source venv/bin/activate

# 2. Instalar dependencias
pip install --upgrade pip
pip install -r requirements/requirements_linux.txt

# 3. Instalar pre-commit
pre-commit install
```


---

## Datos
El corpus (79 048 notas clínicas anonimizadas + etiquetas multietiqueta con 83 códigos) **no se distribuye** por razones de privacidad.  

Para reproducir los experimentos:

1. Solicitar acceso a la versión a los datos.  
2. Colocar los ficheros CSV en `data`.  
3. Ejecutar el notebook **1_data_preprocessing.ipynb**.

---

## Guía de uso rápido
| Paso | Notebook / Script | Descripción |
|------|-------------------|-------------|
| 1 | `1_data_preprocessing.ipynb` | Limpieza y normalización |
| 2 | `2_EDA.ipynb` | Estadísticas descriptivas y visualizaciones |
| 3 | `4_Similarity_over_embeddings.ipynb` | Línea base de similitud coseno |
| 4 | `5_Embeddings_to_classic_models.ipynb` | XGBoost / Random Forest multilabel |
| 5 | `6_Embeddings_to_nn.ipynb` | RN con encoder congelado |
| 6 | `7_Embeddings_and_classification_layer.ipynb` | Fine‑tune completo del encoder |
| 7 | `8_Family_classification_model.ipynb` | Enfoque jerárquico por familias |
| 8 | `9_LLM.ipynb` | Fine‑tuning QLoRA sobre Llama‑3 |

Cada notebook puede ejecutarse de forma independiente; los checkpoints resultantes se guardan en `models/`.

---

## Resultados principales
| Enfoque | F1‑test | Tiempo de entrenamiento |
|---------|--------:|-------------------------|
| Similaridad *embeddings* | 0.281 | – |
| **XGBoost multilabel** | **0.725** | **4 min** |
| RN (encoder fine‑tuned) | 0.757 | 150 min |
| Jerárquico por familias | 0.667 | 460 min |
| Llama‑3‑3B + QLoRA | 0.621 | 11 h / epoch. 33 horas en total |
---