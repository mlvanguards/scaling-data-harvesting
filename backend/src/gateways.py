import os
from typing import Optional, Dict, Any

import httpx
from httpx import ConnectTimeout, HTTPError
from httpx._types import RequestFiles

from errors import ExternalServiceAPIError


class RapidGateway:

    def __init__(self, base_host: str = os.getenv("RAPID_API_ENDPOINT")):
        self._base_host = base_host

    def _make_request(
        self,
        path: str,
        method: str = 'GET',
        data: Optional[Dict[Any, str]] = None,
        headers: Optional[Dict[Any, str]] = None,
        params: Optional[Dict[Any, str]] = None,
        files: RequestFiles | None = None
    ):
        default_headers = {
            "Accept": "application/json",
            "x-rapidapi-ua": "RapidAPI-Playground",
            "x-rapidapi-host": self._base_host,
            "x-rapidapi-key": os.getenv("RAPID_API_KEY")
        }

        if headers:
            default_headers.update(headers)
        try:
            with httpx.Client(timeout=httpx.Timeout(10.0, read=300.0)) as client:
                response = client.request(
                    url=f'https://{self._base_host}/{path}',
                    method=method,
                    json=data,
                    headers=default_headers,
                    params=params,
                    files=files,
                )

                response.raise_for_status()
        except (ConnectionError, ConnectTimeout):
            raise ExternalServiceAPIError(503, "Service Unavailable")

        except HTTPError as e:
            raise e

        if response.text:
            return response.json()
        return None

    def list_posts(self, link: str):
        response = self._make_request("get-profile-posts", params={"linkedin_url": link, "type": "posts"})

        return response.get("data", [])

    def get_profile_link(self, name: str, keywords: str):
        response = self._make_request("google-full-profiles", method="POST", data={"name": name, "keywords": keywords})

        return response