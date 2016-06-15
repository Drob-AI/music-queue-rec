from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from src import FLASK


# Migrate(FLASK, DB)

MANAGER = Manager(FLASK)

if __name__ == '__main__':
    MANAGER.run()
