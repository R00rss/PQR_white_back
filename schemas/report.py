from pydantic import BaseModel
from datetime import date

class ReportFilters(BaseModel):
    report_type: str
    report_filter: str
    date_o: date = None
    date_f: date = None
    ticket_o: str = None
    ticket_f: str = None
    client_id: str = None


class Report(BaseModel):
    report: list