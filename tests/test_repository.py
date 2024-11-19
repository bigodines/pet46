import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from storage.database import Base
from storage.models import Habit, Checkin
from storage.repository import HabitRepository

@pytest.fixture
def test_session():
    """Creates a new database session for testing."""
    engine = create_engine('sqlite:///:memory:')  
    Base.metadata.create_all(engine) 
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session  # Provide the session to tests
    session.close()
    engine.dispose()

@pytest.fixture
def habit_repo(test_session):
    return HabitRepository(test_session)

def test_add_habit(habit_repo):
    """Test adding a new habit."""
    habit = habit_repo.add_habit("Exercise")
    assert habit.id is not None
    assert habit.name == "Exercise"
    assert habit.checkin_count == 0

def test_add_checkin(habit_repo, test_session):
    """Test adding a checkin to a habit."""
    # Add a habit first
    habit = habit_repo.add_habit("Read")
    assert habit.checkin_count == 0

    # Add a checkin
    updated_habit = habit_repo.add_checkin(habit.id)
    assert updated_habit.checkin_count == 1

    # Verify checkin is recorded in Checkin table
    checkin = test_session.query(Checkin).filter_by(habit_id=habit.id).first()
    assert checkin is not None
    assert checkin.habit_id == habit.id

def test_get_habit(habit_repo):
    """Test retrieving a habit."""
    # Add a habit
    habit = habit_repo.add_habit("Meditate")

    # Retrieve the habit
    retrieved_habit = habit_repo.get_habit(habit.id)
    assert retrieved_habit is not None
    assert retrieved_habit.name == "Meditate"
    assert retrieved_habit.checkin_count == 0

def test_add_checkin_invalid_habit(habit_repo):
    """Test adding a checkin to a non-existent habit."""
    with pytest.raises(ValueError, match="Habit with id 999 does not exist"):
        habit_repo.add_checkin(999)
