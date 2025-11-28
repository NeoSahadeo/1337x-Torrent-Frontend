# 1337x Torrent Frontend (Beta)

> [!IMPORTANT]
> I am working on porting the app to a different platform. This is because there have been recent changes on 1337x that prevent my traditional way of webscraping.
>
> The App currently does not work.

<div align="center">
A simple frontend to automate torrent downloads.

![Preview](https://i.imgur.com/mWBhsnh.png)
</div>

## Download

[Download the latest binary](https://github.com/NeoSahadeo/1337x-Torrent-Frontend/releases/) and run it.

> [!IMPORTANT]
> 
> Make sure qBittorrent is open before running it
> or it will not open.

#### Example drun application entry

If you are using drun or another application launcher that uses `.desktop` you can create an entry like so

```
[Desktop Entry]
Name=1337xFrontEnd
Exec=/home/neosahadeo/Applications/1337xFrontEnd
Type=Application
```

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

## Contributions

### Things that need to be done

- Add in loading state + log dialog
- Add confirm dialog
- Create installer
- CLI to configure the qBitorrent client credentials

"Talk is cheap, send patches" - Ffmpeg
