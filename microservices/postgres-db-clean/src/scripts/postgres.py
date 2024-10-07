import psycopg2
import psycopg2.errorcodes
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Postgres:
    def __init__(self, database, user, password, host, port):
        self.connection = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)

    def execute_query(self, query_str, fetch=False):
        try:
            with self.connection.cursor() as cursor:
                logger.info('EXECUTING:' + query_str)
                
                cursor.execute(query_str)
                
                # Log PostgreSQL notices if any
                if self.connection.notices:
                    logger.info(self.connection.notices[-1])
                    self.connection.notices = []

                self.connection.commit()
                
                if fetch:
                    return cursor.fetchall()
                else:
                    return "QUERY SUCCESS"
        except psycopg2.errors.lookup(psycopg2.errorcodes.UNIQUE_VIOLATION) as e:
            self.connection.rollback()
            logger.error("INSERT ERROR: Unique constraint violated")
            return "INSERT ERROR: " + str(e)
        except Exception as e:
            self.connection.rollback()
            logger.error(f"QUERY ERROR: {e}")
            return f"QUERY ERROR: " + str(e)