import datetime
from decimal import Decimal
import enum
from typing import Annotated

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.utcnow
)]


class Role(enum.Enum):
    admin = "admin"
    user = "user"


class Proposal(Base):
    __tablename__ = "proposal"
    
    id: Mapped[intpk]
    title: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    
    users_voted: Mapped[list["User"]] = relationship(
        back_populates="proposals_selected",
        secondary="vote"
    )


class User(Base):
    __tablename__ = "user"
    
    id: Mapped[intpk]
    username: Mapped[str]
    password: Mapped[str]
    wallet_address: Mapped[str] = mapped_column(unique=True)
    role: Mapped[Role]
    is_active: Mapped[bool] = mapped_column(default=True)
    block_number: Mapped[int]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    
    proposals_selected: Mapped[list["Proposal"]] = relationship(
        back_populates="users_voted",
        secondary="vote"
    )


class ResponseOptions(enum.Enum):
    in_favor = "In favor"
    against = "Against"


class Vote(Base):
    __tablename__ = "vote"
    
    proposal_id: Mapped[int] = mapped_column(
        ForeignKey("proposal.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    )
    choice: Mapped[ResponseOptions]
    created_at: Mapped[created_at]
    user_balance: Mapped[Decimal]
    block_number: Mapped[int]
