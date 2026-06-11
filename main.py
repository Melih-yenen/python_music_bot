import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp as youtube_dl
from collections import deque
import asyncio
from datetime import datetime, timezone

# 1. Çoklu Dil Sözlüğü (Localization Matrix)
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
        'lang_changed': "Bot dili başarıyla **Türkçe** olarak ayarlandı! 🇹🇷",
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
        'stopped_desc': "Music stopped, cleaned up, and disconnected from channel.",
        'not_connected': "The bot is not in a voice channel.",
        'loop_status': "Song loop: **{status}**", 'active': "Active 🔄", 'passive': "Passive ➡️",
        'paused': "⏸️ Paused", 'no_playing_err': "No song is currently playing.",
        'resumed': "▶️ Resumed", 'no_paused_err': "No song is currently paused.",
        'volume_success': "Volume set to **{volume}%**.", 'volume_err': "Value must be between 0 and 100.",
        'no_source_err': "No active audio source found.", 'ping': "Latency: **{latency:.2f}ms**",
        'lang_changed': "Bot language successfully set to **English**! 🇺🇸",
        'uptime': "Bot has been active for **{hours}** hours, **{minutes}** minutes, and **{seconds}** seconds.",
        'help_title': "📖 Music Bot Command Guide"
    },
    'es': {
        'error': "Error", 'not_in_voice': "¡Debes unirte a un canal de voz primero!",
        'searching': "🔍 Buscando...", 'searching_desc': "Obteniendo `{query}`...",
        'added_queue': "📥 Añadido a la Cola", 'added_queue_desc': "`{query}` añadido a la cola.",
        'now_playing': "🎵 Reproduciendo Ahora", 'skipped': "⏭️ Canción Saltada",
        'skipped_desc': "Pasando a la siguiente canción.", 'no_skip': "No hay ninguna canción reproduciéndose.",
        'queue_empty': "📋 Cola Vacía", 'queue_empty_desc': "No hay canciones en la cola.",
        'queue_title': "📋 Cola de Música Actual", 'queue_more': "\n*y {count} canciones más...*",
        'stopped_desc': "Música detenida, limpieza realizada y desconectado del canal.",
        'not_connected': "El bot no está en un canal de voz.",
        'loop_status': "Bucle de canción: **{status}**", 'active': "Activo 🔄", 'passive': "Pasivo ➡️",
        'paused': "⏸️ Pausado", 'no_playing_err': "No hay ninguna canción reproduciéndose.",
        'resumed': "▶️ Reanudado", 'no_paused_err': "No hay ninguna canción pausada.",
        'volume_success': "Volumen configurado al **{volume}%**.", 'volume_err': "El valor debe estar entre 0 y 100.",
        'no_source_err': "No se encontró ninguna fuente de audio activa.", 'ping': "Latencia: **{latency:.2f}ms**",
        'lang_changed': "¡Idioma del bot configurado en **Español**! 🇪🇸",
        'uptime': "El bot ha estado activo durante **{hours}** horas, **{minutes}** minutos y **{seconds}** segundos.",
        'help_title': "📖 Guía de Comandos de Música"
    },
    'fr': {
        'error': "Erreur", 'not_in_voice': "Vous devez d'abord rejoindre un salon vocal !",
        'searching': "🔍 Recherche...", 'searching_desc': "Récupération de `{query}`...",
        'added_queue': "📥 Ajouté à la File", 'added_queue_desc': "`{query}` ajouté à la file d'attente.",
        'now_playing': "🎵 En Cours de Lecture", 'skipped': "⏭️ Chanson Sautée",
        'skipped_desc': "Passage à la chanson suivante.", 'no_skip': "Aucune chanson en cours de lecture.",
        'queue_empty': "📋 File Vide", 'queue_empty_desc': "Il n'y a pas de chansons dans la file.",
        'queue_title': "📋 File d'Attente Actuelle", 'queue_more': "\n*et {count} autres chansons...*",
        'stopped_desc': "Musique arrêtée, nettoyage effectué et déconnecté du salon.",
        'not_connected': "Le bot n'est pas dans un salon vocal.",
        'loop_status': "Boucle de chanson : **{status}**", 'active': "Actif 🔄", 'passive': "Passif ➡️",
        'paused': "⏸️ En Pause", 'no_playing_err': "Aucune chanson en cours de lecture.",
        'resumed': "▶️ Reprise", 'no_paused_err': "Aucune chanson en pause.",
        'volume_success': "Volume réglé à **{volume}%**.", 'volume_err': "La valeur doit être comprise entre 0 et 100.",
        'no_source_err': "Aucune source audio active trouvée.", 'ping': "Latence: **{latency:.2f}ms**",
        'lang_changed': "Langue du bot configurée sur **Français** ! 🇫🇷",
        'uptime': "Le bot est actif depuis **{hours}** heures, **{minutes}** minutes et **{seconds}** secondes.",
        'help_title': "📖 Guide des Commandes de Musique"
    },
    'de': {
        'error': "Fehler", 'not_in_voice': "Du musst zuerst einem Sprachkanal beitreten!",
        'searching': "🔍 Suche...", 'searching_desc': "Hole `{query}`...",
        'added_queue': "📥 Zur Warteschlange hinzugefügt", 'added_queue_desc': "`{query}` zur Warteschlange hinzugefügt.",
        'now_playing': "🎵 Wird Jetzt Gespielt", 'skipped': "⏭️ Lied Übersprungen",
        'skipped_desc': "Weiter zum nächsten Lied.", 'no_skip': "Es wird gerade kein Lied gespielt.",
        'queue_empty': "📋 Warteschlange Leer", 'queue_empty_desc': "Es gibt keine Lieder in der Warteschlange.",
        'queue_title': "📋 Aktuelle Musik-Warteschlange", 'queue_more': "\n*und {count} weitere Lieder...*",
        'stopped_desc': "Musik gestoppt, aufgeräumt und vom Kanal getrennt.",
        'not_connected': "Der Bot ist in keinem Sprachkanal.",
        'loop_status': "Lied-Schleife: **{status}**", 'active': "Aktiv 🔄", 'passive': "Inaktiv ➡️",
        'paused': "⏸️ Pausiert", 'no_playing_err': "Es wird kein Lied gespielt.",
        'resumed': "▶️ Fortgesetzt", 'no_paused_err': "Es ist kein Lied pausiert.",
        'volume_success': "Lautstärke auf **{volume}%** eingestellt.", 'volume_err': "Wert muss zwischen 0 und 100 liegen.",
        'no_source_err': "Keine aktive Audioquelle gefunden.", 'ping': "Verzögerung: **{latency:.2f}ms**",
        'lang_changed': "Botsprache erfolgreich auf **Deutsch** gesetzt! 🇩🇪",
        'uptime': "Bot ist seit **{hours}** Stunden, **{minutes}** Minuten und **{seconds}** Sekunden aktiv.",
        'help_title': "📖 Musik-Bot Befehlsübersicht"
    },
    'pt': {
        'error': "Erro", 'not_in_voice': "Você deve entrar em um canal de voz primeiro!",
        'searching': "🔍 Buscando...", 'searching_desc': "Buscando `{query}`...",
        'added_queue': "📥 Adicionado à Fila", 'added_queue_desc': "`{query}` adicionado à fila.",
        'now_playing': "🎵 Tocando Agora", 'skipped': "⏭️ Música Pulada",
        'skipped_desc': "Passando para a próxima música.", 'no_skip': "Nenhuma música está tocando no momento.",
        'queue_empty': "📋 Fila Vazia", 'queue_empty_desc': "Não há músicas na fila.",
        'queue_title': "📋 Fila de Música Atual", 'queue_more': "\n*e mais {count} músicas...*",
        'stopped_desc': "Música parada, limpeza feita e desconectado do canal.",
        'not_connected': "O bot não está em um canal de voz.",
        'loop_status': "Loop de música: **{status}**", 'active': "Ativo 🔄", 'passive': "Inativo ➡️",
        'paused': "⏸️ Pausado", 'no_playing_err': "Nenhuma música tocando.",
        'resumed': "▶️ Continuado", 'no_paused_err': "Nenhuma música pausada.",
        'volume_success': "Volume definido para **{volume}%**.", 'volume_err': "O valor deve ser entre 0 e 100.",
        'no_source_err': "Nenhuma fonte de áudio ativa encontrada.", 'ping': "Latência: **{latency:.2f}ms**",
        'lang_changed': "Idioma do bot definido para **Português**! 🇵🇹",
        'uptime': "Bot ativo por **{hours}** horas, **{minutes}** minutos e **{seconds}** segundos.",
        'help_title': "📖 Guia de Comandos de Música"
    }
}

