from datetime import datetime

import mysql.connector


class MySQL:

    def __init__(self, connector):
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\t[MYSQL]\tConnection established")
        self.db = mysql.connector.connect(**connector)
        self.cursor = self.db.cursor()

    def select(self, query) -> []:
        """

        :param query:
        :return:
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert(self, query) -> int:
        """

        :param query:
        :return:
        """
        self.cursor.execute(query)
        self.db.commit()
        return self.cursor.lastrowid

    def update(self, query) -> bool:
        """

        :param query:
        :return:
        """
        self.cursor.execute(query)
        self.db.commit()
        return True
