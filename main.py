import sys
import threading
import logging
from PyQt5.QtWidgets import QApplication
from core.sip_engine import SipEngine
from api.server import start_api
from gui.main_window import MainWindow

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Initialize SIP Engine
    try:
        engine = SipEngine()
    except Exception as e:
        logging.error(f"Failed to initialize SIP engine: {e}")
        return

    # Start API Server in a background thread
    api_thread = threading.Thread(target=start_api, args=(engine,), daemon=True)
    api_thread.start()
    logging.info("API server started on http://127.0.0.1:8000")

    # Start GUI
    app = QApplication(sys.argv)
    window = MainWindow(engine)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
