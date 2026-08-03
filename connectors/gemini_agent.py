# connectors/gemini_agent.py
import os
import streamlit as st
import google.generativeai as genai

# Configuración de la API Key (prioriza Streamlit Secrets, luego variables de entorno)
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

# Prompt Maestro: Define el rigor académico y el formato APA 7
SYSTEM_INSTRUCTION = """
Eres un Analista Principal de Inteligencia Geopolítica y Relaciones Internacionales con nivel de Doctorado.
Tu objetivo es redactar reportes de investigación exhaustivos, rigurosos y de alta profundidad analítica para clientes corporativos.

INSTRUCCIONES ESTRUCTURALES Y METODOLÓGICAS:
1. RIGOR ACADÉMICO: Aplica teoría de Relaciones Internacionales, economía política comparada y análisis de riesgo regulatorio.
2. CITAS Y FORMATO APA 7: Toda afirmación teórica, dato histórico o marco conceptual debe incluir citas intra-texto en formato APA 7 (Ejemplo: Keohane, 1984; Transparency International, 2023).
3. ESTRUCTURA DEL REPORTE:
   - Resumen Ejecutivo de Alto Nivel.
   - Diagnóstico Político-Institucional y Gobernanza (con citas APA 7).
   - Evaluación de Riesgo Regulatorio y Operacional para el Sector.
   - Análisis de Exposición Financiera y Escenarios de Estrés.
   - Recomendaciones Estratégicas y Medidas de Mitigación Contractual.
   - Referencias Bibliográficas (al final, ordenadas alfabéticamente en formato APA 7).
4. TONO: Estrictamente profesional, neutral, ejecutivo y científico. Sin lenguaje coloquial.
"""

def generate_specialized_report(country: str, sector: str, irp_score: float, efa_usd: float, raw_data_summary: str) -> str:
    """
    Envía los datos procesados del motor a Gemini para generar un reporte analítico denso.
    """
    if not api_key:
        return "Error: No se ha configurado la clave API de Gemini (GEMINI_API_KEY)."

    try:
        # Usamos Gemini 1.5 Pro por su alta capacidad de razonamiento e investigación
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction=SYSTEM_INSTRUCTION
        )

        prompt = f"""
        Genera un reporte analítico de investigación profunda para la estrategia de entrada al mercado.

        DATOS CUANTITATIVOS DEL MOTOR POLITRISK PRO:
        - País Objetivo: {country}
        - Sector de Inversión: {sector}
        - Índice de Riesgo Político (IRP): {irp_score:.1f} / 100
        - Exposición Financiera Ajustada (EFA): USD {efa_usd:,.2f}
        
        RESUMEN DE INDICADORES TÉCNICOS:
        {raw_data_summary}

        Por favor, elabora el reporte completo en formato de investigación científica aplicada, fundamentando el contexto del país con la literatura internacional pertinente y aplicando formato APA 7.
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error al comunicarse con la inteligencia de Gemini: {str(e)}"