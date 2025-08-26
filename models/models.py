from __future__ import annotations

from typing import List, Optional
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Date,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import declarative_base, relationship, Mapped
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "User"

    user_ID = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    active_session = Column(Integer, nullable=False, default=0)

    # ilişkiler
    blocks: Mapped[List[IPBlocks]] = relationship("IPBlocks", back_populates="user", cascade="all, delete-orphan")
    edited_ips: Mapped[List[IPTable]] = relationship("IPTable", back_populates="editor")
    logs: Mapped[List[Logs]] = relationship("Logs", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User id={self.user_ID} username={self.username!r}>"


class Customer(Base):
    __tablename__ = "Customer"

    customer_ID = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String, nullable=False)
    customer_surname = Column(String, nullable=False)

    # ilişkiler
    ips: Mapped[List[IPTable]] = relationship("IPTable", back_populates="customer")

    def __repr__(self) -> str:
        return f"<Customer id={self.customer_ID} name={self.customer_name!r}>"


class IPBlocks(Base):
    __tablename__ = "IP_Blocks"

    block_ID = Column(Integer, primary_key=True, autoincrement=True)
    user_ID = Column(Integer, ForeignKey("User.user_ID"), nullable=False)
    block_name = Column(Text, nullable=False)
    range_start = Column(Text)
    range_end = Column(Text)
    CIDR = Column(Text)
    asno = Column(Text)
    timestamp = Column(DateTime, server_default=func.current_timestamp())
    status = Column(Text, nullable=False, server_default="active")

    __table_args__ = (
        CheckConstraint("status IN ('active','inactive')", name="ck_ip_blocks_status"),
    )

    # ilişkiler
    user: Mapped[User] = relationship("User", back_populates="blocks")
    ips: Mapped[List[IPTable]] = relationship("IPTable", back_populates="block", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<IPBlocks id={self.block_ID} cidr={self.CIDR!r} name={self.block_name!r} status={self.status}>"


class IPTable(Base):
    __tablename__ = "IP_Table"

    IP_ID = Column(Integer, primary_key=True, autoincrement=True)
    block_ID = Column(Integer, ForeignKey("IP_Blocks.block_ID", ondelete="CASCADE"))
    edited_by_user_ID = Column(Integer, ForeignKey("User.user_ID"))
    customer_ID = Column(Integer, ForeignKey("Customer.customer_ID"))
    IP_adress = Column(Text, nullable=False, unique=True)
    reservation = Column(Text)
    note = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)

    # ilişkiler
    block: Mapped[IPBlocks] = relationship("IPBlocks", back_populates="ips")
    editor: Mapped[Optional[User]] = relationship("User", back_populates="edited_ips")
    customer: Mapped[Optional[Customer]] = relationship("Customer", back_populates="ips")

    def __repr__(self) -> str:
        return f"<IPTable id={self.IP_ID} ip={self.IP_adress!r} block_id={self.block_ID}>"


class Logs(Base):
    __tablename__ = "Logs"

    log_ID = Column(Integer, primary_key=True, autoincrement=True)
    user_ID = Column(Integer, ForeignKey("User.user_ID"))
    action = Column(Text, nullable=False)
    timestamp = Column(DateTime, server_default=func.current_timestamp())

    # ilişkiler
    user: Mapped[Optional[User]] = relationship("User", back_populates="logs")

    def __repr__(self) -> str:
        return f"<Logs id={self.log_ID} action={self.action!r}>"


if __name__ == "__main__":
    from sqlalchemy import create_engine
    engine = create_engine("sqlite:///database/ip_data.db", future=True)
    Base.metadata.create_all(engine)
    print("ORM tabloları kontrol edildi / oluşturuldu (varsa).")