class GuildMusicState:
    def __init__(self):
        self.queue = deque()
        self.loop = False
        self.current_source = None
        self.current_title = None
        self.text_channel = None
        self.language = 'tr'  # Varsayılan dil Türkçe

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

bot = MusicBot()

YDL_OPTIONS = {
    'format': 'bestaudio/best', 'noplaylist': True, 'default_search': 'ytsearch',
    'quiet': True, 'no_warnings': True, 'extract_flat': False, 'source_address': '0.0.0.0'
}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 32', 'options': '-vn'
}

@bot.event
async def on_ready():
    bot.start_time = datetime.now(timezone.utc)
    print(f'Bot Aktif: {bot.user}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="müzik"))
    try:
        await bot.tree.sync()
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
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            return ydl.extract_info(query, download=False)
    return await asyncio.to_thread(sync_extract)

async def play_song(guild: discord.Guild, text_channel: discord.TextChannel, query: str):
    state = bot.get_state(guild.id)
    lang = LOCALIZATION[state.language]
    voice_client = guild.voice_client
    if not voice_client: return

    try:
        info = await fetch_song_info(query)
        if 'entries' in info and len(info['entries']) > 0:
            info = info['entries'][0]
        state.current_source, state.current_title = info['url'], info['title']
    except Exception:
        await text_channel.send(embed=discord.Embed(title=lang['error'], description="YouTube Error", color=0xff0000))
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
        def after_playing(error):
            asyncio.run_coroutine_threadsafe(check_queue_and_play(guild, text_channel), bot.loop)
        voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(state.current_source, **FFMPEG_OPTIONS)), after=after_playing)
    elif len(state.queue) > 0:
        await play_song(guild, text_channel, state.queue.popleft())
    else:
        state.current_source, state.current_title = None, None

