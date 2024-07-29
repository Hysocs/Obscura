# exclusions.py
EXCLUDED_NAMES = {
    # Python built-ins (expanded list)
    'self', 'cls', 'super', 'object', 'int', 'str', 'list', 'dict', 'set', 'tuple',
    'print', 'len', 'range', 'input', 'open', 'close', 'write', 'read', 'append', 'insert', 'remove', 'pop',
    'format', 'split', 'join', 'replace', 'strip', 'startswith', 'endswith', 'lower', 'upper', 'capitalize',
    'sort', 'sorted', 'reverse', 'reversed', 'index', 'count', 'find', 'max', 'min', 'sum', 'abs', 'all', 'any',
    'map', 'filter', 'reduce', 'zip', 'enumerate', 'dir', 'help', 'type', 'isinstance', 'issubclass', 'id',
    'hex', 'bin', 'oct', 'ord', 'chr', 'round', 'pow', 'divmod', 'vars', 'globals', 'locals', 'exec', 'eval',
    'compile', 'getattr', 'setattr', 'hasattr', 'delattr', 'callable', 'iter', 'next', 'slice', 'staticmethod',
    'classmethod', 'property', 'frozenset', 'bytearray', 'bytes', 'memoryview', 'complex', 'float', 'bool',
    'True', 'False', 'None', 'Exception', 'BaseException', 'KeyboardInterrupt', 'SystemExit', 'GeneratorExit',
    'StopIteration', 'ArithmeticError', 'AssertionError', 'AttributeError', 'EOFError', 'ImportError',
    'ModuleNotFoundError', 'IndexError', 'KeyError', 'MemoryError', 'NameError', 'OSError', 'OverflowError',
    'ReferenceError', 'RuntimeError', 'SyntaxError', 'IndentationError', 'TabError', 'SystemError',
    'TypeError', 'UnboundLocalError', 'UnicodeError', 'ValueError', 'ZeroDivisionError', 'connect',

    # Double underscore methods (expanded list)
    '__init__', '__str__', '__repr__', '__dict__', '__module__', '__weakref__', '__name__', '__main__',
    '__file__', '__path__', '__doc__', '__annotations__', '__call__', '__class__', '__del__', '__delattr__',
    '__dir__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__gt__', '__hash__',
    '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__setattr__', '__sizeof__',
    '__subclasshook__', '__version__', '__author__', '__email__', '__import__',

    # Python keywords
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield',

    # Common library names (expanded list)
    'os', 'sys', 'json', 'logging', 'random', 'string', 'hashlib', 'base64', 'zlib', 'marshal', 'ast', 'astunparse',
    'deque', 'collections', 'itertools', 'functools', 'datetime', 'time', 're', 'math', 'statistics', 'subprocess',
    'threading', 'multiprocessing', 'socket', 'ssl', 'urllib', 'http', 'unittest', 'doctest', 'pdb', 'argparse',
    'configparser', 'shutil', 'tempfile', 'glob', 'fnmatch', 'pathlib', 'sqlite3', 'decimal', 'fractions',

    # GUI-related names (expanded list)
    'QMessageBox', 'QApplication', 'QWidget', 'QPushButton', 'QLabel', 'QLineEdit', 'QVBoxLayout', 'QHBoxLayout',
    'QGridLayout', 'QComboBox', 'QCheckBox', 'QRadioButton', 'QTextEdit', 'QMainWindow', 'QFileDialog', 'QColorDialog',
    'QFontDialog', 'QFont', 'QIcon', 'QPixmap', 'QImage', 'QPainter', 'QPen', 'QBrush', 'QRect', 'QSize', 'QAction',
    'QTimer', 'QFrame', 'QGroupBox', 'QStackedWidget', 'QSpacerItem', 'QSizePolicy',

    # Cryptography-related names
    'AES', 'pad', 'unpad', 'Fernet', 'hashlib', 'hmac', 'pbkdf2_hmac', 'secrets', 'rsa', 'ecc', 'dsa', 'pki',

    # User-defined class and function names
    'name_generator', 'CodeEncryptor', 'NameGenerator', 'CodeGenerator', 'CodeValidator', 'EXCLUDED_NAMES',

    # OS and system-specific names
    'kernel32', 'IsDebuggerPresent', 'ctypes', 'windll', 'platform', 'psutil', 'resource',

    # Commonly used variable names
    'data', 'info', 'config', 'settings', 'params', 'args', 'kwargs', 'result', 'response', 'request', 'session',
    'user', 'admin', 'password', 'username', 'email', 'address', 'phone', 'token', 'secret', 'key', 'value',
    'items', 'values', 'keys', 'file', 'path', 'filename', 'filepath', 'url', 'endpoint', 'method', 'headers',
    'content', 'text', 'html', 'json_data', 'xml_data', 'csv_data', 'table', 'row', 'column', 'cell', 'index',
    'id', 'uuid', 'timestamp', 'datetime', 'date', 'time', 'year', 'month', 'day', 'hour', 'minute', 'second',

    # Web-related names
    'flask', 'django', 'bottle', 'request', 'response', 'url_for', 'redirect', 'session', 'render_template',
    'get', 'post', 'put', 'delete', 'urlencode', 'urldecode', 'parse_qs', 'parse_qsl', 'quote', 'unquote',
    'parse', 'urlparse', 'urlunparse', 'urljoin', 'httplib', 'httpclient', 'wsgi', 'cgi', 'websocket',

    # Other specific exclusions
    'numpy', 'pandas', 'scipy', 'matplotlib', 'seaborn', 'sklearn', 'tensorflow', 'keras', 'torch', 'torchvision',
    'PIL', 'Image', 'cv2', 'dlib', 'face_recognition',

    # PyQt5 specific methods
    'setStyleSheet', 'show', 'hide', 'close', 'resize', 'move', 'setFixedSize', 'setFont', 'setText', 'setReadOnly',
    'setWindowTitle', 'showMinimized', 'showMaximized', 'showNormal', 'clicked', 'stateChanged', 'setAttribute',
    'setContentsMargins', 'setSpacing', 'addWidget', 'addStretch', 'addSpacerItem', 'setLayout', 'update', 'repaint',
    'append', 'addItem', 'clear', 'setIcon', 'setPen', 'drawText', 'setGeometry'
}
