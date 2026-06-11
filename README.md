# 🎵 Ultimate Multilingual Discord Music Bot

A production-ready, high-performance Discord music bot featuring **Full Native Localization**. Not only do the chat messages adapt to the user's language, but the **slash command names and parameter descriptions change dynamically** based on each individual user's Discord client settings.

---

## 🚀 Advanced Features

* **Dynamic Command Localization:** The slash commands auto-translate natively within the Discord UI. An English user sees `/play`, a Turkish user sees `/oynat`, a Spanish user sees `/reproducir`, etc.
* **Zero-Freeze Async Streaming:** Uses `asyncio.to_thread` for `yt_dlp` extraction. Heavy searches execute in background threads, keeping the bot's core WebSocket loop perfectly stable.
* **FFmpeg Audio Optimization:** Configured with stream reconnection flags (`-reconnect 1`) and aggressive buffering (`probesize 32`) to eliminate mid-song stutters and start playing instantly.
* **Multi-Guild Isolation:** State management (`GuildMusicState`) keeps music queues, volumes, and loops completely separated and leak-free across unlimited servers.

---

## 🗺️ Native Command Mapping Matrix

The bot syncs directly with the Discord API to translate commands instantly. Here is how the core commands map across supported global languages:

| English (Default) | Türkçe | Español | Français | Deutsch | Português |
| --- | --- | --- | --- | --- | --- |
| **`/play`** | `/oynat` | `/reproducir` | `/lire` | `/spielen` | `/tocar` |
| **`/skip`** | `/geç` | `/saltar` | `/passer` | `/überspringen` | `/pular` |
| **`/queue`** | `/kuyruk` | `/cola` | `/file` | `/warteschlange` | `/fila` |
| **`/stop`** | `/kapat` | `/detener` | `/arreter` | `/stoppen` | `/parar` |
| **`/loop`** | `/döngü` | `/bucle` | `/boucle` | `/schleife` | `/loop` |
| **`/volume`** | `/ses` | `/volumen` | `/volume` | `/lautstärke` | `/volume` |
| **`/nowplaying`** | `/çalan-şarkı` | `/sonando` | `/actuel` | `/aktuelles` | `/tocando` |

---

## 🛠️ Requirements & Installation

### 1. Host Dependencies

* **Python 3.10+**
* **FFmpeg** installed on your host system environment and added to the system PATH.

### 2. Install Project Dependencies

Clone the repository and install the required global networking and audio encryption libraries:

```bash
git clone https://github.com/yourusername/localized-music-bot.git
cd localized-music-bot
pip install discord.py yt-dlp PyNaCl

```

---

## ⚙️ Deployment & Production Security

This project enforces secure token management using **Environment Variables**. Never hardcode sensitive production tokens into the script.

### Local Execution

```bash
# Linux/macOS
export DISCORD_TOKEN="your_bot_token_here"
python bot.py

# Windows (Command Prompt)
set DISCORD_TOKEN="your_bot_token_here"
python bot.py

```

### Cloud Providers (Railway, Heroku, Render, VPS)

Add `DISCORD_TOKEN` as a config variable/environment variable in your provider's dashboard, and include `PyNaCl` in your `requirements.txt` file to ensure secure voice packet encryption.

> ⚠️ **Note on Discord UI Syncing:** When running the bot for the first time, `bot.tree.sync()` will register all multi-language translations globally. If command names do not update instantly in your client, simply restart your Discord app or press `CTRL + R` to clear the local client cache.
