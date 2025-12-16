from __future__ import annotations

import base64
import logging
import os
import uuid
from pathlib import Path

from langchain_core.tools import tool
from openai import OpenAI

logger = logging.getLogger("langgraph-demo.tool.image")


def _openai_client() -> OpenAI:
    """
    Cliente OpenAI Usado EXCLUSIVAMENTE para generación de imágenes.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta OPENAI_API_KEY (OpenAI directo)")

    return OpenAI(api_key=api_key)


@tool(
    "generate_image",
    description=(
        "Genera una imagen a partir de un prompt visual. "
        "Entrada: prompt (string). "
        "Salida: path local del PNG generado."
    ),
)
def generate_image(prompt: str) -> str:
    logger.info("🖼️ [TOOL image] Ejecutando generate_image (OpenAI directo)")
    logger.debug(f"🖼️ Prompt recibido: {prompt!r}")

    prompt = (prompt or "").strip()
    if not prompt:
        return "Prompt vacío. Ejemplo: 'Mapa minimalista de Colombia en estilo flat'."

    model = os.getenv("OPENAI_IMAGE_MODEL", "gpt-4o")
    client = _openai_client()

    # Carpeta estática para servir por FastAPI
    repo_root = Path(__file__).resolve().parents[2]
    out_dir = repo_root / "static" / "generated"
    out_dir.mkdir(parents=True, exist_ok=True)

    file_id = uuid.uuid4().hex
    out_path = out_dir / f"{file_id}.png"

    try:
        logger.info(f"🖼️ [TOOL image] Generando imagen con modelo {model}")
        result = client.images.generate(
            model=model,
            prompt=prompt,
            size="1024x1024",
        )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        out_path.write_bytes(image_bytes)
        public_base = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")

        rel_path = f"/static/generated/{out_path.name}"

        if public_base:
            full_url = f"{public_base}{rel_path}"
            logger.info(f"🖼️ [TOOL image] URL pública generada: {full_url}")
            return full_url

        # fallback (por si alguien olvida la env var)
        logger.warning("🖼️ [TOOL image] PUBLIC_BASE_URL no definida, devolviendo path relativo")
        return rel_path

    except Exception as e:
        logger.error("❌ [TOOL image] Error generando imagen con OpenAI", exc_info=True)
        return (
            "Error generando imagen con OpenAI directo.\n"
            f"Detalle técnico: {type(e).__name__}: {e}"
        )
