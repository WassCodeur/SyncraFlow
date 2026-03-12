from app.models.workflows import HttpRequestConfig
from fastapi import HTTPException, status, Request
import requests
from json import dumps


def make_http_request(config: HttpRequestConfig, payload=None):
    """Make an HTTP request based on the provided configuration.

    Parameters
    ----------
    config : HttpRequestConfig
        The configuration for the HTTP request, including method, URL, headers, and body.

    Returns
    -------
    dict
        A dictionary containing the response status code and response body from the HTTP request.

    Raises
    ------
    HTTPException
        If the HTTP request fails or returns a non-success status code.
    """
    try:

        if config.method == "GET":
            response = requests.get(
                url=config.url, headers=config.headers)
        elif config.method == 'POST':
            response = requests.post(url=config.url, headers=config.headers)
        elif config.method == 'DELETE':
            response = requests.delete(url=config.url, headers=config.headers)
        elif config.method == 'PUT':
            response = requests.put(url=config.url, headers=config.headers)
        elif config.method == 'PATCH':
            response = requests.patch(url=config.url, headers=config.headers)
        elif config.method == 'OPTIONS':
            response = requests.options(url=config.url, headers=config.headers)
        elif config.method == 'HEAD':
            response = requests.head(url=config.url, headers=config.headers)

        if response.status_code >= 400:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"HTTP request failed with status code {response.status_code}: {response.text}"
            )

    except requests.RequestException as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"HTTP request failed: {str(e)}"
        )
    return {
        "status_code": response.status_code,
        "response_body": response.json() if response.content else None
    }


if __name__ == "__main__":
    config = HttpRequestConfig(
        method="CONNECT",
        url="https://jsonplaceholder.typicode.com/todos/1",
        headers={"Content-Type": "application/json"},
        body=None
    )
    result = make_http_request(config)
    print(result)
