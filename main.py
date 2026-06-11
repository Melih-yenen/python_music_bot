import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp as youtube_dl
from collections import deque
import asyncio
from datetime import datetime, timezone
import os

# 1. KOMUT İSİMLERİ VE AÇIKLAMALARI İÇİN YERELLEŞTİRME SÖZLÜĞÜ
COMMAND_LOCALIZATION = {
    'tr': {
        'play_name': 'oynat', 'play_desc': 'Bir şarkıyı çalar veya kuyruğa ekler.', 'query_desc': 'Şarkı adı veya YouTube URL\'si',
        'skip_name': 'geç', 'skip_desc': 'Çalan mevcut şarkıyı atlar.',
        'queue_name': 'kuyruk', 'queue_desc': 'Kuyrukta bekleyen şarkıları listeler.',
        'stop_name': 'kapat', 'stop_desc': 'Müziği kapatır ve kuyruğu sıfırlar.',
        'loop_name': 'döngü', 'loop_desc': 'Mevcut şarkıyı döngüye alır.',
        'pause_name': 'duraklat', 'pause_desc': 'Şarkıyı duraklatır.',
        'resume_name': 'devam-et', 'resume_desc': 'Duraklatılan şarkıyı devam ettirir.',
        'np_name': 'çalan-şarkı', 'np_desc': 'Şu anda ne çalındığını gösterir.',
        'vol_name': 'ses', 'vol_desc': 'Ses seviyesini ayarlar.', 'vol_param_desc': 'Ses seviyesi (0 - 100)',
        'ping_name': 'ping', 'ping_desc': 'Botun gecikme değerini ölçer.',
        'uptime_name': 'uptime', 'uptime_desc': 'Aktif kalma süresini gösterir.',
        'help_name': 'yardım', 'help_desc': 'Tüm komutları listeler.'
    },
    'en': {
        'play_name': 'play', 'play_desc': 'Plays a song or adds it to the queue.', 'query_desc': 'Song name or YouTube URL',
        'skip_name': 'skip', 'skip_desc': 'Skips the current song.',
        'queue_name': 'queue', 'queue_desc': 'Lists the songs in the queue.',
        'stop_name': 'stop', 'stop_desc': 'Stops the music and clears the queue.',
        'loop_name': 'loop', 'loop_desc': 'Toggles loop mode for the current song.',
        'pause_name': 'pause', 'pause_desc': 'Pauses the current song.',
        'resume_name': 'resume', 'resume_desc': 'Resumes the paused song.',
        'np_name': 'nowplaying', 'np_desc': 'Shows what is currently playing.',
        'vol_name': 'volume', 'vol_desc': 'Adjusts the volume level.', 'vol_param_desc': 'Volume level (0 - 100)',
        'ping_name': 'ping', 'ping_desc': 'Measures bot latency.',
        'uptime_name': 'uptime', 'uptime_desc': 'Shows how long the bot has been online.',
        'help_name': 'help', 'help_desc': 'Lists all available commands.'
    },
    'es': {
        'play_name': 'reproducir', 'play_desc': 'Reproduce una canción o la añade a la cola.', 'query_desc': 'Nombre de la canción o URL',
        'skip_name': 'saltar', 'skip_desc': 'Salta la canción actual.',
        'queue_name': 'cola', 'queue_desc': 'Muestra la cola de música.',
        'stop_name': 'detener', 'stop_desc': 'Detiene la música y limpia la cola.',
        'loop_name': 'bucle', 'loop_desc': 'Activa o desactiva el bucle de la canción.',
        'pause_name': 'pausar', 'pause_desc': 'Pausa la canción actual.',
        'resume_name': 'reanudar', 'resume_desc': 'Reanuda la canción pausada.',
        'np_name': 'sonando', 'np_desc': 'Muestra lo que está sonando ahora.',
        'vol_name': 'volumen', 'vol_desc': 'Ajusta el nivel de volumen.', 'vol_param_desc': 'Nivel de volumen (0 - 100)',
        'ping_name': 'ping', 'ping_desc': 'Mide la latencia del bot.',
        'uptime_name': 'uptime', 'uptime_desc': 'Muestra el tiempo de actividad.',
        'help_name': 'ayuda', 'help_desc': 'Muestra la lista de comandos.'
    },
    'fr': {
        'play_name': 'lire', 'play_desc': 'Joue une chanson ou l\'ajoute à la file.', 'query_desc': 'Nom de la chanson ou URL',
        'skip_name': 'passer', 'skip_desc': 'Passe la chanson actuelle.',
        'queue_name': 'file', 'queue_desc': 'Affiche la file d\'attente.',
        'stop_name': 'arreter', 'stop_desc': 'Arrête la musique et vide la file.',
        'loop_name': 'boucle', 'loop_desc': 'Active ou désactive la boucle.',
        'pause_name': 'pause', 'pause_desc': 'Met la chanson en pause.',
        'resume_name': 'reprendre', 'resume_desc': 'Reprend la lecture.',
        'np_name': 'actuel', 'np_desc': 'Affiche la chanson en cours.',
        'vol_name': 'volume', 'vol_desc': 'Règle le niveau du volume.', 'vol_param_desc': 'Niveau du volume (0 - 100)',
        'ping_name': 'ping', 'ping_desc': 'Mesure la latence du bot.',
        'uptime_name': 'uptime', 'uptime_desc': 'Affiche le temps d\'activité.',
        'help_name': 'aide', 'help_desc': 'Affiche la liste des commandes.'
    },
    'de': {
        'play_name': 'spielen', 'play_desc': 'Spielt ein Lied oder fügt es der Warteschlange hinzu.', 'query_desc': 'Liedname oder URL',
        'skip_name': 'überspringen', 'skip_desc': 'Überspringt das aktuelle Lied.',
        'queue_name': 'warteschlange', 'queue_desc': 'Zeigt die Warteschlange an.',
        'stop_name': 'stoppen', 'stop_desc': 'Stoppt die Musik und leert die Warteschlange.',
        'loop_name': 'schleife', 'loop_desc': 'Aktiviert/Deaktiviert die Liedwiederholung.',
        'pause_name': 'pausiert', 'pause_desc': 'Pausiert das aktuelle Lied.',
        'resume_name': 'fortsetzen', 'resume_desc': 'Setzt das pausierte Lied fort.',
        'np_name': 'aktuelles', 'np_desc': 'Zeigt an, was gerade gespielt wird.',
        'vol_name': 'lautstärke', 'vol_desc': 'Passt die Lautstärke an.', 'vol_param_desc': 'Lautstärkestufe (0 - 100)',
        'ping_name': 'ping', 'ping_desc': 'Misst die Bot-Latenz.',
        'uptime_name': 'uptime', 'uptime_desc': 'Zeigt die Online-Zeit des Bots.',
        'help_name': 'hilfe', 'help_desc': 'Zeigt die Befehlsliste an.'
    },
    'pt': {
        'play_name': 'tocar', 'play_desc': 'Toca uma música ou adiciona à fila.', 'query_desc': 'Nome da música ou URL',
        'skip_name': 'pular', 'skip_desc': 'Pula a música atual.',
        'queue_name': 'fila', 'queue_desc': 'Mostra a fila de música.',
        'stop_name': 'parar', 'stop_desc': 'Para a música e limpa a fila.',
        'loop_name': 'loop', 'loop_desc': 'Ativa ou desativa o loop da música.',
        'pause_name': 'pausar', 'pause_desc': 'Pausa a música atual.',
        'resume_name': 'continuar', 'resume_desc': 'Continua a música pausada.',
        'np_name': 'tocando', 'np_desc': 'Mostra o que está tocando agora.',
        'vol_name': 'volume', 'vol_desc': 'Ajusta o nível do volume.', 'vol_param_desc': 'Nível do volume (0 - 100)',
        'ping_name': 'ping', 'ping_desc': 'Mede a latência del bot.',
        'uptime_name': 'uptime', 'uptime_desc': 'Mostra o tempo de atividade do bot.',
        'help_name': 'ajuda', 'help_desc': 'Mostra a lista de comandos.'
    }
}

