from pathlib import Path

from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

engine = create_engine("sqlite:///db.sqlite", echo=True)


class Base(DeclarativeBase): ...


class Labels(Base):
    __tablename__ = "labels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sar: Mapped[str] = mapped_column(String)
    home: Mapped[str] = mapped_column(String)
    work: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f"<Labels(sar={self.sar}, home={self.home}, work={self.work})>"


def initialize_db() -> None:
    fixture_file = Path(__file__).parent / "fixtures" / "labels.csv"
    fixtures = [line.split(",") for line in fixture_file.read_text().splitlines()]

    Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all(
            [Labels(sar=sar, home=home, work=work) for (sar, work, home) in fixtures]
        )
        session.commit()

        print(session.query(Labels).count())


if __name__ == "__main__":
    initialize_db()
