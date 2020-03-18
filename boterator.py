import db_handler
class BotOperator:
    """Bot operator
     important fucntions that read, insert to database as well as
     process data from both discord and database.

     """


    def __init__(self):
        pass


    def sync_members(self, members):
        """Ensures database data is synced and  up to date with discord members"""

        print('Starting sync_members')
        # Make set of tuples from db with members
        db_members = set(db_handler.select_all_members())

        # Make set of tuples from dicitionary
        disc_members = set([(k, v.name, v.discriminator) for k, v in members.items()])

        # If both are equal then jobs done!
        if disc_members == db_members:
            return

        # Make two sets New users to be inserted, old users to be updated

        # Remove all that are equal
        disc_members.difference_update(db_members)

        # Iterate over both sets and insert new users
        for disc_user in disc_members:
            user_id = disc_user[0]
            new_user = True
            for db_user in db_members:
                if db_user[0] == user_id:
                    new_user=False
                    break
            if new_user:
                db_handler.insert_user(disc_user)


        # Get new updated set from db and remove equals.
        # Make set of tuples from db with members
        db_members = set(db_handler.select_all_members())

        # Make set of tuples from dicitionary
        disc_members = set([(k, v.name, v.discriminator) for k, v in members.items()])
        disc_members.difference(db_members)

        # Remaining in sets are users who exist in db but need to be updated name or discriminator.
        for user in disc_members:
            db_handler.update_user(user)

        #Return true if db sync was performed or not needed, false if db could not be reached or changed
        return

    def insert_user(self, user):
        """Prefors a insert query and tries to write single user to database by id"""
        db_handler.insert_user(user)

    def insert_users(self, users):
        """Similar to insert user, but inserts multiple users."""
        db_handler.insert_users(users)



    def update_user(self, user):
        """Changes name and / or discirinator of existing user. does not change ID"""
        db_handler.update_user(user)

    def retrieve_db_members(self):
        """Preforms a query and retrieves members as a list"""

        return db_handler.members()