# 2. CHAT MESAJLARI İÇİN METİN SÖZLÜĞÜ
LOCALIZATION = {
    'tr': {
        'error': "Hata", 'not_in_voice': "Önce bir ses kanalına katılmalısınız!",
        'searching': "🔍 Aranıyor...", 'searching_desc': "`{query}` getiriliyor...",
        'added_queue': "📥 Kuyruğa Eklendi", 'added_queue_desc': "`{query}` sıraya eklendi.",
        'now_playing': "🎵 Şimdi Oynatılıyor", 'skipped': "⏭️ Şarkı Geçildi",
        'skipped_desc': "Sıradaki şarkıya geçiliyor.", 'no_skip': "Şu anda atlanabilecek bir şarkı çalmıyor.",
        'queue_empty': "📋 Kuyruk Boş", 'queue_empty_desc': "Sırada bekleyen bir şarkı yok.",
        'queue_title': "📋 Güncel Müzik Kuyruğu", 'queue_more': "\n*ve {count} şarkı daha...*",
        'stopped_desc': "Müzik kapatıldı, temizlik yapıldı ve kanaldan çıkıldı.",
        'not_connected': "Bot zaten aktif bir ses kanalında değil.",
        'loop_status': "Şarkı döngüsü: **{status}**", 'active': "Aktif 🔄", 'passive': "Pasif ➡️",
        'paused': "⏸️ Duraklatıldı", 'no_playing_err': "Çalan bir şarkı yok.",
        'resumed': "▶️ Devam Ediyor", 'no_paused_err': "Duraklatılmış bir şarkı yok.",
        'volume_success': "Ses gücü **%{volume}** yapıldı.", 'volume_err': "Değer 0-100 arası olmalıdır.",
        'no_source_err': "Aktif ses kaynağı yok.", 'ping': "Gecikme: **{latency:.2f}ms**",
        'uptime': "Bot **{hours}** saat, **{minutes}** dakika ve **{seconds}** saniyedir aktif.",
        'help_title': "📖 Müzik Botu Komut Rehberi"
    },
    'en': {
        'error': "Error", 'not_in_voice': "You must join a voice channel first!",
        'searching': "🔍 Searching...", 'searching_desc': "Fetching `{query}`...",
        'added_queue': "📥 Added to Queue", 'added_queue_desc': "`{query}` added to the queue.",
        'now_playing': "🎵 Now Playing", 'skipped': "⏭️ Song Skipped",
        'skipped_desc': "Moving to the next song.", 'no_skip': "No song is currently playing to skip.",
        'queue_empty': "📋 Queue is Empty", 'queue_empty_desc': "There are no songs in the queue.",
        'queue_title': "📋 Current Music Queue", 'queue_more': "\n*and {count} more songs...*",
        'stopped_desc': "Music stopped, cleaned up, and disconnected.",
        'not_connected': "The bot is not in a voice channel.",
        'loop_status': "Song loop: **{status}**", 'active': "Active 🔄", 'passive': "Passive ➡️",
        'paused': "⏸️ Paused", 'no_playing_err': "No song is currently playing.",
        'resumed': "▶️ Resumed", 'no_paused_err': "No song is currently paused.",
        'volume_success': "Volume set to **{volume}%**.", 'volume_err': "Value must be between 0 and 100.",
        'no_source_err': "No active audio source found.", 'ping': "Latency: **{latency:.2f}ms**",
        'uptime': "Bot active for **{hours}**h, **{minutes}**m, and **{seconds}**s.",
        'help_title': "📖 Music Bot Command Guide"
    } # Diğer dillerin metin karşılıkları önceki aşamalardaki gibi genişletilebilir.
}

