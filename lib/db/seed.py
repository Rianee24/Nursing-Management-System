from faker import Faker
from . import get_session, engine, Base
from .models import Manager, Nurse, Elderly

def seed(n_managers=3, nurses_per_manager=2, elderly_per_nurse=3):
    fake = Faker()
    session = get_session()
    Base.metadata.create_all(bind=engine)

    managers = []
    for _ in range(n_managers):
        m = Manager.create(session, name=fake.name(), email=fake.email(), phone_number=fake.phone_number(), department=fake.job())
        managers.append(m)

    for manager in managers:
        for _ in range(nurses_per_manager):
            n = Nurse.create(session, name=fake.name(), specialization=fake.word(), shift=fake.random_element(elements=('day','night','swing')), manager_id=manager.id)
            for _ in range(elderly_per_nurse):
                Elderly.create(session, name=fake.name(), age=fake.random_int(min=65, max=95), health_condition=fake.sentence(nb_words=3), nurse_id=n.id)

    session.close()
    print("Seeding complete.")
