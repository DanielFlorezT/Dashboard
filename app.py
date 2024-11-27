# -*- coding: utf-8 -*-
from dash import Dash, html, dcc, Input, Output, State
import plotly.graph_objects as go
import requests
import pandas as pd

# URL de la API
API_URL = "http://54.164.45.184:8000/api/v1/predict"

# Configurar la aplicación Dash
app = Dash(__name__)
app.title = "Dashboard de Predicción de Riesgo de Impago"

# Layout del Dashboard
app.layout = html.Div(
    style={
        "backgroundColor": "#F7F7F7",  # Fondo general
        "fontFamily": "'Open Sans', sans-serif",
        "padding": "20px",
        "maxWidth": "1200px",
        "margin": "0 auto",
    },
    children=[
        html.H1(
            "Predicción de probabilidad del riesgo de incumplimiento de pago en clientes de tarjetas de crédito",
            style={
                "textAlign": "center",
                "color": "#4E79A7",  # Azul primario
                "paddingBottom": "10px",
            },
        ),
        html.H2(
            "Grupo 4 - Despliegue de Soluciones Analíticas",
            style={"textAlign": "center", "color": "#F28E2C"},
        ),
        html.Div(
            style={
                "backgroundColor": "#FFFFFF",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                "marginBottom": "20px",
            },
            children=[
                html.P(
                    "En el presente dashboard, puede calcularse el riesgo de que un cliente incumpla "
                    "con sus obligaciones de tarjeta de crédito. Explore diferentes combinaciones "
                    "de variables para identificar patrones y factores que más influyen en el riesgo.",
                    style={"color": "#333333", "fontSize": "16px"},
                ),
            ],
        ),
        html.Div(
            style={
                "backgroundColor": "#FFFFFF",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                "marginBottom": "20px",
            },
            children=[
                html.H3("Descripción de Variables", style={"color": "#4E79A7"}),
                html.P("Edad: Edad del cliente.", style={"color": "#555555"}),
                html.P("Límite de crédito: Monto máximo aprobado para el cliente.", style={"color": "#555555"}),
                html.P("Género: 1 para masculino, 2 para femenino.", style={"color": "#555555"}),
                html.P(
                    "Educación: Nivel de educación (1=Postgrado, 2=Universitario, etc.).",
                    style={"color": "#555555"},
                ),
                html.P("Estado Civil: 1=Casado, 2=Soltero, etc.", style={"color": "#555555"}),
                html.P(
                    "PAY_0: Estado del pago en el mes de consulta (-1=pagó a tiempo, 1=atraso de 1 mes, ..., 9=atraso de 9 meses o más).",
                    style={"color": "#555555"},
                ),
            ],
        ),
        html.Div(
            children=[
                html.H3("Panel de Entrada", style={"color": "#4E79A7"}),
                dcc.Input(id="input-limite", type="number", placeholder="Límite de Crédito", style={"margin": "10px"}),
                dcc.Input(id="input-edad", type="number", placeholder="Edad", style={"margin": "10px"}),
                dcc.Input(id="input-genero", type="number", placeholder="Género (1=Masculino, 2=Femenino)", style={"margin": "10px"}),
                dcc.Input(id="input-educacion", type="number", placeholder="Nivel de Educación (1=Postgrado, etc.)", style={"margin": "10px"}),
                dcc.Input(id="input-estado", type="number", placeholder="Estado Civil (1=Casado, etc.)", style={"margin": "10px"}),
                dcc.Input(id="input-pay0", type="number", placeholder="Historial de Pagos (PAY_0)", style={"margin": "10px"}),
                html.Button("Predecir", id="btn-prediccion", style={"backgroundColor": "#4E79A7", "color": "#FFFFFF", "marginTop": "10px"}),
            ],
        ),
        html.Div(
            id="resultado-prediccion",
            style={"marginTop": "20px", "fontSize": "18px", "fontWeight": "bold", "textAlign": "center", "color": "#E15759"},
        ),
        html.Div(
            children=[
                html.H3("Curva ROC", style={"color": "#4E79A7"}),
                dcc.Graph(id="roc-curve"),
            ],
            style={"marginTop": "20px"},
        ),
        html.Div(
            children=[
                html.H3("Factores de Influencia", style={"color": "#4E79A7"}),
                dcc.Graph(id="factores-influencia"),
            ],
            style={"marginTop": "20px"},
        ),
        html.Div(
            children=[
                html.H3("Recomendación", style={"color": "#4E79A7"}),
                html.P(id="recomendacion", style={"color": "#555555", "fontSize": "16px", "marginTop": "20px"}),
            ],
            style={"marginTop": "20px"},
        ),
        html.Div(
            style={
                "textAlign": "center",
                "padding": "20px",
                "borderTop": "1px solid #E0E0E0",
                "marginTop": "20px",
                "color": "#4E79A7",
            },
            children=[
                html.H4("Oscar Ardila - Guillermo Ariza - Paola Cifuentes - Daniel Florez Thomas / Grupo 4"),
                html.P("Despliegue de Soluciones Analíticas"),
                html.P("Universidad de los Andes - Maestría en Inteligencia Analítica de Datos"),
            ],
        ),
    ],
)