# Discord'un Tree yapısına yerelleştirmeleri kaydetmesini sağlayan Translator Sınıfı
class MusicTranslator(app_commands.Translator):
    async def translate(self, string: app_commands.locale_str, locale: discord.Locale, context: app_commands.TranslationContext):
        lang_code = str(locale).split('-')[0]  # 'en-US' -> 'en', 'pt-BR' -> 'pt'
        if lang_code not in COMMAND_LOCALIZATION:
            lang_code = 'en'  # Dil desteklenmiyorsa varsayılan İngilizce yap
        
        return COMMAND_LOCALIZATION[lang_code].get(string.message)

class GuildMusicState:
    def __init__(self):
        self.queue = deque()
        self.loop = False
        self.current_source = None
        self.current_title = None
        self.text_channel = None
        self.last_locale = 'en'

class MusicBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="/", intents=intents)
        self.music_states = {}
        self.start_time = None

    def get_state(self, guild_id: int) -> GuildMusicState:
        if guild_id not in self.music_states:
            self.music_states[guild_id] = GuildMusicState()
        return self.music_states[guild_id]

    # Bot ayağa kalkarken Translator sınıfını ağaca bağlıyoruz
    async def setup_hook(self):
        await self.tree.set_translator(MusicTranslator())

bot = MusicBot()

