from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import calendar

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
base = declarative_base()


class Table(base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __str__(self):
        return self.task


base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
data = session.query(Table).all()
while True:
    print('''1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit''')
    user = int(input())

    if user == 1:  # Today's tasks
        today = datetime.today()
        rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
        print(f'Today {today.day} {today.strftime("%b")}:')
        if not rows:
            print('Nothing to do!')
        else:
            for i in range(len(rows)):
                print(f'{i + 1}. {rows[i].task}')
        print()

    elif user == 2:  # Week's tasks
        date_ = datetime.today()
        while True:
            rows = session.query(Table).filter(Table.deadline == date_.date()).all()
            print(f'{calendar.day_name[date_.weekday()]} {date_.day} {date_.strftime("%b")}:')
            if not rows:
                print('Nothing to do!')
            else:
                for i in range(len(rows)):
                    print(f'{i + 1}. {rows[i].task}')
            print()
            date_ += timedelta(days=1)
            if date_.date() == datetime.today().date() + timedelta(days=7):
                break

    elif user == 3:  # All tasks
        print('All tasks:')
        rows = session.query(Table).order_by(Table.deadline).all()
        for i in range(len(rows)):
            print(f'{i + 1}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime("%b")}')
        print()

    elif user == 4:  # Missed tasks
        rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
        print('Missed tasks:')
        if not rows:
            print('Nothing is missed!')
        else:
            for i in range(len(rows)):
                print(f'{i + 1}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime("%b")}')
        print()

    elif user == 5:  # Add task
        print('Enter task')
        new_data = Table(task=input(), deadline=datetime.strptime(input(), '%Y-%m-%d'))
        session.add(new_data)
        session.commit()
        print('The task has been added!')
        print()

    elif user == 6:  # Delete task
        print('Choose the number of the task you want to delete:')
        rows = session.query(Table).order_by(Table.deadline).all()
        if not rows:
            print('Nothing to delete')
        else:
            for i in range(len(rows)):
                print(f'{i + 1}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime("%b")}')
            row_no = int(input()) - 1  # (input() - 1) because user enters no. based on the for loop above with
            session.delete(rows[row_no])   # index i and no. (i + 1)
            session.commit()
            print('The task has been deleted!')
            print()

    else:  # Exit
        print('Bye!')
        break
