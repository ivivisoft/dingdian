import pymysql
import os

MYSQL_HOSTS = '127.0.0.1'
MYSQL_PORT = 3336
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'study'
MYSQL_DB = 'xiaoshuo'


cnx = pymysql.connect(
    host=MYSQL_HOSTS, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD, db=MYSQL_DB, use_unicode=True, charset='utf8')
cur = cnx.cursor()


class GenToFile:

    @classmethod
    def get_books(cls):
        sql = 'select xs_name ,category,xs_author, name_id   from dd_name  ORDER BY category'
        sqll = 'select t1.xs_chaptername,t1.xs_content from dd_chaptername t1, dd_name t2 WHERE t1.id_name = t2.name_id and t1.id_name =%(name_id)s order by t1.num_id'
        cur.execute(sql)
        result = cur.fetchall()
        for i in range(0, len(result)):
            GenToFile.mkdir(result[i][1])
            value = {
                'name_id': result[i][3]
            }
            cur.execute(sqll, value)
            book = cur.fetchall()
            f = open(result[i][0] + '.txt', 'a')
            for i in range(0, len(book)):
                f.writelines(book[i][0] + '\n' + book[i][1])
            f.close()

    @classmethod
    def mkdir(cls, path):
        path = path.strip()
        isExists = os.path.exists(
            os.path.join('/Users/andysoft/pythonwebdriver/dingdian/books', path))
        if not isExists:
            print('Create a dir:' + path)
            os.makedirs(
                os.path.join('/Users/andysoft/pythonwebdriver/dingdian/books', path))
            os.chdir(
                os.path.join('/Users/andysoft/pythonwebdriver/dingdian/books', path))
        else:
            print('The dir: ' + path + ' is already exists')
            os.chdir(
                os.path.join('/Users/andysoft/pythonwebdriver/dingdian/books', path))

GenToFile.get_books()
