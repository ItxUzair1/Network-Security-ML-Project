import sys
import traceback

def get_detailed_message(error, error_detail: sys): # type: ignore
    _, _, error_tb = error_detail.exc_info()
    filename = error_tb.tb_frame.f_code.co_filename # type: ignore
    lineno = error_tb.tb_lineno # type: ignore
    message = f"Error occurred in script: [{filename}] line number: [{lineno}] error message: [{str(error)}]"
    return message

class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys): # type: ignore
        self.error_message = get_detailed_message(error_message, error_detail)
        super().__init__(self.error_message)

    def __str__(self):
        return self.error_message
