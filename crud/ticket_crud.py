from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from uuid import UUID

from models import (
    ticket_model,
    client_model,
    canal_model,
    social_model,
    catalog_model,
    user_model,
    catalog_user_model,
    comment_model,
    agencia_model
)

from schemas.ticket import Ticket, TicketCreate, TicketUpdate, TicketDelete
from schemas.report import ReportFilters


# **************************** TICKET **************************
# Get next ticket id
def get_next_ticket_id(db: Session):
    tickets_in_db = (
        db.query(ticket_model.Ticket)
        .order_by(ticket_model.Ticket.ticket_id.desc())
        .all()
    )

    return tickets_in_db[0].ticket_id + 1


# CREATE TICKET
def create_ticket(db: Session, ticket: TicketCreate):
    client_in_db = (
        db.query(client_model.Client)
        .filter(client_model.Client.client_id == ticket.client_id)
        .first()
    )

    if not client_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )

    catalog_in_db = (
        db.query(catalog_model.Catalog)
        .filter(catalog_model.Catalog.catalog_id == ticket.catalog_id)
        .first()
    )

    if not catalog_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Catalog not found"
        )

    user_in_db = (
        db.query(user_model.User)
        .filter(user_model.User.user_id == ticket.user_id)
        .first()
    )

    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    canal_in_db = (
        db.query(canal_model.Canal)
        .filter(canal_model.Canal.canal_id == ticket.canal_id)
        .first()
    )

    if not canal_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Canal not found"
        )

    if ticket.social_id:
        social_in_db = (
            db.query(social_model.Social)
            .filter(social_model.Social.social_id == ticket.social_id)
            .first()
        )

        if not social_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Social not found"
            )
        
    agencia_in_db = (
        db.query(agencia_model.Agencia)
        .filter(agencia_model.Agencia.agencia_id == ticket.agencia_id)
        .first()
    )

    if not agencia_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Agencia not found"
        )

    db_ticket = ticket_model.Ticket(
        status=ticket.status,
        amount=ticket.amount,
        client_id=ticket.client_id,
        catalog_id=ticket.catalog_id,
        user_id=ticket.user_id,
        canal_id=ticket.canal_id,
        social_id=ticket.social_id,
        agencia_id=ticket.agencia_id,
    )

    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)

    return db_ticket


# GET TICKET BY ID
def get_ticket_by_id(db: Session, ticket_id: int):
    ticket_in_db = (
        db.query(ticket_model.Ticket)
        .filter(ticket_model.Ticket.ticket_id == ticket_id)
        .first()
    )

    if not ticket_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found"
        )

    return ticket_in_db


# GET ALL TICKETS
def get_all_tickets(db: Session):
    ticket_in_db = (
        db.query(ticket_model.Ticket)
        .options(
            joinedload(ticket_model.Ticket.catalog),
            joinedload(ticket_model.Ticket.client),
            joinedload(ticket_model.Ticket.user),
            joinedload(ticket_model.Ticket.canal),
            joinedload(ticket_model.Ticket.social),
            joinedload(ticket_model.Ticket.comment),
        )
        .all()
    )

    if not ticket_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found"
        )

    for ticket in ticket_in_db:
        print(ticket.__dict__)

    return ticket_in_db


