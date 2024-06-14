from database.DB_connect import DBConnect
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllNodi():
        conn = DBConnect.get_connection()

        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select *
from go_products gp """
        cursor.execute(query)
        for row in cursor:
            result.append(Product(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllArchiPesati(n1, n2, year):
        conn = DBConnect.get_connection()

        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select count(distinct gds2.Retailer_code) as cont
from go_daily_sales gds, go_daily_sales gds2 
where gds2.Retailer_code = gds.Retailer_code and gds2.Product_number = %s and  gds.Product_number = %s and year(gds2.`Date`) = %s
and gds2.`Date` = gds.`Date`
"""
        cursor.execute(query, (n1.Product_number, n2.Product_number, year, ))
        for row in cursor:
            result.append(row["cont"])
        cursor.close()
        conn.close()
        return result[0]
