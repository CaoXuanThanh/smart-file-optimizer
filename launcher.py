"""Entry point for the portable Windows distribution."""
from pathlib import Path
import sys


def main():
    root = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))
    sys.path.insert(0, str(root / 'src'))
    from streamlit.web import cli
    sys.argv = ['streamlit', 'run', str(root / 'app.py'),
                '--global.developmentMode=false',
                '--server.address=127.0.0.1', '--server.port=8501',
                '--server.headless=false', '--server.showEmailPrompt=false',
                '--server.fileWatcherType=none',
                '--browser.gatherUsageStats=false']
    print('Smart File Optimizer: http://127.0.0.1:8501')
    print('Keep this window open. Close it to stop the application.')
    return cli.main()


if __name__ == '__main__':
    raise SystemExit(main())
