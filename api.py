import enum
from typing import Annotated
from livekit.agents import llm
import logging

logger = logging.getLogger("grievance-management")
logger.setLevel(logging.INFO)

class GrievanceType(enum.Enum):
    INFRASTRUCTURE = ("infrastructure", "infrastructure@gmail.com")
    PUBLIC_SAFETY = ("public_safety", "safety@gmail.com")
    HEALTH = ("health", "health@gmail.com")
    OTHER = ("other", "other@gmail.com")

    def __init__(self, grievance_type, email):
        self.grievance_type = grievance_type
        self.email = email

class Grievance:
    def __init__(self, grievance_id, description, grievance_type):
        self.grievance_id = grievance_id
        self.description = description
        self.grievance_type = grievance_type

class AssistantFnc(llm.FunctionContext):
    def __init__(self):
        super().__init__()

        self.grievances = {}
        self.grievance_counter = 0

    @llm.ai_callable(description="File a new grievance.")
    def file_grievance(
        self,
        description: Annotated[str, llm.TypeInfo(description="Description of the grievance")],
        grievance_type: Annotated[GrievanceType, llm.TypeInfo(description="Type of the grievance")],
    ) -> str:
        self.grievance_counter += 1
        grievance_id = f"G-{self.grievance_counter}"
        new_grievance = Grievance(grievance_id, description, grievance_type)
        self.grievances[grievance_id] = new_grievance

        logger.info("Filed new grievance: %s", grievance_id)

    @llm.ai_callable(
        description="the language user has selected to have the entire conversation in. Make sure to respond in the selected language only. \
            The acceptable options of language selection are english and hindi"
    )
    def conversation_language(
        self,
        language: Annotated[str, llm.TypeInfo(description="Preferred language: 'english' or 'hindi'")],
    ) -> None:
        logger.info(f"Set the language of conversation to {language}")
        return