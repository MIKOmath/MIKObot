from datetime import date
from aiohttp import ClientSession

from utils.models import Seminar

class ApiWrapper:
    def __init__(self):
        self.session = None

    async def setup(self, session: ClientSession):
        self.session = session

    async def fetch_seminars(self, start_date: date, end_date: date):
        url = f'seminars/?start_date={start_date or ''}&end_date={end_date or ''}&limit=100&display_only=1'
        async with self.session.get(url) as resp:
            data = await resp.json()
            if not data['count']:
                return []

            results = data['results']
            while data['next']:
                resp = await self.session.get(data['next'])
                data = await resp.json()
                results += data['results']

            return [Seminar.from_json(result) for result in results]

    async def fetch_seminar(self, seminar_id: int):
        url = f'seminars/{seminar_id}/?display_only=1'
        async with self.session.get(url) as resp:
            data = await resp.json()
            return Seminar.from_json(data)
