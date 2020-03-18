import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
env_pw = os.getenv('DB_PW')


def db_connector(func):
    def wrapper_connection_(*args, **kwargs):
        try:
            connection = psycopg2.connect(user='testbot',
                                          password=env_pw,
                                          host='localhost',
                                          port='5432',
                                          database='test')

            cursor = connection.cursor()
            # Print propertiies of connection
            print(connection.get_dsn_parameters(), '\n')
    
            # Query Function to be called
            query_function = func(cursor, *args, **kwargs)
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print('Error connecting to PSQL: ', error)
            connection.rollback()
        finally:
            # close db connection
            if (connection):
                cursor.close()
                connection.close()
                print('PSQL connection closed')
        return query_function
    return wrapper_connection_

@db_connector
def test(cursor):
    print('Start of test')
    cursor.execute('SELECT version();')
    record = cursor.fetchone()
    print('You are connected to: ', record, '\n')


@db_connector
def insert_user(cursor, user):
    """Takes a discord user object and inserts it to db table discord_users"""
    postgres_insert_query = """ INSERT INTO discord_users (userID, userName, userNumber) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING"""
    record_to_insert = (user.id, user.name, int(user.discriminator))
    cursor.execute(postgres_insert_query, record_to_insert)

@db_connector
def update_user(cursor, user):
    """ Updates name or discriminator of existing user by id"""
    postgres_update_query = """ UPDATE discord_users set userName=%s, userNumber=%s where userID=%s ON CONFLICT DO NOTHING"""
    record_to_insert = (user.name, int(user.discriminator), user.id)
    cursor.execute(postgres_update_query, record_to_insert)

@db_connector
def select_all_members(cursor):
    """Returns all members of db table discord_users"""
    cursor.execute('SELECT * FROM discord_users ;')
    return cursor.fetchall()

@db_connector
def find_member_id(cursor, user_id):
    """finds and returns member as tuplet. None if not found"""
    postgres_select_query = """ SELECT * FROM discord_users WHERE userID =(%s)"""
    user_id_to_select = (user_id,)
    cursor.execute(postgres_select_query, user_id_to_select)
    return cursor.fetchall()
