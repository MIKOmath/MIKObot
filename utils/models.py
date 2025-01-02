from datetime import datetime

class Seminar:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.group = kwargs.get('group')
        self.start = kwargs.get('start')
        self.duration = kwargs.get('duration')
        self.difficulty = kwargs.get('difficulty')

        self.theme = kwargs.get('theme')
        self.description = kwargs.get('description')
        self.discord_channel_id = kwargs.get('discord_channel_id')
        self.tutors = kwargs.get('tutors')

        self.started = kwargs.get('started')
        self.finished = kwargs.get('finished')
        self.featured = kwargs.get('featured')
        self.special_guest = kwargs.get('special_guest')

        self.group_name = kwargs.get('group_name')
        self.group_role_id = kwargs.get('group_role_id')
        self.difficulty_label = kwargs.get('difficulty_label')
        self.difficulty_icon = kwargs.get('difficulty_icon')

    @staticmethod
    def _parse_start(date: str, time: str):
        date = datetime.strptime(date, '%Y-%m-%d').date()
        time = datetime.strptime(time, '%H:%M:%S').time()
        return datetime.combine(date, time)

    @staticmethod
    def _parse_duration(duration: str):
        return datetime.strptime(duration, '%H:%M:%S') - datetime(year=1900, month=1, day=1)

    @property
    def end(self):
        return self.start + self.duration

    @classmethod
    def from_json(cls, seminar):
        seminar['start'] = cls._parse_start(seminar['date'], seminar['time'])
        seminar['duration'] = cls._parse_duration(seminar['duration'])
        return cls(**seminar)
