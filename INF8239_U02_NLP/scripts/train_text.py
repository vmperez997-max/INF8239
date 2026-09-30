from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from inf8239_u02.text_model import train
if __name__ == '__main__':
    print(train().to_string(index=False))

