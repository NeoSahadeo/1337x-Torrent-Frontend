# 1337x Torrent Frontend (Beta)

<div align="center">
A simple frontend to automate torrent downloads.

![Preview](https://i.imgur.com/mWBhsnh.png)
</div>

## Setup

As the app is in beta, Linux has first class support (because it's the only
thing I use). Other platforms may require more steps.

__Clone le repo__

```bash
git clone --depth=1 https://github.com/NeoSahadeo/1337x-Torrent-Frontend
cd 1337x-Torrent-Frontend
```

__qBittorrent__
Change the login details to your qBittorrent details in `main.py`.

__Install__
```bash
pip install -r requirements.txt
```

__Run__
```bash
python main.py
```

If you would like to install it, run this.

__Python Installer__

## Usage

Make sure qBitorrent is open before running the app.

Use the searchbox in the top left to search for torrents. This will scrape
1337x and display it.

After that you can click on the checkbox, or click on the text of the torrent
to select it.

Once selected you may search for other torrents

After you're done, click on `Queue Selected` to add those torrents to
qBitorrent.

## Roadmap

- Add in QoL buttons

## Contributions

"Talk is cheap, send patches" - Ffmpeg
