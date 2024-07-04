from sqlalchemy import MetaData, Table, Column, Integer, String, BigInteger

metadata = MetaData()

bots_accounts = Table("bots_accounts", metadata,
    Column("id", Integer, primary_key=True),
    Column("login", String, nullable=False),
    Column("password", String, nullable=False),
)

user_accounts = Table("user_accounts", metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", BigInteger, nullable=False),
)
