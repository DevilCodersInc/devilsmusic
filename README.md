# DevilCodes Music Telegram Bot - This is a pyrogram bot based on pytgcalls for playing songs or audio files in Telegram group voice chat
[![Devil](https://telegra.ph/file/f739907e5a8c8aa78e758.jpg)](https://t.me/devilcodes_inc)
## Notes
-The playlist function isn't available for now but will be given in next update. Avoid use of commands related to skip

-It is inspired from su music project and hamkercat's telegram voice bot.
Neither su music project , nor pytgcalls are stable

## Requirements

- FFmpeg
- NodeJS [nodesource.com](https://nodesource.com/)
- Python 3.7+
- [PyTgCalls](https://github.com/pytgcalls/pytgcalls)

## Deployment

### Config

Copy `example.env` to `.env` and fill it with your credentials.

### Without Docker

1. Install Python requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Run:
   ```bash
   python main.py
   ```

### Using Docker

1. Build:
   ```bash
   docker build -t musicplayer .
   ```
2. Run:
   ```bash
   docker run --env-file .env musicplayer
   ```

### Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/edguru/devilsmusic/)


## Credits
- [hamker cat](https://github.com/thehamkercat/Telegram_VC_Bot)
- [Roj](https://github.com/rojserbest)
- [Marvin](https://github.com/BlackStoneReborn)
- [Laky](https://github.com/Laky-64) & [Andrew](https://github.com/AndrewLaneX): PyTgCalls