def get_tickets_by_user(db: Session, user_id: UUID):
    user_catalogs = (
        db.query(catalog_user_model.catalog_user.c.catalog_id)
        .filter(catalog_user_model.catalog_user.c.user_id == user_id)
        .all()
    )

    catalog_ids = []

    for catalog in user_catalogs:
        # print(type(catalog))
        for catalog_id in catalog:
            # print(type(catalog_id))
            catalog_ids.append(catalog_id)
    # print(catalog_ids)

    open_tickets = (
        db.query(ticket_model.Ticket)
        .options(
            joinedload(ticket_model.Ticket.catalog),
            joinedload(ticket_model.Ticket.client),
            joinedload(ticket_model.Ticket.user),
            joinedload(ticket_model.Ticket.canal),
            joinedload(ticket_model.Ticket.social),
            joinedload(ticket_model.Ticket.comment),
        )
        .filter(
            ticket_model.Ticket.status == "Abierto",
            ticket_model.Ticket.catalog_id.in_(catalog_ids),
        )
        .all()
    )
    print(type(open_tickets))
    # for ticket in open_tickets:
    #     print(ticket.__dict__)

    in_progress_tickets = (
        db.query(ticket_model.Ticket)
        .options(
            joinedload(ticket_model.Ticket.catalog),
            joinedload(ticket_model.Ticket.client),
            joinedload(ticket_model.Ticket.user),
            joinedload(ticket_model.Ticket.canal),
            joinedload(ticket_model.Ticket.social),
            joinedload(ticket_model.Ticket.comment),
        )
        .filter(
            ticket_model.Ticket.status == "En progreso",
            ticket_model.Ticket.user_id == user_id,
        )
        .all()
    )

    print(type(in_progress_tickets))

    closed_tickets = (
        db.query(ticket_model.Ticket)
        .options(
            joinedload(ticket_model.Ticket.catalog),
            # joinedload(type_model.Type),
            joinedload(ticket_model.Ticket.client),
            joinedload(ticket_model.Ticket.user),
            joinedload(ticket_model.Ticket.canal),
            joinedload(ticket_model.Ticket.social),
            joinedload(ticket_model.Ticket.comment),
        )
        .filter(
            ticket_model.Ticket.status == "Finalizado",
            ticket_model.Ticket.user_id == user_id,
        )
        .all()
    )

    tickets = {
        "openned_tickets": open_tickets,
        "in_progress_tickets": in_progress_tickets,
        "closed_tickets": closed_tickets,
    }
    print("*********", tickets)
    return tickets
    # tickets = open_tickets + in_progress_tickets + closed_tickets

    # return open_tickets, in_progress_tickets, closed_tickets

    # raise HTTPException(status_code=status.HTTP_200_OK, detail="Ticket found")


# Count tickets by user
def count_tickets(db: Session, user_id: UUID):
    tickets = get_tickets_by_user(db, user_id)

    # open_tickets = len(tickets["openned_tickets"])
    in_progress_tickets = len(tickets["in_progress_tickets"])
    closed_tickets = len(tickets["closed_tickets"])

    comments = (
        db.query(comment_model.Comment)
        .options(joinedload(comment_model.Comment.ticket))
        .filter(comment_model.Comment.user_id == user_id)
        .all()
    )

    comments_count = len(comments)

    tickets_count = {
        "in_progress_tickets": in_progress_tickets,
        "closed_tickets": closed_tickets,
        "comments_count": comments_count,
    }

    return tickets_count


# UPDATE TICKET
def update_ticket(db: Session, ticket: TicketUpdate):
    ticket_in_db = (
        db.query(ticket_model.Ticket)
        .filter(ticket_model.Ticket.ticket_id == ticket.ticket_id)
        .first()
    )

    if not ticket_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found"
        )

    ticket_in_db.status = ticket.status
    ticket_in_db.amount = ticket.amount
    ticket_in_db.client_id = ticket.client_id
    ticket_in_db.catalog_id = ticket.catalog_id
    ticket_in_db.catalog_id = ticket.user_id
    ticket_in_db.canal_id = ticket.canal_id
    ticket_in_db.social_id = ticket.social_id
    ticket_in_db.agencia_id = ticket.agencia_id

    db.commit()
    db.refresh(ticket_in_db)

    return ticket_in_db


# Ticket reports
def get_ticket_report(db: Session, report_model: ReportFilters):
    
    # if report_model.report_type == "historico":

    if report_model.report_filter == "fechas":
        if not report_model.date_o or not report_model.date_f:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Missing dates"
            )
        tickets = (
            db.query(ticket_model.Ticket)
            .filter(ticket_model.Ticket.created_at.between(report_model.date_o, report_model.date_f))
            .all()
        )

        if not tickets:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tickets not found"
            )
        return tickets
    
    elif report_model.report_filter == "ticket_number":
        if not report_model.ticket_o:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Missing ticket number"
            )
        ticket = (
            db.query(ticket_model.Ticket)
            .filter(ticket_model.Ticket.ticket_id == report_model.ticket_o)
            .first()
        )

        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found"
            )
        
        return ticket
    
    elif report_model.report_filter == "ticket_range":

        if not report_model.ticket_o or not report_model.ticket_f:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Missing ticket range"
            )

        tickets = (
            db.query(ticket_model.Ticket)
            .filter(ticket_model.Ticket.ticket_id.between(report_model.ticket_o, report_model.ticket_f))
            .all()
        )

        if not tickets:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tickets not found"
            )
        
        return tickets

    elif report_model.report_filter == "client_id":

        if not report_model.client_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Missing client id"
            )
        
        tickets = (
            db.query(ticket_model.Ticket)
            .filter(ticket_model.Ticket.client_id == report_model.client_id)
            .all()
        )

        if not tickets:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tickets not found"
            )
        
        return tickets
