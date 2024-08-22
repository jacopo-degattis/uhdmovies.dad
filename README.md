# UhdMovies.dad streaming

## Description

A python utility to directly access video streaming from uhdmovies.dad.

Usuallly you should go through a url shortener called "tech.unblockedgames.world" then you should transfer the film to your drive or download the film locally.

Using this script you can get a url that provides the requeted film or episode stream that you can later use on VLC or any other movie player.

## Usage

First install required dependencies with:

```bash
pip3 install -r requirements.txt
```

and then

```bash
$ python3 main.py https://tech.unblockedgames.world/?sid=<ID>
```

A simple flask http server should be launched, now you can point with your local player like VLC directly to `http://localhost:3000/stream` to watch your movie or tv show.