# --- DİL AYARLAMA KOMUTU ---
@bot.tree.command(name='language', description='Botun dilini değiştirir / Changes the bot language.')
@app_commands.choices(lang=[
    app_commands.Choice(name="Türkçe 🇹🇷", value="tr"),
    app_commands.Choice(name="English 🇺🇸", value="en"),
    app_commands.Choice(name="Español 🇪🇸", value="es"),
    app_commands.Choice(name="Français 🇫🇷", value="fr"),
    app_commands.Choice(name="Deutsch 🇩🇪", value="de"),
    app_commands.Choice(name="Porteguês 🇵🇹", value="pt")
])
async def change_language(interaction: discord.Interaction, lang: app_commands.Choice[str]):
    state = bot.get_state(interaction.guild_id)
    state.language = lang.value
    
    lang_data = LOCALIZATION[state.language]
    embed = discord.Embed(title="Language / Dil", description=lang_data['lang_changed'], color=0x00ff00)
    await interaction.response.send_message(embed=embed)

# --- MÜZİK KOMUTLARI ---
@bot.tree.command(name='oynat', description='Şarkı çalar veya kuyruğa ekler.')
async def play(interaction: discord.Interaction, query: str):
    await interaction.response.defer()
    state = bot.get_state(interaction.guild_id)
    lang = LOCALIZATION[state.language]
    
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

