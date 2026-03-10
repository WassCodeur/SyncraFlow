from app.nodes.email import send_email
from app.nodes.logic_filter import filter_data
from app.nodes.whatsapp import send_whatsapp_message
from app.nodes.formatter import format_field
from app.models.workflows import HttpRequestConfig


def run_step(step_type, config):
    """Run a workflow step based on its type and configuration.

    Parameters:
    -----------
    step_type: str
        The type of the step to execute (e.g., "email", "filter", "http_request", "whatsapp_message", "formatter").

    config: dict
        The configuration for the step, which should match the expected structure for the given step type.

    Returns:
    --------
    str
        A message indicating the result of the step execution.
    """
    if step_type == "email":
        from app.nodes.email import send_email
        pass
        # send_email(config=config)
    elif step_type == "filter":
        from app.nodes.logic_filter import filter_data
        pass
        # filter_data(config=config)
    elif step_type == "http_request":
        from app.nodes.http_request import make_http_request
        config = HttpRequestConfig(**config)
        res = make_http_request(config=config)
        print(f"HTTP request step result: {res}")
        return res
    elif step_type == "whatsapp_message":
        from app.nodes.whatsapp import send_whatsapp_message
        # return (f"Executing whatsapp message step with config: {config}")
        # send_whatsapp_message(config=config)
    elif step_type == "formatter":
        from app.nodes.formatter import format_field
        # return (f"Executing formatter step with config: {config}")
        # format_field(config=config)
    else:
        raise ValueError(f"Unsupported step type: {step_type}")
