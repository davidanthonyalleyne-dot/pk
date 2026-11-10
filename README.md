# PK

Walk Parkdale as Da Mayor with Yuki on the leash. Errands, the 501, twelve PK stickers between Queen and the Dufferin Gate.

It's a single page hosted free on GitHub Pages. The game itself is locked: `game.bin` is the whole game encrypted with AES-256, and only the access code opens it. Nothing playable sits in this repo in the clear, so it's safe for the repo to be public.

## 1. Put it on GitHub Pages

1. On github.com click **New repository**, name it `pk`, make it **Public** (Pages is free on public repos), and leave it empty.
2. On the empty repo page click **uploading an existing file** and drag in everything in this folder, including the `icons` and `tools` folders. On a Mac, press Cmd+Shift+. in Finder first so the hidden `.nojekyll` file shows up. Commit.
3. Go to **Settings**, then **Pages**. Under Build and deployment set Source to **Deploy from a branch**, pick **main** and **/ (root)**, and save.

After a minute it's live at `https://YOUR-USERNAME.github.io/pk/`.

## 2. Getting in

The first screen asks for the access code. Enter it once and the phone or computer remembers it, so the next visit goes straight to the title screen. Keep the code to yourself and the people you invite; it isn't written anywhere in this repo.

To invite someone, send them the link with the code on the end:

`https://YOUR-USERNAME.github.io/pk/#join=ABCD-EFGH-JKLM-NPQR`

Opening it once lets them in and remembers the code on their device. The code is then removed from the address bar.

To lock a device again, pause the game and tap **Lock this device**.

## 3. Changing the code

If the code leaks, make a new one (16 letters and numbers, no I, O, 0 or 1) and re-lock the game with the unlocked game page, which is kept out of this repo on purpose:

```
pip install cryptography
python3 tools/lock.py path/to/pk.html NEW1-CODE-GOES-HERE
```

Commit the new `game.bin`. Every game update is published the same way. Everyone on the old code is asked for the new one next time they open PK.

## 4. Add it to the home screen

On iPhone open the link in Safari, tap Share, then **Add to Home Screen**. It gets the sunset and CN Tower icon and opens full screen. On Android use Chrome's menu and **Add to Home screen**.
