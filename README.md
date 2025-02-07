# Spotify to YouTube Audio Downloader (Spotyload)

Este é um script Python que baixa faixas de áudio do YouTube com base em uma playlist do Spotify. O script utiliza a API do Spotify para obter os nomes das faixas de uma playlist e, em seguida, busca por esses títulos no YouTube utilizando o [pytube](https://pytube.io/). Após encontrar o vídeo, o áudio é baixado e convertido para MP3 usando o [yt-dlp](https://github.com/yt-dlp/yt-dlp).

O script permite que você:
- Baixe as músicas a partir de uma determinada faixa (por exemplo, iniciando pela faixa 100).
- Organize os arquivos de áudio em uma pasta especificada pelo usuário ou automaticamente com o nome da playlist, caso o usuário não informe um nome.
- Abstraia informações sensíveis (Spotify Client ID e Client Secret) utilizando variáveis de ambiente em um arquivo `.env`.

## Funcionalidades

- **Recuperação de Faixas:** Obtém as faixas de uma playlist do Spotify.
- **Busca no YouTube:** Utiliza o `pytube` para buscar vídeos relacionados às faixas sem depender da API oficial do YouTube. (Optei por não usar pois ela possui limite de 100 requisições /dia.)
- **Download e Conversão:** Baixa (WEBM) e converte o áudio dos vídeos para MP3 usando o `yt-dlp`.
- **Organização dos Arquivos:** Cria uma pasta para os downloads. Caso o usuário não informe um nome, utiliza o nome da playlist.
- **Configuração Segura:** Armazena as credenciais do Spotify em variáveis de ambiente, evitando expor dados sensíveis. 

## Dependências

- Python 3.6
- [FFmpeg](https://ffmpeg.org/) (para conversão de áudio)
- [Pytube](https://pytube.io/) (`pip install pytube`)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) (`pip install yt-dlp`)
- [python-dotenv](https://pypi.org/project/python-dotenv/) (`pip install python-dotenv`)
- [spotipy](https://spotipy.readthedocs.io/en/2.19.0/) (`pip install spotipy`)

## Pré-requisitos

- Python 3.6 ou superior.
- Conta de desenvolvedor no Spotify para obter o **Client ID** e o **Client Secret**. (Para isso acesse [Developer Spotify](https://developer.spotify.com/))
- [FFmpeg](https://ffmpeg.org/) instalado e configurado (necessário para a conversão de áudio via `yt-dlp`).
- Pytube instalado ``pip install pytube``
- Python-dotenv ``pip install python-dotenv``

## Configuração 

1. **Crie um arquivo .env na raiz do projeto com o seguinte conteúdo:**

   ```bash
   SPOTIFY_CLIENT_ID=seu_spotify_client_id
   SPOTIFY_CLIENT_SECRET=seu_spotify_client_secret


## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/spotify-to-youtube-downloader.git
   cd spotify-to-youtube-downloader

## Utilização

1. Para executar o script, substitua `<nome_do_arquivo.py>` pelo nome do arquivo principal e execute:

   ```bash
   python <nome_do_arquivo.py>

## Contribuição

Contribuições são bem-vindas! Se você deseja melhorar o projeto ou corrigir bugs, por favor abra uma issue ou envie um pull request.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
