from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from schemas import user, catalog, client, file, comment, canal, social, agencia


class TicketBase(BaseModel):
    status: str = None
    amount: float = None


class TicketCreate(TicketBase):
    client_id: str
    catalog_id: str
    user_id: str
    canal_id: str
    social_id: str = None
    agencia_id: str


class Ticket(TicketBase):
    ticket_id: int
    # client_id: UUID
    client: client.Client
    # catalog_id: UUID
    catalog: catalog.Catalog
    # user_id: UUID
    user: user.User_public
    comment: list[comment.Comment]
    files: list[file.File_DB]
    canal: canal.Canal
    social: social.Social | None
    agencia: agencia.Agencia

    created_at: datetime

    class Config:
        orm_mode = True


class TicketUpdate(TicketCreate):
    ticket_id: str


class TicketDelete(BaseModel):
    ticket_id: str


class TicketFilter(BaseModel):
    openned_tickets: list[Ticket]
    in_progress_tickets: list[Ticket]
    closed_tickets: list[Ticket]


class TicketCount(BaseModel):
    in_progress_tickets: int
    closed_tickets: int
    comments_count: int
