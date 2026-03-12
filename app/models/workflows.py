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
    type: Literal['email'] = 'email'
    to: str
    subject: str
    body: str
    action_url: Optional[str] = None
    action_text: Optional[str] = None


class FilterConfig(BaseModel):
    type: Literal["filter"]
    field_to_check: str  # ex: "amount"
    operator: Literal[">", "<", "==", "!="] = None
    value_to_compare: Union[int, float, str] = None


class HttpRequestConfig(BaseModel):
    type: Literal["http_request"] = "http_request"
    method: Literal["GET", "POST", "PUT", "DELETE",
                    "PATCH", "OPTIONS", "CONNECT", "HEAD"]
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


if __name__ == "__main__":
    email_config = EmailConfig(
        to="user@example.com",
        subject="Test Email",
        body="This is a test email."
    )

    filter_config = FilterConfig(
        type="filter",
        field_to_check="amount",
        operator=">",
        value_to_compare=100
    )

    http_request_config = HttpRequestConfig(
        type="http_request",
        method="GET",
        url="http://127.0.0.1:8080/user/me",
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ3YXNzNTYiLCJleHAiOjE3NzMyNzU1MzV9._x-MPcVbRWBha2UpbsSAjCuvDxOSPzCAr9ecEbADJzM"},
        body={"key": "value"}
    )
    email_config.model_dump()
    filter_config.model_dump()

    print(http_request_config.model_dump())
