from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import  Column, Integer, String, Boolean
  
sqlite_database = "sqlite:///bot.db"
  
engine = create_engine(sqlite_database, echo=True)
Session = sessionmaker(autoflush=False, bind=engine)


class Base(DeclarativeBase): pass


class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True, index=True)
	initials = Column(String)
	city = Column(String)
	date_of_birth = Column(String)
	phone = Column(String)
	username = Column(String)
	amount_of_days = Column(String)
	amount_of_hours = Column(String)


	def add_new_user(initials, city, date_of_birth, phone, username, amount_of_days, amount_of_hours):
		with Session(autoflush=False, bind=engine) as db:
			new_user = User(initials=initials, city=city, date_of_birth=date_of_birth, phone=phone, username=username, amount_of_days=amount_of_days, amount_of_hours=amount_of_hours)

			db.add(new_user)
			db.commit()


Base.metadata.create_all(bind=engine)