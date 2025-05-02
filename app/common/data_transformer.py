from typing import Dict, Any, List
from lark_oapi.api.bitable.v1 import AppTableRecord


class DataTransformer:
    @staticmethod
    def select_keys(payload: Dict[str, Any], columns: List[str]):
        """select keys to extract from dictionary input"""
        data = {}

        for key, value in payload.items():
            if key in columns:
                data[key] = value

        return data
   
    @staticmethod
    def convert_raw_lark_record_to_dict(records: List[AppTableRecord], columns: List[str]):
        """convert raw field from lark to dictionary object"""
        if len(records) == 0:
            return

        items = []

        for record in records:
            data = {}
            for key in columns:
                value = record.fields.get(key)
                data[key] = value
            # include record_id
            data["record_id"] = record.record_id

            items.append(data)

        return items