from tortoise import Tortoise
from passlib.context import CryptContext
from user.model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
MAX_BCRYPT_LEN = 72

async def create_default_admin():
    await Tortoise.init(
        db_url="postgres://admin:samuel@localhost:5432/sklep",
        modules={"models": ["user.model"]}
    )

    admin = await User.filter(login="admin").first()
    if not admin:
        hashed_password = pwd_context.hash("samuel"[:MAX_BCRYPT_LEN])
        await User.create(login="admin", password=hashed_password, role="admin")
        print("Utworzono domyślnego administratora")

    await Tortoise.close_connections()
