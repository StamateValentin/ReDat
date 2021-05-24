import typing

from services.server.database.connection.connection import execute_sql


class TopicModel:
    def __init__(self, name, topic_id=0):
        self.topic_id = topic_id
        self.name = name
        self.url = f'https://www.reddit.com/r/{name}'

    def fetch_topic(self):
        db_topic = TopicModel.get_by_name(self.name)['object']

        self.topic_id = db_topic.topic_id
        self.name = db_topic.name

    # CRUD OPERATIONS
    def save(self):

        try:
            execute_sql(f"""INSERT INTO topics(name, url) VALUES ('{self.name}', '{self.url}')""")

            print(f"Topic {self.name} saved")
        except Exception as e:
            print(e)
            return {'status': False, 'message': 'Error at adding topic'}

        self.fetch_topic()

        return {'status': True, 'message': 'Topic created successfully'}

    # GETTERS
    @staticmethod
    def get_by_name(name):
        return TopicModel.__get_topic_by_key("name", f"'{name}'")

    @staticmethod
    def get_by_id(topic_id):
        return TopicModel.__get_topic_by_key("id", f"{topic_id}")

    @staticmethod
    def __get_topic_by_key(key, value):
        try:
            row = execute_sql(f"SELECT * FROM topics WHERE {key} = {value}")[0]
            topic = TopicModel(topic_id=row[0], name=row[1])
            return {'object': topic, 'message': 'Success'}
        except IndexError:
            return {'object': None, 'message': f"Topic with key:{key} and value:{value} not found"}

    @staticmethod
    def get_all() -> typing.List['TopicModel']:
        topics = []

        rows = execute_sql("SELECT * FROM topics")

        for row in rows:
            topics.append(TopicModel(topic_id=row[0], name=row[1]))

        return topics

    def __str__(self):
        return f"Topic {self.topic_id, self.name}"
