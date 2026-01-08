import json
from pathlib import Path
from typing import Any
from uuid import uuid4
from datetime import date, datetime, time
import re

class StorageService:
    def __init__(self):
        self.base_path = Path('data')
        self.base_path.mkdir(parents=True, exist_ok=True)

        # Archivos por recurso
        self.files = {
            "users": self.base_path / "users.json",
            "appointments": self.base_path / "appointments.json"
        }

        # Inicializa los archivos si no existen
        for f in self.files.values():
            if not f.exists():
                f.write_text("[]")

    # --- Lectura ---
    def load(self, resource: str) -> list[dict]:
        file_path = self.files[resource]
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # --- Escritura ---
    def save(self, resource: str, data: list[dict]):
        file_path = self.files[resource]
        with open(file_path, "w", encoding="utf-8") as f:
            # AQUÍ ESTÁ EL CAMBIO: agregamos 'default'
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
                default=self._json_date_serializable
            )


    # --- Métodos específicos ---
    def load_users(self) -> list[dict]:
        return self.load("users")

    def save_users(self, users: list[dict]):
        self.save("users", users)

    # Generar un id único automáticamente
    def generate_id(self) -> str:
        return str(uuid4())

    def _json_date_serializable(self, obj):
        """Convierte objetos de fecha a string ISO para guardar en JSON."""
        if isinstance(obj, (date, datetime,time)):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")

    def _json_date_decoder(self, dct):
        """Detecta strings que parecen fechas y los convierte a objetos date/datetime."""
        date_regex = r'^\d{4}-\d{2}-\d{2}$' # Formato YYYY-MM-DD
        datetime_regex = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.*$' # Formato ISO con T

        for key, value in dct.items():
            if isinstance(value, str):
                if re.match(datetime_regex, value):
                    try:
                        dct[key] = datetime.fromisoformat(value)
                    except ValueError: pass
                elif re.match(date_regex, value):
                    try:
                        dct[key] = date.fromisoformat(value)
                    except ValueError: pass
        return dct


storage = StorageService()