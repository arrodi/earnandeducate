class Queries:

    def __init__(self):
        self.table_schemas = {
            "USER_ACCOUNTS": {
                "USER_EMAIL": "text PRIMARY KEY",
                "USER_NAME": "text",
                "USER_PASS": "text",
                "USER_RATING": "decimal",
                "USER_SCHOOL": "text",
                "USER_TUTOR": "boolean",
                "USER_BACKGROUND_CHECK": "boolean",
                "CRT_DT": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                "UPD_DT": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
            },
            "USER_HOBBIES" : {
                "HOBBY_ID": "text PRIMARY KEY",
                "USER_EMAIL": "text REFERENCES USER_ACCOUNTS (USER_EMAIL)",
                "HOBBY_NAME": "text",
                "HOBBY_DESCRIPTION": "text",
                "HOBBY_PROFICIENCY": "text",
                "HOBBY_TUTORING": "boolean",
                "EXPERIENCE_YEARS": "integer",
                "EXPERIENCE_MONTHS": "integer",
                "CRT_DT": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                "UPD_DT": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            },
            "USER_HOBBIES_TUTORING" : {
                "HOBBY_ID": "text REFERENCES USER_HOBBIES (HOBBY_ID)",
                "TUTORING_HOURLY_RATE": "integer",
                "TUTORING_MODE_LIVE_CALL": "boolean",
                "TUTORING_MODE_PUBLIC_IN_PERSON": "boolean",
                "TUTORING_MODE_PRIVATE_IN_PERSON": "boolean",
                "TUTORING_DESCRIPTION": "text",
                "CRT_DT": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                "UPD_DT": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            },
            "TUTORING_SESSION" : {
                "SESSION_ID": "text PRIMARY KEY",
                "USER_TUTOR_ID": "text REFERENCES USER_ACCOUNTS (USER_EMAIL)",
                "USER_STUDENT_ID": "text REFERENCES USER_ACCOUNTS (USER_EMAIL)",
                "SESSION_HOBBY": "text",
                "SESSION_MODE": "text",
                "SESSION_SCHEDULED_START_TIME": "TIMESTAMP",
                "SESSION_SCHEDULED_END_TIME": "TIMESTAMP",
                "SESSION_ACTUAL_START_TIME": "TIMESTAMP",
                "SESSION_ACTUAL_END_TIME": "TIMESTAMP",
            },
            "TUTORING_SESSION_REVIEWS" : {
                "REVIEW_ID": "text PRIMARY KEY",
                "USER_EMAIL": "text REFERENCES USER_ACCOUNTS (USER_EMAIL)",
                "SESSION_ID": "text REFERENCES TUTORING_SESSION (SESSION_ID)",
                "SESSION_REVIEW_TEXT": "text",
                "SESSION_RATING": "integer"
            }
        }

    def create_table(self, table_nm, table_columns):
        
        data_lst = []
        for _column_nm, _column_config in table_columns.items():
             data_lst.append(f"{_column_nm} {_column_config}")

        data_str = ", ".join(data_lst)

        sql = f"""
                CREATE TABLE IF NOT EXISTS {table_nm}
                    ({data_str})
                """
        
        return sql
    
    def modify_record(self, table_nm, record_data, record_condition):

        record_data_lst = []
        for _key, _value in record_data.items():
            record_data_lst.append(f"{_key} = '{_value}'")

        record_data_str = ", ".join(record_data_lst)

        sql_context = f"""
                UPDATE {table_nm}
                SET {record_data_str}
                WHERE {record_condition};
                """
        
        return sql_context
    
    def insert_into_table(self, table_nm, table_data):
        
        column_lst = []
        value_lst = []
        for _column_nm, _column_value in table_data.items():
             column_lst.append(_column_nm)
             value_lst.append(f"'{_column_value}'")

        column_str = ", ".join(column_lst)
        value_str = ", ".join(value_lst)

        sql_context =f"""
        INSERT INTO
            {table_nm} ({column_str})
            VALUES ({value_str});
        """
        
        return sql_context
    
    def select_table(self, table_nm, table_columns_lst, where_clause):
        table_columns_str = ", ".join(table_columns_lst)
        sql_context =f"""
            SELECT 
                {table_columns_str}
            FROM 
                {table_nm}
            WHERE
                {where_clause}
            """
        
        return sql_context
    
    def select_join_table(self, table_nm_1, table_nm_2, table_columns_lst, join_column, where_clause = ""):
        table_columns_str = ", ".join(table_columns_lst)

        join_clause = f"a.{join_column} = b.{join_column}"

        if where_clause:
            sql_context =f"""
            SELECT 
                {table_columns_str}
            FROM 
                {table_nm_1} a
            INNER JOIN
                {table_nm_2} b
            ON
                {join_clause}
            WHERE
                {where_clause}
            """
        else:
            sql_context =f"""
            SELECT 
                {table_columns_str}
            FROM 
                {table_nm_1} a
            INNER JOIN
                {table_nm_2} b
            ON
                {join_clause}
            """
        
        return sql_context
        
    def upd_dt_function(self, function_nm):
    
        sql = f"""
                CREATE OR REPLACE FUNCTION {function_nm}()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.UPD_DT = CURRENT_TIMESTAMP;
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
                """
        return sql
    
    def tutoring_mode_function(self, function_nm):

        sql = f"""
                CREATE OR REPLACE FUNCTION {function_nm}()
                RETURNS TRIGGER AS $$
                BEGIN
                    IF NEW.TUTORING_MODE_LIVE_CALL IS NULL THEN
                        NEW.TUTORING_MODE_LIVE_CALL := false;
                    END IF;
                    IF NEW.TUTORING_MODE_PUBLIC_IN_PERSON IS NULL THEN
                        NEW.TUTORING_MODE_PUBLIC_IN_PERSON := false;
                    END IF;
                    IF NEW.TUTORING_MODE_PRIVATE_IN_PERSON IS NULL THEN
                        NEW.TUTORING_MODE_PRIVATE_IN_PERSON := false;
                    END IF;
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
                """
        return sql
    
    def upd_dt_function_trigger(self, table_nm, function_nm):
        sql = f"""
        CREATE TRIGGER {table_nm}_TRIGGER_{function_nm}
        BEFORE UPDATE ON {table_nm}
        FOR EACH ROW
        EXECUTE FUNCTION {function_nm}();
        """

        return sql
    
    def tutoring_mode_function_trigger(self, table_nm, function_nm):
        sql = f"""
        CREATE TRIGGER {table_nm}_TRIGGER_{function_nm}
        BEFORE INSERT ON {table_nm}
        FOR EACH ROW EXECUTE FUNCTION {function_nm}();
        """

        return sql
    
    def drop_tables(self):
        sql = """
        DO $$ 
        DECLARE
            r RECORD;
        BEGIN
            FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public')
            LOOP
                EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
            END LOOP;
        END $$;
        """

        return sql