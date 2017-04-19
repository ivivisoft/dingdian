import pymysql


MYSQL_HOSTS = '127.0.0.1'
MYSQL_PORT = 3336
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'study'
MYSQL_DB = 'xiaoshuo'


sql = """
CREATE TABLE `dd_name`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `xs_name` varchar(255) DEFAULT NULL,
    `xs_author` varchar(255) DEFAULT NULL,
    `category` varchar(255) DEFAULT NULL,
    `name_id` varchar(255) DEFAULT NULL,
    PRIMARY KEY(`id`)
)ENGINE = InnoDB AUTO_INCREMENT = 38 DEFAULT CHARSET = utf8mb4
"""

sql1 = """
CREATE TABLE `dd_chaptername` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `xs_chaptername` varchar(255) DEFAULT NULL,
  `xs_content` text,
  `id_name` int(11) DEFAULT NULL,
  `num_id` int(11) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2726 DEFAULT CHARSET=utf8mb4;
SET FOREIGN_KEY_CHECKS=1;
"""


cnx = pymysql.connect(
    host=MYSQL_HOSTS, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD, db=MYSQL_DB, use_unicode=True, charset='utf8')
cur = cnx.cursor()


class Sql:

    @classmethod
    def insert_dd_name(cls, xs_name, xs_author, category, name_id):
        sql = 'insert into dd_name(`xs_name`,`xs_author`,`category`,`name_id`) values (%(xs_name)s,%(xs_author)s,%(category)s,%(name_id)s)'
        value = {
            'xs_name': xs_name,
            'xs_author': xs_author,
            'category': category,
            'name_id': name_id
        }
        cur.execute(sql, value)
        cnx.commit()

    @classmethod
    def select_name(cls, name_id):
        sql = 'select exists(select 1 from dd_name where name_id=%(name_id)s)'
        value = {
            'name_id': name_id
        }
        cur.execute(sql, value)
        return cur.fetchall()[0]

    @classmethod
    def insert_dd_chaptername(cls, xs_chaptername, xs_content, id_name, num_id, url):
        sql = 'insert into dd_chaptername(`xs_chaptername`,`xs_content`,`id_name`,`num_id`,`url`) values (%(xs_chaptername)s,%(xs_content)s,%(id_name)s,%(num_id)s,%(url)s)'
        value = {
            'xs_chaptername': xs_chaptername,
            'xs_content': xs_content,
            'id_name': id_name,
            'num_id': num_id,
            'url': url
        }
        cur.execute(sql, value)
        cnx.commit()

    @classmethod
    def select_chapter(cls, url):
        sql = 'select exists(select 1 from dd_chaptername where url=%(url)s)'
        value = {
            'url': url
        }

        cur.execute(sql, value)
        return cur.fetchall()[0]
