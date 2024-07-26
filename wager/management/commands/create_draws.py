from django.core.management.base import BaseCommand
from wager.models import pick1
from datetime import datetime, timedelta, time
import pytz


class Command(BaseCommand):
    help = "Manage pick1 draws"

    def handle(self, *args, **kwargs):
        self.manage_draws()

    def manage_draws(self):
        draw_times = {
            pick1.drawNameChoice.MORNING: {
                "draw_time": time(9, 58),  # 9:00 AM
                "game_time": time(10, 0),  # 10:00 AM
            },
            pick1.drawNameChoice.AFTERNOON: {
                "draw_time": time(13, 58),  # 1:00 PM
                "game_time": time(14, 0),  # 2:00 PM
            },
            pick1.drawNameChoice.EVENING: {
                "draw_time": time(18, 58),  # 6:00 PM
                "game_time": time(19, 0),  # 7:00 PM
            },
        }
        now = datetime.now(pytz.UTC)
        for draw_name, times in draw_times.items():
            self.create_draw(draw_name, now, times)

    def create_draw(self, draw_name, now, times):
        game_date_time = datetime.combine(now.date() + times["game_time"])
        draw_date_time = datetime.combine(now.date() + times["draw_time"])

        new_draw = pick1.objects.create(
            draw_number=pick1.objects.count(),
            draw_name=draw_name,
            draw_date=now.date(),
            draw_time=times["draw_time"],
            draw_date_time=draw_date_time,
            game_date_time=game_date_time,
        )
        self.stdout.write(
            self.style.SUCCESS(f"Successfully created draw {new_draw.draw_number}")
        )
