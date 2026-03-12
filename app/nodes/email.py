from app.models.workflows import EmailConfig
from smtplib import SMTP_SSL
import ssl
from app.core.config import settings, logger
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.nodes.email_utils import get_email_step_template, get_action_button_template, get_trigger_email_template


def send_email(config: EmailConfig, payload=None):
    """Send an email based on the provided configuration.

    Parameters
    ----------
    config : EmailConfig
        The configuration for the email, including recipient, subject, body, and optional action button.
    payload : dict, optional
        Additional data that can be used to customize the email content (not currently utilized in this implementation).

    Returns
    -------
    bool
        True if the email was sent successfully, False otherwise.
    """
    message = MIMEMultipart('alternative')
    message['To'] = config.to
    message['Subject'] = config.subject
    message['From'] = f"SyncraFlow <{settings.smtp_username}>"

    text = f"""\
    {config.body}
    """

    action_button = get_action_button_template(
        config.action_url, config.action_text)
    html = get_email_step_template(details_blocks=config.body, business_name="SyncraFlow", title=config.subject,
                                   action_button=action_button)

    text_part = MIMEText(text, 'plain')
    html_part = MIMEText(html, 'html')

    message.attach(text_part)
    message.attach(html_part)

    context = ssl.create_default_context()

    try:
        with SMTP_SSL(host=settings.smtp_server, port=settings.smtp_port, context=context) as server:
            logger.info(
                f"Connecting to SMTP server {settings.smtp_server}:{settings.smtp_port}")
            server.login(user=settings.smtp_username,
                         password=settings.smtp_password)
            server.send_message(message)
    except Exception as e:
        logger.error(f"Error while sending the email: {e}")
        return False
