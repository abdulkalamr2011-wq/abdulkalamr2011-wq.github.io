# Chess Bot for Computer Games

This is a Chrome extension that reads the visible board and uses Stockfish.js 19 Lite (single-threaded WebAssembly) to choose moves for the active side on Chess.com or Lichess. The engine is bundled locally; gameplay does not send positions to an external service.

## Install in Chrome

1. Open `chrome://extensions`.
2. Turn on **Developer mode**.
3. Select **Load unpacked** and choose this `browser-chess-bot` folder.
4. Open a game against the site's computer opponent and press **Start** in the Chess Bot panel.

The extension reads the visible board and uses Chrome's debugger permission to send mouse input to the active chess tab. Chrome may show a debugger access warning when you reload or use the extension. It currently supports Chess.com and Lichess; other sites need their own board adapter. Use it only in computer games where automation is allowed.

Stockfish.js is licensed under GPL-3.0; its license text is in `COPYING.txt`. Upstream source and engine details: https://github.com/nmrugg/stockfish.js

