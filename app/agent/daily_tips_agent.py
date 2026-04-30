import os
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from agno.agent import Agent
from agno.models.nvidia import Nvidia

load_dotenv()

class DailyTip(BaseModel):
    """Modelo para un tip financiero individual."""
    titulo: str = Field(..., description="Título del tip financiero")
    texto: str = Field(..., description="Contenido detallado del tip financiero")
    categoria: str = Field(..., description="Categoría a la que pertenece el tip")
    day_of_week: Optional[int] = Field(
        None,
        description="Día de la semana (0=Lunes, 6=Domingo, 7=Extra). Opcional para tips individuales."
    )


class DailyTipBatch(BaseModel):
    """Modelo para un lote de 7 tips financieros semanales."""
    tips: list[DailyTip] = Field(
        ...,
        description="Lista de exactamente 7 tips financieros para la semana"
    )

    def __init__(self, **data):
        super().__init__(**data)
        if len(self.tips) != 7:
            raise ValueError(f"Se esperaban exactamente 7 tips, se recibieron: {len(self.tips)}")

class DailyTipsAgent:
    """Agente para generar tips financieros diarios usando modelos de Nvidia.

    Utiliza agno con Structured Output (Pydantic models) para garantizar
    respuestas válidas y tipadas.
    """

    # Categorías permitidas para los tips
    ALLOWED_CATEGORIES = [
        "Sueldo mínimo",
        "Combustible",
        "Alimentos",
        "Vivienda",
        "Transporte",
        "Servicios básicos",
        "Impuestos",
        "Créditos",
        "Ahorro",
        "Inversiones",
    ]

    def __init__(self):
        """Inicializa el agente con las claves de API de Nvidia con fallback."""
        self.agent = self._create_agent()
        self.session_id = "daily_tips_session"

    def _get_nvidia_api_key(self) -> str:
        """
        Obtiene la clave de API de Nvidia con manejo de fallback.
        Intenta usar las claves en orden: NVIDIA_API_KEY, NVIDIA_API_KEY_FALLBACK, etc.
        """
        api_keys = [
            os.getenv("NVIDIA_API_KEY"),
            os.getenv("NVIDIA_API_KEY_FALLBACK"),
            os.getenv("NVIDIA_API_KEY_FALLBACK2"),
            os.getenv("NVIDIA_API_KEY_FALLBACK3"),
            os.getenv("NVIDIA_API_KEY_FALLBACK4"),
        ]

        for api_key in api_keys:
            if api_key and api_key.strip():
                return api_key

        raise ValueError(
            "No NVIDIA API keys found. Please configure NVIDIA_API_KEY "
            "or its fallback variants in your .env file."
        )

    def _create_agent(self) -> Agent:
        """
        Crea y configura el agente diario de tips financieros.

        Utiliza:
        - Structured output con Pydantic models
        - Instructions explícitas para mejor control del comportamiento
        - Session tracking para contexto de conversación

        Returns:
            Agent: Agente configurado con el modelo de Nvidia
        """
        api_key = self._get_nvidia_api_key()

        model = Nvidia(
            id="qwen/qwen3-coder-480b-a35b-instruct",
            api_key=api_key,
        )

        # Instrucciones explícitas para el agente
        instructions = f"""Eres un experto en finanzas personales e inversiones con conocimiento profundo de la economía chilena.

Tu rol es generar tips financieros prácticos, accionables y específicamente diseñados para personas en Chile.

Categorías permitidas para los tips:
{', '.join(self.ALLOWED_CATEGORIES)}

REGLAS IMPORTANTES:
1. TODOS los tips DEBEN ser específicos del contexto económico chileno
2. Menciona: moneda CLP, instituciones chilenas (AFP, bancos locales, SII), indicadores chilenos (UF, IPC, salario mínimo)
3. Los consejos deben ser relevantes para la realidad financiera de Chile
4. NO menciones otros países, monedas foráneas ni contextos internacionales
5. Cada tip debe ser conciso, práctico y fácil de implementar
6. Valida que la categoría esté en la lista permitida antes de responder

Responde SIEMPRE con la estructura JSON exacta especificada, sin texto adicional.
"""

        agent = Agent(
            name="DailyTipsAgent",
            model=model,
            instructions=instructions,
            description="Agente para generar tips financieros diarios personalizados para Chile",
            session_id="daily_tips_session",
            markdown=True,
        )

        return agent

    def generate_daily_tip(self) -> DailyTip:
        """
        Genera un tip financiero diario individual.

        Returns:
            DailyTip: Objeto con titulo, texto y categoria

        Raises:
            Exception: Si falla la generación del tip
        """
        categories_str = ', '.join(self.ALLOWED_CATEGORIES)

        prompt = f"""Genera 1 tip financiero en español EXCLUSIVAMENTE PARA CHILE.

El tip debe:
1. Ser conciso, práctico y accionable
2. Pertenecer a UNA de estas categorías: {categories_str}
3. Ser específico de la economía chilena (menciona CLP, instituciones chilenas, etc.)
4. Proporcionar un consejo útil para personas en Chile

Responde SOLO con el JSON, sin texto adicional.
"""

        try:
            response = self.agent.run(prompt, output_schema=DailyTip)
            if response.content is None:
                raise ValueError("El modelo no devolvió un contenido válido")
            return response.content
        except Exception as e:
            raise Exception(f"Error al generar tip diario: {str(e)}")

