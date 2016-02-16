import pusher

from main.settings import env


def get_pusher():
    return pusher.Pusher(
      app_id=env('PUSHER_APP_ID'),
      key=env('PUSHER_KEY'),
      secret=env('PUSHER_SECRET'),
      ssl=True,
      port=443
    )
