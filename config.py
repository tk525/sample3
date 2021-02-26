# from configparser import ConfigParser
# import os

# def db_setting():

#     host = os.environ['DB_HOSTNAME']
#     database = os.environ['DB_NAME']
#     user = os.environ['DB_USERNAME']
#     password = os.environ['DB_PASSWORD']
#     port=5432
#     return host, database, user, password, port


# # def config(filename='heroku.ini', section='postgresql'):
# def config(section='postgresql'):

#     parser = ConfigParser()

#     # parser.read(filename)
#     parser.read(
#         # host = os.environ['DB_HOSTNAME'],
#         # database = os.environ['DB_NAME'],
#         # user = os.environ['DB_USERNAME'],
#         # password = os.environ['DB_PASSWORD'],
#         # port=5432
#         db_setting()
#     )

#     # get section, default to postgresql
#     db = {}
#     if parser.has_section(section):
#         params = parser.items(section)
#         for param in params:
#             db[param[0]] = param[1]
#     else:
#         # raise Exception('Section {0} not found in the {1} file'.format(section, filename))
#         raise Exception('Section {0} not found in the {1} file'.format(section,
#             # host = os.environ['DB_HOSTNAME'],
#             # database = os.environ['DB_NAME'],
#             # user = os.environ['DB_USERNAME'],
#             # password = os.environ['DB_PASSWORD'],
#             # port=5432)
#             db_setting()
#             )
#         )

#     return db