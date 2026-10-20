from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# رابط قاعدة بيانات SQLite محلية بسيطة
SQLALCHEMY_DATABASE_URL = "sqlite:///./restaurant.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def auto_migrate():
    """التحقق من وجود الأعمدة الجديدة في قاعدة البيانات وإضافتها تلقائياً دون فقد البيانات."""
    try:
        with engine.connect() as conn:
            # التحقق من جدول orders
            result = conn.execute(text("PRAGMA table_info(orders)"))
            cols = [row[1] for row in result.fetchall()]
            if cols:
                if "customer_name" not in cols:
                    conn.execute(text("ALTER TABLE orders ADD COLUMN customer_name VARCHAR"))
                if "order_type" not in cols:
                    conn.execute(text("ALTER TABLE orders ADD COLUMN order_type VARCHAR DEFAULT 'دليفري'"))
                if "delivery_address" not in cols:
                    conn.execute(text("ALTER TABLE orders ADD COLUMN delivery_address TEXT"))
                if "notes" not in cols:
                    conn.execute(text("ALTER TABLE orders ADD COLUMN notes TEXT"))
                if "created_at" not in cols:
                    conn.execute(text("ALTER TABLE orders ADD COLUMN created_at DATETIME"))
                if "updated_at" not in cols:
                    conn.execute(text("ALTER TABLE orders ADD COLUMN updated_at DATETIME"))
                conn.commit()
    except Exception as e:
        print(f"[Auto Migrate Note]: {e}", flush=True)
