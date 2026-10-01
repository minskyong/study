import os
import requests
import xml.etree.ElementTree as ET
import pandas as pd

from dotenv import load_dotenv


load_dotenv()


class PortAPIClient:
    BASE_URL = "https://apis.data.go.kr/1192000"

    def __init__(self):
        self.service_key = os.getenv("PORT_API_KEY")

        if not self.service_key:
            raise ValueError(
                "PORT_API_KEY가 없습니다. .env 파일을 확인해주세요."
            )

    def get_xml(self, endpoint, params):
        url = f"{self.BASE_URL}/{endpoint}"

        request_params = {
            "serviceKey": self.service_key,
            **params
        }

        response = requests.get(
            url,
            params=request_params,
            timeout=30
        )

        response.raise_for_status()

        return response.text

    def xml_to_dataframe(self, xml_data):
        root = ET.fromstring(xml_data)

        items = []

        for item in root.findall(".//item"):
            row = {}

            for child in item:
                row[child.tag] = child.text

            items.append(row)

        return pd.DataFrame(items)