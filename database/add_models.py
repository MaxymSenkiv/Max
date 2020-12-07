from models import Session, Playlist, User

session1 = Session()

user1 = User(user_id = 1, name = "Vasya", email = "vasya@gmail.com", password = "vasyatop")
playlist1 = Playlist(playlist_id = 12, name = "morgenshtern", owner_id = 1, songs = ['du','ca','la','bo','gu'])

session1.add(user1)
session1.add(playlist1)

session1.commit()

session1.close()

# psql -h localhost -d musiclist -U postgres -p 5432 -a -q -f create_tables.sql
# python add_models.py 
# alembic revision --autogenerate
# alembic upgrade head