# Callback para realizar la predicción y actualizar el resultado
@app.callback(
    Output("resultado-prediccion", "children"),
    Output("roc-curve", "figure"),
    Output("factores-influencia", "figure"),
    Output("recomendacion", "children"),
    Input("btn-prediccion", "n_clicks"),
    State("input-limite", "value"),
    State("input-edad", "value"),
    State("input-genero", "value"),
    State("input-educacion", "value"),
    State("input-estado", "value"),
    State("input-pay0", "value"),
)
def actualizar_dashboard(n_clicks, limite, edad, genero, educacion, estado, pay0):
    if n_clicks:
        # Realizar la solicitud a la API
        try:
            payload = {
                "LIMIT_BAL": limite,
                "AGE": edad,
                "PAY_0": pay0,
                "SEX": genero,
                "EDUCATION": educacion,
                "MARRIAGE": estado,
            }
            response = requests.post(API_URL, json=payload, timeout=10)
            if response.status_code == 200:
                resultado = response.json()
                probabilidad = resultado["probabilidad"]
                riesgo = resultado["riesgo"]

                # Generar la curva ROC
                fpr = [0.0, 0.1, 0.2, 0.5, 0.7, 1.0]
                tpr = [0.0, 0.3, 0.5, 0.7, 0.9, 1.0]
                roc_fig = go.Figure(data=go.Scatter(x=fpr, y=tpr, mode="lines"))
                roc_fig.update_layout(title="Curva ROC", xaxis_title="FPR", yaxis_title="TPR")

                # Factores de influencia
                factores = {"Límite de Crédito": 0.5, "Edad": 0.3, "Historial de Pagos": 0.2}
                factores_df = pd.DataFrame(factores.items(), columns=["Variable", "Importancia"])
                factores_fig = go.Figure(data=[go.Bar(x=factores_df["Variable"], y=factores_df["Importancia"])])

                # Recomendación
                recomendacion = (
                    "Se recomienda establecer alertas tempranas y ajustar políticas para clientes con alto riesgo."
                )

                return (
                    f"Probabilidad de incumplimiento: {probabilidad:.2f}. Riesgo: {riesgo}",
                    roc_fig,
                    factores_fig,
                    recomendacion,
                )
            else:
                return f"Error en la predicción: {response.text}", go.Figure(), go.Figure(), ""
        except requests.exceptions.Timeout:
            return "Error: La API no respondió a tiempo.", go.Figure(), go.Figure(), ""
        except requests.exceptions.ConnectionError:
            return "Error: No se pudo conectar a la API.", go.Figure(), go.Figure(), ""
        except Exception as e:
            return f"Error: {e}", go.Figure(), go.Figure(), ""
    return "", go.Figure(), go.Figure(), ""


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)


