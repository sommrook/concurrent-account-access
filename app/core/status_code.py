from enum import Enum

class StatusCode(Enum):
    CODE5000 = "CODE5000", "Internal Server Error"
    CODE5001 = "CODE5001", "DataBase Error"

    @property
    def code(self):
        return self.value[0]

    @property
    def message(self):
        return self.value[1]

    def response(self):
        return {
            "response_code": self.value[0],
            "response_message": self.value[1]
        }