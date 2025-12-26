from typing import Any

class APIResponse:
    @staticmethod
    def success(data: Any = None, message: str = "success") -> dict:
        return {"status": True, "message": message, "data": data}

    @staticmethod
    def error(message: str, code: int = 1, data: Any = None) -> dict:
        # The 'code' parameter is kept for compatibility but not used in the final dict
        return {"status": False, "message": message, "data": data}
