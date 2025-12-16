from __future__ import annotations

import logging
import requests
from langchain_core.tools import tool

logger = logging.getLogger("langgraph-demo.tool.weather")


@tool(
    "get_weather",
    description=(
        "Obtiene el clima actual por ubicación. "
        "Entrada: location (ciudad o lugar, ej: 'Medellín'). "
        "Salida: resumen con temperatura, viento y humedad."
    ),
)
def get_weather(location: str) -> str:
    """
    Tool de clima GRATIS (Open-Meteo):
    1) geocoding: location -> lat/lon
    2) forecast current: lat/lon -> temperatura, viento, etc.

    Logs:
      - entrada location
      - geocoding ok/no
      - forecast ok/no
      - errores con stacktrace
    """
    logger.info("🌤️ [TOOL weather] Ejecutando get_weather")
    logger.debug(f"🌤️ [TOOL weather] location (raw): {location!r}")

    location = (location or "").strip()
    if not location:
        logger.warning("🌤️ [TOOL weather] location vacío -> saliendo")
        return "No recibí ubicación. Por favor indica una ciudad (ej: 'Medellín')."

    try:
        # 1) Geocoding
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {"name": location, "count": 1, "language": "es", "format": "json"}

        logger.info(f"🌤️ [TOOL weather] Geocoding -> {location}")
        geo = requests.get(geo_url, params=geo_params, timeout=15)
        geo.raise_for_status()
        geo_data = geo.json()

        results = geo_data.get("results") or []
        if not results:
            logger.warning(f"🌤️ [TOOL weather] No encontré resultados para: {location}")
            return (
                f"No encontré la ubicación '{location}'. "
                "Prueba con ciudad y país (ej: 'Medellín, Colombia')."
            )

        place = results[0]
        name = place.get("name", location)
        admin1 = place.get("admin1", "")
        country = place.get("country", "")
        lat = place.get("latitude")
        lon = place.get("longitude")

        logger.info(f"🌤️ [TOOL weather] Ubicación resuelta: {name}, {admin1}, {country} ({lat}, {lon})")

        # 2) Forecast actual
        forecast_url = "https://api.open-meteo.com/v1/forecast"
        forecast_params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m",
            "timezone": "auto",
        }

        logger.info("🌤️ [TOOL weather] Consultando forecast actual")
        fc = requests.get(forecast_url, params=forecast_params, timeout=15)
        fc.raise_for_status()
        fc_data = fc.json()

        current = fc_data.get("current") or {}
        temp = current.get("temperature_2m")
        feels = current.get("apparent_temperature")
        hum = current.get("relative_humidity_2m")
        wind = current.get("wind_speed_10m")

        place_str = ", ".join([p for p in [name, admin1, country] if p])

        result = (
            f"Clima actual en {place_str}:\n"
            f"- Temperatura: {temp}°C (sensación: {feels}°C)\n"
            f"- Humedad: {hum}%\n"
            f"- Viento: {wind} km/h\n"
            f"(Fuente: Open-Meteo)"
        )

        logger.info("🌤️ [TOOL weather] OK -> devolviendo resultado")
        return result

    except Exception as e:
        logger.error("❌ [TOOL weather] Error consultando clima", exc_info=True)
        return (
            "Ocurrió un error consultando el clima. "
            f"Detalle técnico: {type(e).__name__}: {e}"
        )
