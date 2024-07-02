from database.DB_connect import DBConnect
from model.gene import Gene


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getGeni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * 
                from genes_small.genes g 
                where g.Essential = 'Essential' """

        cursor.execute(query, )

        for row in cursor:
            result.append(Gene(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select g.GeneID as g1, g2.GeneID as g2, i.Expression_Corr as peso
                from genes_small.genes g, genes_small.genes g2, genes_small.interactions i 
                where ((g2.GeneID = i.GeneID2 and g.GeneID = i.GeneID1) or (g.GeneID = i.GeneID2 and g2.GeneID = i.GeneID1)) 
                and g2.Essential = 'Essential' and g.Essential = 'Essential' and g.GeneID < g2.GeneID 
                group by g.GeneID, g2.GeneID"""

        cursor.execute(query, )

        for row in cursor:
            result.append((row["g1"], row["g2"], row["peso"]))

        cursor.close()
        conn.close()
        return result