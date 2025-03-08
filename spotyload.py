import os
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import Search
import yt_dlp as youtube_dl
from dotenv import load_dotenv
import concurrent.futures

load_dotenv()

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

# Caminho base onde as músicas serão salvas (exemplo: pen drive em E:\)
BASE_DOWNLOAD_PATH = "E:\\"  # Utilize duas barras invertidas para o caminho correto

def extract_playlist_id(url):
    match = re.search(r'playlist/([a-zA-Z0-9]+)', url)
    return match.group(1) if match else None

def get_spotify_tracks(playlist_id):
    """Obtém os nomes das músicas do Spotify no formato 'Artista - Título'."""
    auth = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    )
    sp = spotipy.Spotify(client_credentials_manager=auth)
    
    tracks = []
    try:
        results = sp.playlist_tracks(playlist_id)
        while results:
            for item in results['items']:
                track = item['track']
                if track:
                    artist = track['artists'][0]['name']
                    tracks.append(f"{artist} - {track['name']}")
            results = sp.next(results) if results['next'] else None
        return tracks
    except Exception as e:
        print(f"Erro no Spotify: {e}")
        return []

def get_playlist_name(playlist_id):
    """Obtém o nome da playlist do Spotify."""
    try:
        auth = SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET
        )
        sp = spotipy.Spotify(client_credentials_manager=auth)
        playlist_data = sp.playlist(playlist_id)
        return playlist_data.get('name', 'playlist_downloads')
    except Exception as e:
        print(f"Não foi possível obter o nome da playlist: {e}")
        return 'playlist_downloads'

def search_youtube(query):
    """Busca vídeos no YouTube utilizando pytube e retorna o URL do primeiro resultado."""
    try:
        search = Search(query)
        results = search.results
        if results:
            return results[0].watch_url
        else:
            return None
    except Exception as e:
        print(f"Erro na busca do YouTube para '{query}': {e}")
        return None

def download_audio(url, download_path):
    """Baixa o áudio do YouTube usando yt-dlp e converte para MP3."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',  # Qualidade do áudio (128, 192, 256, 320)
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        print(f"Erro ao baixar: {e}")
        return False

def process_track(track, download_path):
    """Processa uma música: busca no YouTube e baixa o áudio."""
    video_url = search_youtube(track)
    if video_url:
        print(f"\n⬇️ Baixando: {track}")
        success = download_audio(video_url, download_path)
        print("✅ Sucesso!" if success else "❌ Falha!")
    else:
        print(f"⚠️ Não encontrado: {track}")

def main():
    # Solicita a URL da playlist do Spotify
    playlist_url = input("Cole o link da playlist do Spotify: ").strip()
    playlist_id = extract_playlist_id(playlist_url)
    if not playlist_id:
        print("❌ Link inválido!")
        return

    # Solicita o nome da pasta onde as músicas serão salvas
    folder_name = input("Informe o nome da pasta onde as músicas serão salvas (deixe vazio para usar o nome da playlist): ").strip()
    if not folder_name:
        folder_name = get_playlist_name(playlist_id)
    
    # Cria o caminho final de download unindo o BASE_DOWNLOAD_PATH e o nome da pasta
    final_download_path = os.path.join(BASE_DOWNLOAD_PATH, folder_name)
    os.makedirs(final_download_path, exist_ok=True)
    print(f"As músicas serão salvas em: {final_download_path}")

    # Obtém as músicas da playlist do Spotify
    print("\n🔍 Obtendo músicas da playlist...")
    tracks = get_spotify_tracks(playlist_id)
    if not tracks:
        print("❌ Nenhuma música encontrada!")
        return
    
    total_tracks = len(tracks)
    print(f"🎵 Total de músicas na playlist do Spotify: {total_tracks}")

    # Verifica quantas músicas já foram baixadas (arquivos .mp3)
    local_files = [f for f in os.listdir(final_download_path) if f.lower().endswith('.mp3')]
    local_count = len(local_files)
    print(f"💾 Músicas já baixadas: {local_count}")

    if local_count >= total_tracks:
        print("✅ Todas as músicas já foram baixadas!")
        return
    else:
        # Assume que as músicas foram baixadas na mesma ordem da playlist
        tracks_to_download = tracks[local_count:]
        print(f"⬇️ Baixando {len(tracks_to_download)} músicas faltantes...")

    # Utiliza multithreading para processar os downloads em paralelo
    with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
        futures = [executor.submit(process_track, track, final_download_path) for track in tracks_to_download]
        concurrent.futures.wait(futures)
    
    print("\nConcluído!")

if __name__ == "__main__":
    main()
