from django import forms
from datetime import date, timedelta


class DatePickerInput(forms.DateInput):
    input_type = "date"

    @classmethod
    def get_options(cls):
        today = date.today()
        max_date = today - timedelta(days=365 * 18)
        min_date = today - timedelta(days=365 * 80)
        
        options = {
            "format": "mm-dd-yyyy",
            "maxDate": max_date.strftime("%m-%d-%Y"),
            "minDate": min_date.strftime("%m-%d-%Y"),
        }
        
        return options

    

class TimePickerInput(forms.TimeInput):
    input_type = "time"


class DateTimePickerInput(forms.DateTimeInput):
    input_type = "datetime"
