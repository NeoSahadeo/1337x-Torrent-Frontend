# 1337x Torrent Frontend (Beta)

<div align="center">
A simple frontend to automate torrent downloads.

![Preview](https://i.imgur.com/AK1BDWk.png)
</div>

## Setup

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

## Usage

There is a small search box in the middle top of the screen. After typing in a
query, you can press the search icon or hit `Enter` (return on the keyboard).
This will then load in the current contents of 1337x.

After that you may use the two `<` and `>` to navigate between pages. Page
number is indicated in the middle bottom of the screen.

Clicking on a torrent will select it and save it locally and you may freely
search for other torrents; they ones' selected will not be unselected.

After selecting your torrents, click on the `Queue Selected` button in the
bottom right corner to start the scrape. This will add the torrents to
qBittorrent.

## Roadmap

- Add in QoL buttons

## Contributions

"Talk is cheap, send patches" - Ffmpeg