def generate_weekly_tips_batch(self) -> list[DailyTip]:
        """
        Genera 7 tips financieros en UNA SOLA llamada a la IA.
        Optimizado para usar modelos gratuitos de Nvidia sin limites de rate.

        Usa Structured Output (output_schema) para validación automática.

        Returns:
            list[DailyTip]: Lista de exactamente 7 tips validados

        Raises:
            Exception: Si falla la generación o validación de tips
        """
        categories_str = ', '.join(self.ALLOWED_CATEGORIES)

        prompt = f"""Genera exactamente 7 tips financieros en español EXCLUSIVAMENTE PARA CHILE, uno para cada día de la semana (lunes a domingo).

        REQUISITOS:
        - Cada tip DEBE ser específico de la economía chilena
        - Menciona: moneda chilena (CLP), instituciones chilenas (AFP, bancos chilenos, SII), indicadores chilena (UF, IPC, salario mínimo)
        - Cada tip pertenece a UNA de estas categorías: {categories_str}
        - Los tips deben variar en categorías para dar diversidad durante la semana
        - Consejos prácticos, accionables y relevantes para personas en Chile
        - NO menciones otros países, monedas foráneas ni contextos internacionales

        Asigna day_of_week de 0 a 6 (0=Lunes, 6=Domingo).

        Responde SOLO con un array JSON de 7 objetos con estructura exacta.
        """

        try:
            response = self.agent.run(prompt, output_schema=DailyTipBatch)

            if response.content is None:
                raise ValueError("El modelo no devolvió un contenido válido")

            batch = response.content
            tips_list = batch.tips

            for i, tip in enumerate(tips_list):
                if tip.categoria not in self.ALLOWED_CATEGORIES:
                    raise ValueError(
                        f"Tip {i}: Categoría no permitida '{tip.categoria}'. "
                        f"Permitidas: {', '.join(self.ALLOWED_CATEGORIES)}"
                    )

            return tips_list
        except Exception as e:
            raise Exception(f"Error al generar lote de tips: {str(e)}")

    def get_daily_tip_safe(self) -> Optional[DailyTip]:
        """
        Genera un tip financiero diario con manejo seguro de errores.

        Propaga excepciones para mejor logging, pero devuelve None como fallback.

        Returns:
            Optional[DailyTip]: Objeto DailyTip si tiene éxito, None si hay error

        Note:
            Para mejor debugging, considera capturar la excepción en el llamador
            y loguear el error explícitamente.
        """
        try:
            return self.generate_daily_tip()
        except Exception as e:
            print(f"[ERROR] Error en DailyTipsAgent.get_daily_tip_safe(): {str(e)}")
            return None

    def get_weekly_tips_batch_safe(self) -> Optional[list[DailyTip]]:
        """
        Genera un lote de 7 tips semanales con manejo seguro de errores.

        Returns:
            Optional[list[DailyTip]]: Lista de 7 tips si tiene éxito, None si hay error

        Note:
            Para mejor debugging, considera capturar la excepción en el llamador
            y loguear el error explícitamente.
        """
        try:
            return self.generate_weekly_tips_batch()
        except Exception as e:
            print(f"[ERROR] Error en DailyTipsAgent.get_weekly_tips_batch_safe(): {str(e)}")
            return None

daily_tips_agent = DailyTipsAgent()
