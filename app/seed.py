from app.database import SessionLocal, engine, Base
from app.models import MenuItem
from app.menu_data import flatten_menu_items


def seed_menu(replace: bool = True):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        existing = db.query(MenuItem).count()
        if existing and not replace:
            print("المنيو مضاف مسبقاً!")
            return

        if existing:
            db.query(MenuItem).delete()
            db.commit()

        for item_data in flatten_menu_items():
            db.add(MenuItem(**item_data))

        db.commit()
        print(f"Rostica full menu seeded ({len(flatten_menu_items())} items).")
    finally:
        db.close()


if __name__ == "__main__":
    seed_menu()
