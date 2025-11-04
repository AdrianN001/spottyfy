
# spottyfy
A spotify client in the terminal, made by Python. 
## 🚀 Features
- active lyrics sync
## 🔧 Installation
1. Clone the repository:  
   ```bash
    git clone https://github.com/AdrianN001/spottyfy.git
    cd spottyfy
    ```

2. Set up a virtual environment (recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate     # Unix/macOS
   venv\Scripts\activate        # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Usage

* To start the program:

  ```bash
  python main.py
  ```

* Additional modules:

  * `tui/` – contains the text interface
  * `spoti/` – handles Spotify/music integration logic
  * `lyrics/` – for lyrics functionality

## 🧩 Project Structure

```
spottyfy/
├── lyrics/
│   └── … (lyrics-related files)  
├── spoti/
│   └── … (Spotify/music integration)  
├── tui/
│   └── … (Text interface)  
├── main.py
├── requirements.txt
└── .gitignore
```

* `main.py` is the entry point.
* Subfolders separate components logically (UI vs logic).
* `requirements.txt` lists external libraries.

## 📝 Notes & Tips

* Make sure any required API keys or tokens are properly configured ( Spotify API and Scrape.Do)
* Pull requests are welcome if you want to add features like a GUI, more lyrics providers, etc.
* Be mindful of rate limits and API usage rules if integrating with music services.

## 💡 Ideas for Future Development

* Support for other music services (Apple Music, YouTube Music, etc.)
* Playlist import/export
* Theme support for the TUI

## 🧾 License

This project is licensed under the [MIT License](LICENSE) 

---

Thanks for checking out spottyfy! 🙏
If you have questions or suggestions, feel free to open an issue or contact me.

