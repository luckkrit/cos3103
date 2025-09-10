import pymysql
from enum import Enum

class Database:
    def __init__(self, host='localhost',port='', user='root', password='root', database='shop_db'):
        try:
            # By default, MySQL is autocommit but python is not autocommit by default
            self.connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                cursorclass=pymysql.cursors.DictCursor
            )
            print(f"Connected to database: {database}")
        except Exception as e:
            print(f"Failed to connect to database: {e}")
            raise
    
    def execute_non_query(self, sql, params=None):
        with self.connection.cursor() as cursor:
            try:
                affected_rows = cursor.execute(sql, params)
                self.connection.commit()
                return affected_rows
            except Exception as e:
                print(f"Error: {e}")
                self.connection.rollback()
                return -1

    def execute_query(self, sql, params=None):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(sql, params)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error executing query: {e}")
                raise

    def execute_single(self, sql, params=None):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(sql, params)
                result = cursor.fetchone()
                return result
            except Exception as e:
                print(f"Error executing single query: {e}")
                raise
    
    def get_last_insert_id(self):
        return self.connection.insert_id()
    
    def close(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()


class OrderStatus(Enum):
    SHIPPED = "shipped"
    IN_PROCESS = "In Process"

class Orders:
    def __init__(self, order_date,required_date,status:OrderStatus,customer_number,order_number=None, shipped_date=None, comments=None):
        self.order_number = order_number
        self.order_date = order_date
        self.required_date = required_date
        self.status = status
        self.customer_number = customer_number
        self.shipped_date = shipped_date
        self.comments = comments

class OrderDetails:
    def __init__(self, quantity_ordered, price_each, order_line_number, product_code ,order_number=None):
        self.order_number = order_number
        self.product_code = product_code
        self.quantity_ordered = quantity_ordered
        self.price_each = price_each
        self.order_line_number = order_line_number

class Store:
    def __init__(self,db: Database):
        self.db = db

    def get_order_number(self):
        result = self.db.execute_single("select MAX(ordernumber)+1 as order_number from orders")
        return result['order_number']

    def is_valid_product_code(self, product_code):
        result = self.db.execute_single("SELECT count(*) is_valid FROM products WHERE productCode = %s;", (product_code))
        return True if result["is_valid"] else False

    def is_valid_customer_number(self, customer_number):
        result = self.db.execute_single("SELECT count(*) is_valid FROM customers WHERE customerNumber = %s;", (customer_number))
        return True if result["is_valid"] else False

    def insert_order(self, orders:Orders, order_details:OrderDetails):

        with self.db.connection.cursor() as cursor:
            try:
                if not self.is_valid_customer_number(orders.customer_number):
                    raise ValueError(f"Customer number: {orders.customer_number} is not valid")
        
                if not self.is_valid_product_code(order_details.product_code):
                    raise ValueError(f"Product code: {order_details.product_code} is not valid")
                
                orders.order_number = self.get_order_number()
                order_details.order_number = orders.order_number
                affected_rows = cursor.execute("INSERT INTO orders (orderNumber,orderDate,requiredDate,shippedDate,status,comments,customerNumber) VALUES(%s,%s,%s,%s,%s,%s,%s);", (orders.order_number, orders.order_date, orders.required_date, orders.shipped_date, orders.status.value, orders.comments, orders.customer_number))

                # raise ValueError("Simulate error after insert table, rollback")

                affected_rows2 = cursor.execute("INSERT INTO orderdetails(orderNumber,productCode,quantityOrdered,priceEach,orderLineNumber) VALUES (%s,%s,%s,%s,%s);", (order_details.order_number, order_details.product_code, order_details.quantity_ordered, order_details.price_each, order_details.order_line_number))

                if affected_rows>0 and affected_rows2>0:
                    self.db.commit()
                else:
                    self.db.rollback()
                                

                return affected_rows
            except Exception as e:
                print(f"Error: {e}")
                self.db.rollback()
                return -1


if __name__ == '__main__':
    db = Database(database="classicmodels")
    store = Store(db=db)
    # print(store.get_order_number())
    # print(store.is_valid_product_code("S10_475"))
    # print(store.is_valid_customer_number("12"))

    orders = Orders(required_date="2005-06-07", order_date="2005-05-31", status=OrderStatus.IN_PROCESS, customer_number="121")
    order_details = OrderDetails(order_line_number=2, quantity_ordered=1,price_each=10.1, product_code="S32_1268")

    affected_rows = store.insert_order(orders=orders, order_details=order_details)
    print(f'Affected rows: {affected_rows}')