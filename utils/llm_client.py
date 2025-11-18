"""
Modernisierter LLM Client für AIRO
Unterstützt Streaming, Retry-Logic, strukturierte Ausgaben und mehr
"""

import json
import time
from typing import Optional, Dict, Any, Generator, Union
import ollama
from config import models, system


class LLMClient:
    """Verbesserter LLM Client mit modernen Features"""

    def __init__(self, host: Optional[str] = None, timeout: Optional[int] = None):
        self.host = host or system.OLLAMA_HOST
        self.timeout = timeout or system.OLLAMA_TIMEOUT
        self.client = ollama.Client(host=self.host)

    def generate(
        self,
        agent_type: str,
        prompt: str,
        temperature: Optional[float] = None,
        system_prompt: Optional[str] = None,
        json_mode: bool = False,
        stream: bool = False,
        max_retries: Optional[int] = None,
    ) -> Union[str, Generator[str, None, None]]:
        """
        Generiere Antwort von LLM mit erweiterten Optionen

        Args:
            agent_type: Typ des Agents (project_planner, coder, etc.)
            prompt: Der User-Prompt
            temperature: Temperatur für Sampling (überschreibt Standard)
            system_prompt: Optionaler System-Prompt für bessere Steuerung
            json_mode: Erzwinge JSON-Ausgabe
            stream: Streame die Antwort
            max_retries: Maximale Anzahl von Wiederholungen bei Fehlern

        Returns:
            String oder Generator für gestreamte Antwort
        """
        model_name = self._get_model_for_agent(agent_type)
        temp = temperature or self._get_temperature_for_agent(agent_type)
        retries = max_retries or system.MAX_RETRIES

        messages = []

        # System-Prompt hinzufügen wenn vorhanden
        if system_prompt:
            messages.append({
                'role': 'system',
                'content': system_prompt
            })

        messages.append({
            'role': 'user',
            'content': prompt
        })

        options = {
            'temperature': temp,
        }

        # JSON-Mode aktivieren wenn unterstützt
        format_option = 'json' if json_mode and system.USE_JSON_MODE else None

        for attempt in range(retries):
            try:
                if stream and system.ENABLE_STREAMING:
                    return self._stream_response(model_name, messages, options, format_option)
                else:
                    response = self.client.chat(
                        model=model_name,
                        messages=messages,
                        options=options,
                        format=format_option
                    )
                    return response['message']['content']

            except Exception as e:
                if attempt < retries - 1:
                    wait_time = system.RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                    print(f"Fehler bei LLM-Anfrage: {e}. Wiederhole in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"Maximale Anzahl von Wiederholungen erreicht. Fehler: {e}")
                    return None

    def _stream_response(
        self,
        model_name: str,
        messages: list,
        options: dict,
        format_option: Optional[str]
    ) -> Generator[str, None, None]:
        """Streame die Antwort Token für Token"""
        stream = self.client.chat(
            model=model_name,
            messages=messages,
            options=options,
            format=format_option,
            stream=True
        )

        for chunk in stream:
            if 'message' in chunk and 'content' in chunk['message']:
                yield chunk['message']['content']

    def _get_model_for_agent(self, agent_type: str) -> str:
        """Bestimme das richtige Modell für den Agent-Typ"""
        model_mapping = {
            'project_planner': models.PROJECT_PLANNER,
            'coder': models.CODER,
            'code_reviewer': models.CODE_REVIEWER,
            'documentation': models.DOCUMENTATION,
            'architect': models.ARCHITECT,
            'test_generator': models.TEST_GENERATOR,
            'security_analyzer': models.SECURITY_ANALYZER,
            'tasknamer': models.TASKNAMER,
        }

        model = model_mapping.get(agent_type)
        if not model:
            raise ValueError(f"Unbekannter Agent-Typ: {agent_type}")
        return model

    def _get_temperature_for_agent(self, agent_type: str) -> float:
        """Bestimme die richtige Temperatur für den Agent-Typ"""
        if agent_type in ['coder', 'test_generator']:
            return system.TEMP_CODING
        elif agent_type in ['code_reviewer', 'security_analyzer']:
            return system.TEMP_REVIEW
        elif agent_type in ['project_planner', 'architect']:
            return system.TEMP_PLANNING
        elif agent_type == 'documentation':
            return system.TEMP_CREATIVE
        else:
            return 0.7  # Default

    def generate_structured(
        self,
        agent_type: str,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Generiere strukturierte JSON-Ausgabe basierend auf einem Schema

        Args:
            agent_type: Typ des Agents
            prompt: User-Prompt
            schema: JSON-Schema für die erwartete Ausgabe
            system_prompt: Optionaler System-Prompt

        Returns:
            Geparste JSON-Daten oder None bei Fehler
        """
        # Füge Schema-Beschreibung zum Prompt hinzu
        enhanced_prompt = f"""{prompt}

Please respond with valid JSON matching this schema:
{json.dumps(schema, indent=2)}

Respond ONLY with the JSON object, no additional text."""

        enhanced_system = system_prompt or ""
        enhanced_system += "\nYou are a helpful assistant that responds with valid JSON."

        response = self.generate(
            agent_type=agent_type,
            prompt=enhanced_prompt,
            system_prompt=enhanced_system,
            json_mode=True
        )

        if response:
            try:
                return json.loads(response)
            except json.JSONDecodeError as e:
                print(f"Fehler beim Parsen der JSON-Antwort: {e}")
                # Versuche JSON aus der Antwort zu extrahieren
                try:
                    # Finde JSON-Block zwischen ```json und ```
                    import re
                    json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group(1))
                except:
                    pass
        return None

    def check_model_availability(self, model_name: str) -> bool:
        """Prüfe ob ein Modell verfügbar ist"""
        try:
            models_list = self.client.list()
            return any(model['name'] == model_name for model in models_list.get('models', []))
        except Exception as e:
            print(f"Fehler beim Prüfen der Modell-Verfügbarkeit: {e}")
            return False

    def pull_model(self, model_name: str) -> bool:
        """Lade ein Modell herunter falls nicht vorhanden"""
        try:
            print(f"Lade Modell {model_name} herunter...")
            self.client.pull(model_name)
            return True
        except Exception as e:
            print(f"Fehler beim Herunterladen des Modells: {e}")
            return False


# Globale Client-Instanz
llm_client = LLMClient()