YDL_OPTIONS = {
    'format': 'bestaudio/best', 'noplaylist': True, 'default_search': 'ytsearch',
    'quiet': True, 'no_warnings': True, 'extract_flat': False, 'source_address': '0.0.0.0'
}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 32', 'options': '-vn'
}

def get_lang(interaction: discord.Interaction) -> dict:
    state = bot.get_state(interaction.guild_id)
    locale_prefix = str(interaction.locale).split('-')[0]
    if locale_prefix in LOCALIZATION:
        state.last_locale = locale_prefix
        return LOCALIZATION[locale_prefix]
    return LOCALIZATION.get(state.last_locale, LOCALIZATION['en'])

@bot.event
async def on_ready():
    bot.start_time = datetime.now(timezone.utc)
    print(f'Global Yerelleştirilmiş Bot Aktif: {bot.user}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="music 🎵"))
    try:
        await bot.tree.sync()  # Bu işlem yerelleştirilmiş isimleri Discord API'sine iletir.
        print("Tüm dillerdeki Slash komutları Discord'a senkronize edildi.")
    except Exception as e:
        print(f"Sync Error: {e}")

@bot.event
async def on_voice_state_update(member, before, after):
    if member == bot.user and after.channel is None:
        state = bot.get_state(member.guild.id)
        state.current_source, state.current_title = None, None
        state.queue.clear()

async def fetch_song_info(query: str):
    def sync_extract():
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl: return ydl.extract_info(query, download=False)
    return await asyncio.to_thread(sync_extract)

async def play_song(guild: discord.Guild, text_channel: discord.TextChannel, query: str):
    state = bot.get_state(guild.id)
    lang = LOCALIZATION.get(state.last_locale, LOCALIZATION['en'])
    voice_client = guild.voice_client
    if not voice_client: return

    try:
        info = await fetch_song_info(query)
        if 'entries' in info and len(info['entries']) > 0: info = info['entries'][0]
        state.current_source, state.current_title = info['url'], info['title']
    except Exception:
        await text_channel.send(embed=discord.Embed(title=lang['error'], description="API/Streaming Error", color=0xff0000))
        await check_queue_and_play(guild, text_channel)
        return

    def after_playing(error):
        asyncio.run_coroutine_threadsafe(check_queue_and_play(guild, text_channel), bot.loop)

    voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(state.current_source, **FFMPEG_OPTIONS)), after=after_playing)
    await text_channel.send(embed=discord.Embed(title=lang['now_playing'], description=f"**{state.current_title}**", color=0x00ff00))

