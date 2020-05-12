from io import StringIO


class BufferedFileWriter(object):
    def __init__(self, path, buffer_size=65536):
        self.file = open(path, 'w', encoding='utf-8')
        self.buffer = ''
        self.buffer_size = buffer_size

    def flush(self):
        self.file.write(self.buffer)
        self.buffer = ''

    def close(self):
        self.flush()
        self.file.close()

    def write(self, data):
        self.buffer += data
        if len(self.buffer) > self.buffer_size:
            self.flush()


class BufferedFileReader(object):
    def __init__(self, path, buffer_size=65536):
        self.file = open(path, 'w', encoding='utf-8')
        self.buffer = StringIO()
        self.buffer_size = buffer_size

    def close(self):
        self.file.close()

    def readline(self):
        line = self.buffer.readline()
        if not line:
            # Clear memory buffer.
            self.buffer.seek(0)
            self.buffer.truncate(0)

            # Read from file and write to the buffer.
            self.buffer.write(self.file.read(self.buffer_size)
                              + self.file.readline())

            # Move the file pointer to first.
            self.buffer.seek(0)
            line = self.buffer.readline()
        return line
