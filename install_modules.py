import subprocess
import sys

def install_modules():
    try:
        import nltk as nk
        import flask as fl
        import tqdm as tq
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'nltk'])
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'flask'])
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'tqdm'])
    finally:
        import nltk as nk
        import flask as fl
        import tqdm as tq