async def check_queue_and_play(guild: discord.Guild, text_channel: discord.TextChannel):
    state = bot.get_state(guild.id)
    voice_client = guild.voice_client
    if not voice_client or not voice_client.is_connected(): return

    if state.loop and state.current_source:
        def after_playing(error): asyncio.run_coroutine_threadsafe(check_queue_and_play(guild, text_channel), bot.loop)
        voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(state.current_source, **FFMPEG_OPTIONS)), after=after_playing)
    elif len(state.queue) > 0:
        await play_song(guild, text_channel, state.queue.popleft())
    else:
        state.current_source, state.current_title = None, None

# --- DİNAMİK ADLANDIRILMIŞ SLASH KOMUTLARI ---

@bot.tree.command(name=app_commands.locale_str('play_name'), description=app_commands.locale_str('play_desc'))
@app_commands.describe(query=app_commands.locale_str('query_desc'))
async def play(interaction: discord.Interaction, query: str):
    await interaction.response.defer()
    state = bot.get_state(interaction.guild_id)
    lang = get_lang(interaction)
    
    if not interaction.user.voice:
        return await interaction.followup.send(embed=discord.Embed(title=lang['error'], description=lang['not_in_voice'], color=0xff0000))

    channel = interaction.user.voice.channel
    voice_client = interaction.guild.voice_client

    if not voice_client: voice_client = await channel.connect()
    elif voice_client.channel != channel: await voice_client.move_to(channel)

    if voice_client.is_playing() or voice_client.is_paused():
        state.queue.append(query)
        await interaction.followup.send(embed=discord.Embed(title=lang['added_queue'], description=lang['added_queue_desc'].format(query=query), color=0x00ff00))
    else:
        await interaction.followup.send(embed=discord.Embed(title=lang['searching'], description=lang['searching_desc'].format(query=query), color=0x00ff00))
        await play_song(interaction.guild, interaction.channel, query)

