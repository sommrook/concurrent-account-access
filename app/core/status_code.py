from enum import Enum

class StatusCode(Enum):
    CODE2000 = "CODE2000", "OK"

    CODE5000 = "CODE5000", "Internal Server Error"
    CODE5001 = "CODE5001", "DataBase Error"

    CODE4000 = "CODE4000", "Bad Request"

    # NOT FOUND
    CODE4101 = "CODE4101", "NOT FOUND - user not found"

    # ALREADY EXISTS
    CODE4201 = "CODE4201", "ALREADY EXISTS - user account is already exists"

    # INVALID FORMAT
    CODE4301 = "CODE4301", "INVALID FORMAT - invalid account length"
    CODE4302 = "CODE4302", "INVALID FORMAT - account contains blank"
    CODE4303 = "CODE4303", "INVALID FORMAT - invalid password format"
    CODE4304 = "CODE4304", "INVALID FORMAT - invalid email format"
    CODE4305 = "CODE4305", "INVALID FORMAT - must have enter account"
    CODE4306 = "CODE4306", "INVALID FORMAT - must have enter password"

    # INVALID INFO
    CODE4401 = "CODE4401", "INVALID INFO - invalid password"

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