# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field


def add_task():
    print("Enter task")
    new_task = input()
    print("Enter deadline")
    new_deadline = input()
    new_row = Table(task=new_task, deadline=datetime.strptime(new_deadline, '%Y-%m-%d'))
    session.add(new_row)
    session.commit()


def print_tasks_daily(day, today=False):
    rows = session.query(Table).filter(Table.deadline == day.date()).all()
    print("{} {} {}:".format("Today" if today else day.strftime('%A'), day.day, day.strftime('%b')))
    if len(rows) > 0:
        for row in range(len(rows)):
            print("{}. {}".format(row + 1, rows[row].task))
    else:
        print("Nothing to do!")


def print_all_tasks(missed=False, delete=False):
    if missed:
        rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
    else:
        rows = session.query(Table).order_by(Table.deadline).all()
    if len(rows) > 0:
        for row in rows:
            print("{}. {}. {} {}".format(row.id, row.task, row.deadline.day, row.deadline.strftime('%b')))
    else:
        if missed:
            print("Nothing is missed!")
        elif delete:
            print("Nothing to delete")
        else:
            print("Nothing to do!")


def delete_task(deleted_task):
    rows = session.query(Table).order_by(Table.deadline).all()
    if deleted_task < len(rows):
        session.delete(rows[deleted_task])
        session.commit()
        print("The task has been deleted!\n")
    else:
        print("Task with such id is not present!")


def main_menu():
    choice = "-1"
    while choice != "0":
        print("1) Today's tasks", "2) Week's tasks", "3) All tasks", "4) Missed tasks",
              "5) Add task", "6) Delete task", "0) Exit", sep="\n")
        choice = input()
        print("got choice {}".format(choice))
        if choice == "1":
            print_tasks_daily(datetime.today(), today=True)
            print()
        elif choice == "2":
            for days in range(0, 7):
                print_tasks_daily(datetime.today() + timedelta(days=days))
                print()
        elif choice == "3":
            print("All tasks:")
            print_all_tasks()
            print()
        elif choice == "4":
            print("Missed tasks:")
            print_all_tasks(missed=True)
            print()
        elif choice == "5":
            add_task()
        elif choice == "6":
            print("Choose the number of the task you want to delete:")
            print_all_tasks(delete=True)
            delete_task(deleted_task=int(input()))


if __name__ == '__main__':
    engine = create_engine('sqlite:///todo.db?check_same_thread=False')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    main_menu()
