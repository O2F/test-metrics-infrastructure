import logging
import sys

import mysql.connector

from cfg.configuration_loader import ConfigurationLoader


class StatsIngestion:

    def __init__(self):
        self.cl = ConfigurationLoader()
        mysql_section = self.cl.get_toml_config().get("mysql")

        self.table_name = mysql_section.get("datasource").get("db_table")
        self.db_name = mysql_section.get("datasource").get("db_name")

        try:
            self.conn = mysql.connector.connect(
                host=mysql_section.get("host"),
                user=mysql_section.get("username"),
                password=mysql_section.get("password"),
                port=mysql_section.get("port"),
                use_pure=True,
                database=self.db_name
            )
        except mysql.connector.errors.ProgrammingError:
            logging.critical("Couldn't connect to the stated database, aborting...")
            sys.exit(1)

    def get_cursor(self):
        return self.conn.cursor()

    def __stats_tbl_exists(self):
        with self.get_cursor() as cursor:

            cursor.execute("""
            SELECT COUNT(*)
            FROM
                information_schema.tables
            WHERE
                table_schema = %(db_name)s
            AND
                table_name = %(table_name)s
            """, {
                'db_name': self.db_name,
                "table_name": self.table_name
            })

            if cursor.fetchone()[0] > 0:
                return True

    def insert_stats_from_dict(self, dict_of_stats):

        sql = f"""
                INSERT INTO
                    {self.db_name}.{self.table_name}(
                        `suites_nr`,
                        `tests_nr`,
                        `passes`,
                        `pending`,
                        `failures`,
                        `skipped`,
                        `duration_ms`,
                        `pass_percent`
                        )
                VALUES
                    (
                    {dict_of_stats['suites']},
                    {dict_of_stats['tests']},
                    {dict_of_stats['passes']},
                    {dict_of_stats['pending']},
                    {dict_of_stats['failures']},
                    {dict_of_stats['skipped']},
                    {dict_of_stats['duration']},
                    {round(dict_of_stats['passPercent'],2)}
                    );
                """

        if self.__stats_tbl_exists():
            with self.get_cursor() as cursor:
                cursor.execute(sql)
                cursor.execute("commit;")
        else:
            raise NotImplementedError("Expected Stats table is not yet created")
