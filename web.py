from textual_serve.server import Server

def main() -> None:
    Server("source venv/bin/activate && python3 main.py").serve(True)

if __name__ == "__main__": 
    main()