@bot.tree.command(name='geç', description='Mevcut şarkıyı atlar.')
async def skip(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    state = bot.get_state(interaction.guild_id)
    lang = LOCALIZATION[state.language]
    
    if voice_client and voice_client.is_playing():
        curr_loop = state.loop
        state.loop = False
        voice_client.stop()
        state.loop = curr_loop
        await interaction.response.send_message(embed=discord.Embed(title=lang['skipped'], description=lang['skipped_desc'], color=0x00ff00))
    else:
        await interaction.response.send_message(embed=discord.Embed(title=lang['error'], description=lang['no_skip'], color=0xff0000))

@bot.tree.command(name='kuyruk', description='Kuyruğu listeler.')
async def queue_info(interaction: discord.Interaction):
    state = bot.get_state(interaction.guild_id)
    lang = LOCALIZATION[state.language]
    if len(state.queue) == 0:
        return await interaction.response.send_message(embed=discord.Embed(title=lang['queue_empty'], description=lang['queue_empty_desc'], color=0xffee00))
    
    q_list = "".join(f"**{i}.** {song}\n" for i, song in enumerate(list(state.queue)[:10], start=1))
    if len(state.queue) > 10: q_list += lang['queue_more'].format(count=len(state.queue)-10)
    await interaction.response.send_message(embed=discord.Embed(title=lang['queue_title'], description=q_list, color=0x00ff00))

@bot.tree.command(name='kapat', description='Kuyruğu temizler ve kanaldan çıkar.')
async def stop(interaction: discord.Interaction):
    state = bot.get_state(interaction.guild_id)
    voice_client = interaction.guild.voice_client
    lang = LOCALIZATION[state.language]

    state.loop, state.current_source, state.current_title = False, None, None
    state.queue.clear()

    if voice_client and (voice_client.is_playing() or voice_client.is_paused()):
        voice_client.stop()
        await voice_client.disconnect()
        await interaction.response.send_message(embed=discord.Embed(title="🛑 Stop", description=lang['stopped_desc'], color=0xff0000))
    else:
        await interaction.response.send_message(embed=discord.Embed(title=lang['error'], description=lang['not_connected'], color=0xff0000))

@bot.tree.command(name='döngü', description='Döngüyü açar/kapatır.')
async def loop_(interaction: discord.Interaction):
    state = bot.get_state(interaction.guild_id)
    lang = LOCALIZATION[state.language]
    state.loop = not state.loop
    status_str = lang['active'] if state.loop else lang['passive']
    await interaction.response.send_message(embed=discord.Embed(title="Loop", description=lang['loop_status'].format(status=status_str), color=0x00ff00))

@bot.tree.command(name='duraklat', description='Şarkıyı duraklatır.')
async def pause(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    lang = LOCALIZATION[state.language]
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await interaction.response.send_message(embed=discord.Embed(title=lang['paused'], color=0x00ff00))
    else:
        await interaction.response.send_message(embed=discord.Embed(title=lang['error'], description=lang['no_playing_err'], color=0xff0000))

@bot.tree.command(name='devam-et', description='Şarkıyı devam ettirir.')
async def resume(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    lang = LOCALIZATION[state.language]
    if voice_client and voice_client.is_paused():
        voice_client.resume()
        await interaction.response.send_message(embed=discord.Embed(title=lang['resumed'], color=0x00ff00))
    else:
        await interaction.response.send_message(embed=discord.Embed(title=lang['error'], description=lang['no_paused_err'], color=0xff0000))

@bot.tree.command(name='çalan-şarkı', description='Çalan şarkıyı gösterir.')
async def nowplaying(interaction: discord.Interaction):
    state = bot.get_state(interaction.guild_id)
    lang = LOCALIZATION[state.language]
    if state.current_title:
        await interaction.response.send_message(embed=discord.Embed(title=lang['now_playing'], description=f"**{state.current_title}**", color=0x00ff00))
    else:
        await interaction.response.send_message(embed=discord.Embed(title=lang['error'], description=lang['no_playing_err'], color=0xff0000))

@bot.tree.command(name='ses', description='Ses seviyesini ayarlar.')
async def volume(interaction: discord.Interaction, volume: int):
    voice_client = interaction.guild.voice_client
    state = bot.get_state(interaction.guild_id)
    lang = LOCALIZATION[state.language]
    if voice_client and voice_client.source:
        if 0 <= volume <= 100:
            voice_client.source.volume = volume / 100
            await interaction.response.send_message(embed=discord.Embed(title="Volume", description=lang['volume_success'].format(volume=volume), color=0x00ff00))
        else:
            await interaction.response.send_message(embed=discord.Embed(title=lang['error'], description=lang['volume_err'], color=0xff0000))
    else:
        await interaction.response.send_message(embed=discord.Embed(title=lang['error'], description=lang['no_source_err'], color=0xff0000))

@bot.tree.command(name='ping', description='Gecikmeyi ölçer.')
async def ping(interaction: discord.Interaction):
    state = bot.get_state(interaction.guild_id)
    lang = LOCALIZATION[state.language]
    await interaction.response.send_message(embed=discord.Embed(title="🏓 Pong", description=lang['ping'].format(latency=bot.latency*1000), color=0x00ff00))

@bot.tree.command(name='uptime', description='Aktif kalma süresi.')
async def uptime(interaction: discord.Interaction):
    state = bot.get_state(interaction.guild_id)
    lang = LOCALIZATION[state.language]
    if bot.start_time:
        delta = datetime.now(timezone.utc) - bot.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        await interaction.response.send_message(embed=discord.Embed(title="Uptime", description=lang['uptime'].format(hours=hours, minutes=minutes, seconds=seconds), color=0x00ff00))

@bot.tree.command(name="yardım", description="Komut rehberi.")
async def yardım(interaction: discord.Interaction):
    state = bot.get_state(interaction.guild_id)
    lang = LOCALIZATION[state.language]
    embed = discord.Embed(title=lang['help_title'], color=0x00ff00)
    embed.add_field(name="/language", value="tr, en, es, fr, de, pt", inline=True)
    embed.add_field(name="/oynat & /geç", value="Music control", inline=True)
    embed.add_field(name="/kuyruk & /kapat", value="Queue control", inline=True)
    await interaction.response.send_message(embed=embed)

bot.run('Bot token')
