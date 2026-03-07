from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from typing import List, Dict, Any, Literal, Union, Optional


class WorkFlowModel(BaseModel):
    name: str


class WorkFlow(WorkFlowModel):
    id: str
    user_id: str
    trigger_slug: str
    is_active: bool


class EmailConfig(BaseModel):
    type: Literal['email']
    to: str
    subject: str
    body: str


class FilterConfig(BaseModel):
    type: Literal["filter"]
    field_to_check: str  # ex: "amount"
    operator: Literal[">", "<", "==", "!="]
    value_to_compare: Union[int, float, str]


class HttpRequestConfig(BaseModel):
    type: Literal["http_request"]
    method: Literal["GET", "POST", "PUT", "DELETE"]
    url: str
    headers: Dict[str, str] = {}
    body: Optional[Union[Dict[str, Any], str]] = None


class WhatsappMessageConfig(BaseModel):
    type: Literal["whatsapp_message"]
    to: str
    message: str


class Trigger(BaseModel):
    slug: str
    description: str


class FormatterConfig(BaseModel):
    type: Literal["formatter"]
    field_to_format: str
    format_type: Literal["currency", "date", "uppercase", "lowercase"]


class Step(BaseModel):
    type: Literal["email", "filter", "http_request",
                  "whatsapp_message", "formatter"]
    config: Union[EmailConfig, FilterConfig, HttpRequestConfig,
                  WhatsappMessageConfig, FormatterConfig] = Field(..., discriminator="type")


class StepModel(Step):
    step_id: str
    workflow_id: str
    order: int


class Steps(BaseModel):
    steps: List[Step]


class WorkflowCreated(BaseModel):
    workflow_id: str
    trigger_slug: str
