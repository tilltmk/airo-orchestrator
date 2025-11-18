"""
Basis-Agent-Klasse für AIRO
Alle spezialisierten Agenten erben von dieser Klasse
"""

from typing import Optional, Dict, Any
from utils.llm_client import llm_client


class BaseAgent:
    """Basis-Klasse für alle AIRO-Agenten"""

    def __init__(self, agent_type: str, name: str, system_prompt: str):
        """
        Initialisiere einen Agenten

        Args:
            agent_type: Typ für LLM-Auswahl (coder, architect, etc.)
            name: Anzeigename des Agenten
            system_prompt: System-Prompt für konsistentes Verhalten
        """
        self.agent_type = agent_type
        self.name = name
        self.system_prompt = system_prompt
        self.llm = llm_client

    def execute(self, task: str, **kwargs) -> Optional[str]:
        """
        Führe eine Aufgabe aus

        Args:
            task: Die zu erledigende Aufgabe
            **kwargs: Zusätzliche Parameter für LLM

        Returns:
            Antwort des Agenten
        """
        return self.llm.generate(
            agent_type=self.agent_type,
            prompt=task,
            system_prompt=self.system_prompt,
            **kwargs
        )

    def execute_structured(
        self,
        task: str,
        schema: Dict[str, Any],
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Führe eine Aufgabe mit strukturierter JSON-Ausgabe aus

        Args:
            task: Die zu erledigende Aufgabe
            schema: JSON-Schema für Ausgabe
            **kwargs: Zusätzliche Parameter

        Returns:
            Strukturierte JSON-Daten
        """
        return self.llm.generate_structured(
            agent_type=self.agent_type,
            prompt=task,
            schema=schema,
            system_prompt=self.system_prompt
        )

    def __repr__(self):
        return f"<{self.__class__.__name__}(name='{self.name}')>"
