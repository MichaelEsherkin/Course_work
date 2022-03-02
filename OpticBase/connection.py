import datetime
import pyodbc


class DataBase():
    def __init__(self):
        pass

    def connect(self, server, database, username, password):
        """Used to create connection"""
        self.server = server
        self.database = database
        self.cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+username+';PWD='+ password)
        self.cursor = self.cnxn.cursor()

    def insert(self, table, fields, field_values):
        """
        Inserts field_values to fields in table
        Args:
            table: table to insert
            fields: name of fields
            field_values: field values

        Returns:
            inserted id
        """
        self.cursor.execute("INSERT INTO [" + table + "] (" +
                            ",".join(fields) + ") VALUES (" +
                            ",".join(map(lambda x: "?", fields)) +  ")",
                            *field_values)
        self.cnxn.commit()
        self.cursor.execute("SELECT @@IDENTITY")
        return self.cursor.fetchone()[0]

    def insertDetail(self, order_id, detail):
        """Inserts order detail with order_id to Details_order and returns order_id of inserted"""
        inserted = self.insert("Details_order",
                    ["id_service_price", "id_service", "id_product_price",
                     "id_product", "count_details", "id_order"],
                    detail + [order_id])
        return inserted

    def insertOrder(self, id_client, id_seller, date, details):
        """
        Inserts full order with details
        Args:
            id_client:
            id_seller:
            date:
            details: list of lists [[details_order_fields]]

        Returns:
            tuple(order_id, [id_details])
        """
        order_id = self.insert("Order", ["id_client", "id_seller", "date_order"], [id_client, id_seller, date])
        detail_order_ids = []
        for detail in details:
            detail_order_ids.append(self.insert("Details_order",
                        ["id_service_price", "id_service", "id_product_price",
                         "id_product", "count_details", "id_order"],
                        detail + [order_id]))
        print("Inserted order with id: " + str(order_id))
        print("Details_ids: " + ";".join(map(str, detail_order_ids)))
        return (order_id, detail_order_ids)

    def add(self, fields, entity):
        """
        Inserts entity with fields to database
        Args:
            fields: fields of entity in declared order
            entity:

        Returns:
            id of inserted entity
        """
        fields = list(map(lambda x: x.text(), fields))

        row_id = None

        if (entity == "manufacturer"):
            # checking if there is country
            self.cursor.execute("SELECT id_manufacturer_country FROM Manufacturer_country WHERE country_manufacturer = ?",
                                fields[1])
            row = self.cursor.fetchone()

            row_id = None
            if (row is None):
                row_id = self.insert("Manufacturer_country", ["country_manufacturer"], [fields[1]])
                print("Inserted country with id: " + str(row_id))
            else:
                row_id = row[0]

            # inserting manufacturer
            manu_id = self.insert("Manufacturer_name",
                                  ["name_manufacturer", "id_manufacturer_country"],
                                  [fields[0], row_id])
            print("Inserted manufacturer with id: " + str(manu_id))
            row_id = manu_id

        if (entity == "product"):
            materials = fields[0]
            material_ids = []
            for material_orig in materials.split(","):
                material = material_orig.strip()
                self.cursor.execute(
                    "SELECT id_material FROM Material WHERE name_material = ?",
                    material)
                row = self.cursor.fetchone()

                row_id = None
                if (row is None):
                    row_id = self.insert("Material", ["name_material"], [material])
                    print("Inserted material with id: " + str(row_id))
                else:
                    row_id = row[0]

                material_ids.append(row_id)

            self.cursor.execute(
                "SELECT id_manufacturer FROM Manufacturer_name WHERE name_manufacturer = ?",
                fields[1])
            row = self.cursor.fetchone()

            manu_id = None
            if (row is None):
                print("No such manufacturer: " + str(fields[1]))
                return -1
            else:
                manu_id = row[0]

            # inserting product
            product_id = self.insert("Product",
                                  ["id_manufacturer", "name_product", "product_availability"],
                                  [manu_id, fields[2], fields[3]])

            # self.insert("Product_price")

            for row_id in material_ids:
                prod_mat_id = self.insert("Product_material", ["id_material", "id_product"], [row_id, product_id])
                print("Product_material inserted with id: " + str(prod_mat_id))

            product_price_id = self.insert("Product_price", ["id_product", "cost_product", "price_list_date"],
                                           [product_id, fields[4], datetime.datetime.now()])

            print("Product inserted with id: " + str(product_id))
            row_id = product_id

        if (entity == "client"):
            row_id = self.insert("Client",
                                 ["surname_client", "name_client", "patronymic_client", "phone_number_client"], fields)
            print("Client inserted with id: " + str(row_id))

        if (entity == "seller"):
            row_id = self.insert("Seller",
                                 ["surname_seller", "name_seller", "patronymic_seller", "phone_number_seller",
                                  "position_seller"],
                                 fields)
            print("Seller inserted with id: " + str(row_id))

        if (entity == "service"):
            row_id = self.insert("Service",
                                 ["name_service"],
                                 [fields[0]])
            row_id_p = self.insert("Service_price", ["id_service", "cost_service", "price_list_date"],
                                   [row_id, fields[1], datetime.datetime.now()])
            print("Service inserted with id: " + str(row_id))

        return row_id

    def searchExistingOrder(self, order_id, surname):
        """
        Search existing order in db by order_id or surname
        Args:
            order_id:
            surname:

        Returns:
            [order (id_order, surname, name, phone_number, date)]
        """
        if (order_id != ""):
            selected = self.cursor.execute(
                """SELECT [id_order], surname_client, name_client, phone_number_client, date_order
                   FROM [Order] o JOIN Client c ON o.id_client = c.id_client
                   WHERE o.id_order = ?
                """, order_id)
            res = selected.fetchall()
            print(res)

        else:
            selected = self.cursor.execute(
                """SELECT [id_order], surname_client, name_client, phone_number_client, date_order
                   FROM [Order] o JOIN Client c ON o.id_client = c.id_client
                   WHERE c.surname_client = ?
                """, surname)
            res = selected.fetchall()

        return res

    def searchExistingOrderDetailed(self, order_id):
        """
        Returns order details of order_id order
        Args:
            order_id:

        Returns:
            list of order_details
        """
        selected = self.cursor.execute(
            """SELECT id_details, 'Услуга' as f1, name_service, cost_service, count_details 
               FROM Details_order do
               JOIN [Service] s ON do.id_service = s.id_service
               JOIN [Service_price] sp ON do.id_service_price = sp.id_service_price 
               WHERE id_order = ?
               UNION ALL
               SELECT id_details, 'Товар' as f1, name_product, cost_product, count_details 
               FROM Details_order do
               JOIN [Product] p ON do.id_product = p.id_product
               JOIN [Product_price] pp ON do.id_product_price = pp.id_product_price 
               WHERE id_order = ?
            """, order_id, order_id)

        res = selected.fetchall()
        print(res)

        return res

    def selectForList(self, entity):
        """
        Selects and returns info about all entities
        Args:
            entity:

        Returns:
            (list(string), list)
        """
        if (entity == "product"):
            selected = self.cursor.execute(
                """SELECT p.id_product, p.name_product, pp.cost_product, mn.name_manufacturer, 
                          p.product_availability, pp.id_product_price 
                   FROM Product p 
                   JOIN Product_price pp ON p.id_product = pp.id_product
                   JOIN (SELECT MAX(price_list_date) as price_list_date, id_product
                         FROM Product_price GROUP BY id_product) ppl 
                        ON pp.id_product = ppl.id_product AND pp.price_list_date = ppl.price_list_date
                   JOIN Manufacturer_name mn ON p.id_manufacturer = mn.id_manufacturer
                """)
            res = selected.fetchall()
            return ((list(map(lambda x: str(x[1]) + ", " + str(x[3]), res))),
                    (list(map(lambda x: (x[5], x[0], x[2]), res))))

        if (entity == "service"):
            selected = self.cursor.execute(
                """SELECT s.id_service, s.name_service, sp.cost_service, sp.id_service_price
                   FROM Service s 
                   JOIN Service_price sp ON s.id_service = sp.id_service
                   JOIN (SELECT MAX(price_list_date) as price_list_date, id_service
                         FROM Service_price GROUP BY id_service) spl 
                        ON sp.id_service = spl.id_service AND sp.price_list_date = spl.price_list_date
                """)
            res = selected.fetchall()
            return ((list(map(lambda x: str(x[1]), res))),
                    (list(map(lambda x: (x[3], x[0], x[2]), res))))

        if (entity == "client"):
            selected = self.cursor.execute(
                """SELECT c.id_client, c.surname_client, c.name_client, c.patronymic_client
                   FROM Client c
                """)
            res = selected.fetchall()
            return ((list(map(lambda x: "{} {} {}".format(x[1], x[2], x[3]), res))),
                    (list(map(lambda x: (x[0]), res))))

        if (entity == "seller"):
            selected = self.cursor.execute(
                """SELECT s.id_seller, s.position_seller, s.surname_seller, s.name_seller
                   FROM Seller s
                """)
            res = selected.fetchall()
            return ((list(map(lambda x: "{} {} {}".format(x[1], x[2], x[3]), res))),
                    (list(map(lambda x: (x[0]), res))))

    def select(self, fields, entity):
        """
        Search and returns entity where some fields = fields
        Args:
            fields: list of str
            entity:

        Returns:
            list, list(list)
            headers, entities
        """
        fields = list(map(lambda x: x.text(), fields))

        row_id = None

        if (entity == "manufacturer"):
            # checking if there is country
            selected = self.cursor.execute(
                """SELECT mn.id_manufacturer, mn.name_manufacturer, mc.country_manufacturer 
                   FROM Manufacturer_name mn JOIN Manufacturer_country mc ON mn.id_manufacturer_country = mc.id_manufacturer_country 
                   WHERE name_manufacturer LIKE ?""",
                fields)

        if (entity == "product"):
            selected = self.cursor.execute(
                """SELECT p.id_product, p.name_product, pp.cost_product, mn.name_manufacturer, p.product_availability FROM Product p 
                   JOIN Product_price pp ON p.id_product = pp.id_product
                   JOIN (SELECT MAX(price_list_date) as price_list_date, id_product
                         FROM Product_price GROUP BY id_product) ppl 
                        ON pp.id_product = ppl.id_product AND pp.price_list_date = ppl.price_list_date
                   JOIN Manufacturer_name mn ON p.id_manufacturer = mn.id_manufacturer
                   
                   WHERE name_product LIKE ?""",
                fields)

        if (entity == "client"):
            selected = self.cursor.execute(
                """SELECT * FROM Client WHERE (surname_client LIKE ?) AND (name_client LIKE ?) AND (patronymic_client LIKE ?)""",
                fields)

        if (entity == "seller"):
            selected = self.cursor.execute(
                """SELECT * FROM Seller WHERE (surname_seller LIKE ?) AND (name_seller LIKE ?) AND (patronymic_seller LIKE ?)""",
                fields)

        if (entity == "service"):
            selected = self.cursor.execute(
                """SELECT s.*, sp.cost_service 
                   FROM Service s JOIN Service_price sp ON s.id_service = sp.id_service
                   JOIN (SELECT MAX(price_list_date) as price_list_date, id_service
                         FROM Service_price GROUP BY id_service) spl 
                        ON sp.id_service = spl.id_service AND sp.price_list_date = spl.price_list_date
                   WHERE name_service LIKE ?""",
                fields)

        return (list(map(lambda x: x[0], selected.description)), selected.fetchall())

    def deleteById(self, ent_id, entity):
        """
        Deletes entity by id
        Returns:
            number of deleted

        """
        if (entity == "manufacturer"):
            # checking if there is country
            deleted = self.cursor.execute(
                "DELETE  FROM Manufacturer_name WHERE id_manufacturer = ?",
                ent_id).rowcount

        if (entity == "product"):
            deleted = self.cursor.execute(
                """DELETE FROM Product_material WHERE id_product = ?""",
                ent_id).rowcount
            print("Deleted rows: " + str(deleted))

            deleted = self.cursor.execute(
                """DELETE FROM Product_price WHERE id_product = ?""",
                ent_id).rowcount
            print("Deleted rows: " + str(deleted))

            deleted = self.cursor.execute(
                """DELETE FROM Product WHERE id_product = ?""",
                ent_id).rowcount

            print("Deleted rows: " + str(deleted))

        if (entity == "client"):
            deleted = self.cursor.execute(
                """DELETE FROM Client WHERE id_client = ?""",
                ent_id).rowcount
            print("Deleted rows: " + str(deleted))

        if (entity == "seller"):
            deleted = self.cursor.execute(
                """DELETE FROM Seller WHERE id_seller = ?""",
                ent_id).rowcount
            print("Deleted rows: " + str(deleted))

        if (entity == "service"):
            deleted = self.cursor.execute(
                """DELETE FROM Service_price WHERE id_service = ?""",
                ent_id).rowcount
            print("Deleted rows: " + str(deleted))

            deleted = self.cursor.execute(
                """DELETE FROM Service WHERE id_service = ?""",
                ent_id).rowcount
            print("Deleted rows: " + str(deleted))

        if (entity == "detail"):
            deleted = self.cursor.execute(
                """DELETE FROM Details_order WHERE id_details = ?""",
                ent_id).rowcount
            print("Deleted rows: " + str(deleted))

        self.cnxn.commit()
        return deleted

    def updateRow(self, row, entity):
        """
        Updates entities using row
        Args:
            row: list of str, used as args of update queries
            entity:

        Returns:
            number of updated rows
        """
        if (entity == "manufacturer"):
            # checking if there is country
            self.cursor.execute(
                "SELECT id_manufacturer_country FROM Manufacturer_country WHERE country_manufacturer = ?",
                row[2])
            res_row = self.cursor.fetchone()

            country_id = None
            if (res_row is None):
                country_id = self.insert("Manufacturer_country", ["country_manufacturer"], [row[2]])
                print("Inserted country with id: " + str(country_id))
            else:
                country_id = res_row[0]

            updated = self.cursor.execute(
                "UPDATE Manufacturer_name SET name_manufacturer = ?, id_manufacturer_country = ? WHERE id_manufacturer = ?",
                [row[1], country_id, row[0]])
            print("Updated rows: " + str(updated))

        if (entity == "product"):
            new_cost_id = self.insert("Product_price", ["id_product", "cost_product", "price_list_date"],
                                      [row[0], row[2], datetime.datetime.now()])

            print("Updated price: " + str(new_cost_id))

            self.cursor.execute(
                """SELECT id_manufacturer FROM Manufacturer_name 
                   WHERE name_manufacturer = ?""",
                row[3])

            res_row = self.cursor.fetchone()
            manu_id = None
            if (res_row is None):
                print("No such manufacturer: ")
                return -1
            else:
                manu_id = res_row[0]

            updated = self.cursor.execute(
                "UPDATE Product SET name_product = ?, product_availability = ?, id_manufacturer = ? WHERE id_product = ?",
                [row[1], row[4], manu_id, row[0]]).rowcount
            print("Updated rows: " + str(updated))


        if (entity == "client"):
            updated = self.cursor.execute(
                """UPDATE Client SET surname_client = ?, name_client = ?, patronymic_client = ?, phone_number_client = ? WHERE id_client = ?""",
                *row[1:], row[0]).rowcount
            print("Updated rows: " + str(updated))

        if (entity == "seller"):
            updated = self.cursor.execute(
                """UPDATE Seller SET surname_seller = ?, name_seller = ?, patronymic_seller = ?, 
                                     phone_number_seller = ?, position_seller = ? 
                   WHERE id_seller = ?""",
                *row[1:], row[0]).rowcount
            print("Updated rows: " + str(updated))

        if (entity == "service"):
            new_cost_id = self.insert("Service_price", ["id_service", "cost_service", "price_list_date"],
                                      [row[0], row[2], datetime.datetime.now()])

            print("Updated price: " + str(new_cost_id))

            updated = self.cursor.execute(
                """UPDATE Service SET name_service = ? WHERE id_service = ?""",
                row[1], row[0]).rowcount

            print("Updated rows: " + str(updated))

        self.cnxn.commit()
        return updated


global db
db = DataBase()