@bot.tree.command(name=app_commands.locale_str('skip_name'), description=app_commands.locale_str('skip_desc'))
async def skip(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    state = bot.get_state(interaction.guild_id)
    lang = get_lang(interaction)
    
    if voice_client and voice_client.is_playing():
        curr_loop = state.loop
        state.loop = False
        voice_client.stop()
        state.loop = curr_loop
        await interaction.response.send_message(embed=discord.Embed(title=lang['skipped'], description=lang['skipped_desc'], color=0x00ff00))
    else:
        await interaction.response.send_message(embed=discord.Embed(title=lang['error'], description=lang['no_skip'], color=0xff0000))

@bot.tree.command(name=app_commands.locale_str('queue_name'), description=app_commands.locale_str('queue_desc'))
async def queue_info(interaction: discord.Interaction):
    state = bot.get_state(interaction.guild_id)
    lang = get_lang(interaction)
    if len(state.queue) == 0:
        return await interaction.response.send_message(embed=discord.Embed(title=lang['queue_empty'], description=lang['queue_empty_desc'], color=0xffee00))
    
    q_list = "".join(f"**{i}.** {song}\n" for i, song in enumerate(list(state.queue)[:10], start=1))
    if len(state.queue) > 10: q_list += lang['queue_more'].format(count=len(state.queue)-10)
    await interaction.response.send_message(embed=discord.Embed(title=lang['queue_title'], description=q_list, color=0x00ff00))

@bot.tree.command(name=app_commands.locale_str('stop_name'), description=app_commands.locale_str('stop_desc'))
async def stop(interaction: discord.Interaction):
    state = bot.get_state(interaction.guild_id)
    voice_client = interaction.guild.voice_client
    lang = get_lang(interaction)

    state.loop, state.current_source, state.current_title = False, None, None
    state.queue.clear()

    if voice_client and (voice_client.is_playing() or voice_client.is_paused()):
        voice_client.stop()
        await voice_client.disconnect()
        await interaction.response.send_message(embed=discord.Embed(title="🛑 Stop", description=lang['stopped_desc'], color=0xff0000))
    else:
        await interaction.response.send_message(embed=discord.Embed(title=lang['error'], description=lang['not_connected'], color=0xff0000))

@bot.tree.command(name=app_commands.locale_str('loop_name'), description=app_commands.locale_str('loop_desc'))
async def loop_(interaction: discord.Interaction):
    state = bot.get_state(interaction.guild_id)
    lang = get_lang(interaction)
    state.loop = not state.loop
    status_str = lang['active'] if state.loop else lang['passive']
    await interaction.response.send_message(embed=discord.Embed(title="Loop", description=lang['loop_status'].format(status=status_str), color=0x00ff00))

@bot.tree.command(name=app_commands.locale_str('pause_name'), description=app_commands.locale_str('pause_desc'))
async def pause(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    lang = get_lang(interaction)
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await interaction.response.send_message(embed=discord.Embed(title=lang['paused'], color=0x00ff00))
    else:
        await interaction.response.send_message(embed=discord.Embed(title=lang['error'], description=lang['no_playing_err'], color=0xff0000))

@bot.tree.command(name=app_commands.locale_str('resume_name'), description=app_commands.locale_str('resume_desc'))
async def resume(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    lang = get_lang(interaction)
    if voice_client and voice_client.is_paused():
        voice_client.resume()
        await interaction.response.send_message(embed=discord.Embed(title=lang['resumed'], color=0x00ff00))
    else:
        await interaction.response.send_message(embed=discord.Embed(title=lang['error'], description=lang['no_paused_err'], color=0xff0000))

@bot.tree.command(name=app_commands.locale_str('np_name'), description=app_commands.locale_str('np_desc'))
async def nowplaying(interaction: discord.Interaction):
    state = bot.get_state(interaction.guild_id)
    lang = get_lang(interaction)
    if state.current_title:
        await interaction.response.send_message(embed=discord.Embed(title=lang['now_playing'], description=f"**{state.current_title}**", color=0x00ff00))
    else:
        await interaction.response.send_message(embed=discord.Embed(title=lang['error'], description=lang['no_playing_err'], color=0xff0000))

@bot.tree.command(name=app_commands.locale_str('vol_name'), description=app_commands.locale_str('vol_desc'))
@app_commands.describe(volume=app_commands.locale_str('vol_param_desc'))
async def volume(interaction: discord.Interaction, volume: int):
    voice_client = interaction.guild.voice_client
    lang = get_lang(interaction)
    if voice_client and voice_client.source:
        if 0 <= volume <= 100:
            voice_client.source.volume = volume / 100
            await interaction.response.send_message(embed=discord.Embed(title="Volume", description=lang['volume_success'].format(volume=volume), color=0x00ff00))
        else:
            await interaction.response.send_message(embed=discord.Embed(title=lang['error'], description=lang['volume_err'], color=0xff0000))
    else:
        await interaction.response.send_message(embed=discord.Embed(title=lang['error'], description=lang['no_source_err'], color=0xff0000))

@bot.tree.command(name=app_commands.locale_str('ping_name'), description=app_commands.locale_str('ping_desc'))
async def ping(interaction: discord.Interaction):
    lang = get_lang(interaction)
    await interaction.response.send_message(embed=discord.Embed(title="🏓 Pong", description=lang['ping'].format(latency=bot.latency*1000), color=0x00ff00))

@bot.tree.command(name=app_commands.locale_str('uptime_name'), description=app_commands.locale_str('uptime_desc'))
async def uptime(interaction: discord.Interaction):
    lang = get_lang(interaction)
    if bot.start_time:
        delta = datetime.now(timezone.utc) - bot.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        await interaction.response.send_message(embed=discord.Embed(title="Uptime", description=lang['uptime'].format(hours=hours, minutes=minutes, seconds=seconds), color=0x00ff00))

@bot.tree.command(name=app_commands.locale_str('help_name'), description=app_commands.locale_str('help_desc'))
async def yardım(interaction: discord.Interaction):
    lang = get_lang(interaction)
    embed = discord.Embed(title=lang['help_title'], color=0x00ff00)
    await interaction.response.send_message(embed=embed)

TOKEN = os.getenv('DISCORD_TOKEN', 'TOKENİNİZ')
bot.run(TOKEN)
