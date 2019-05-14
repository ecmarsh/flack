# CS50W Project 2: _flack_

**_Slack + Flask (SocketIO) → Flack: Your Lightweight Single Page Chat App_**

![minty flack logo](static/assets/readme-entry.png 'Flack Logo')

**Python:** Flask/Flask-SocketIO
**Javascript:** AngularJS/SocketIO
**CSS:** Bootstrap/SCSS

## Usage

```txt
$ git clone github.com/ethan-marsh/flack.git dir/

$ pip install -r requirements.txt

$ flask run --no-reload
* Running on http://localhost:5000/
```

Flask-SocketIO package replaces the flask run command, so use --no-reload if you encounter a `ValueError`.

...Or just check out the project submission video:

[https://youtu.be/YZXYF0aUU_g](https://youtu.be/YZXYF0aUU_g 'CS50W - Project2: Flack w/ Flask SocketIO')

## **File Navigation**

### `requirements.txt`

- Flask and included packages
- Flask-SocketIO: Server communication for Flask
- Flask-Scss/Flask-Assets: Compile SCSS files to `styles.css`

### `helper.py`

- Lightweight helper functions for `application.py`.

### `channels.py`

- Class definition to store and organize messages.

### `application.py`

- App, SocketIO, and styles initalization.
- Globals:
  - `users`: a 'roster' of users stored by session.
  - `rooms`: The channels class instance to store messages.
- App functions: render the view and a request handler to create new channels.
- Server-side socketIO signal handlers to communicate with client (AngularJS controller).

### `static/js/`

- `controller.js`: The AngularJS controller to store local state, communicate with server, and update the views (`templates/`).
- `cookieFns.js`: Helper functions to set and get browser storage. Methods stored under global variable.

### `templates/`

- `layout.html`: External resourcer, header, and container Angular Controller.
- `index.html`: The single page chat app content.

### `sass/`

- Minimal base and component styles + some bootstrap overrides.
- Flask assets generates `styles.css`, the file used by the application (linked in `layout.html`).

**Personal Touch Spec:** Change your message colors using the new HTML5 color picker!
