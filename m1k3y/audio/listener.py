import sounddevice as sd
import queue
import logging

logger = logging.getLogger(__name__)

class AudioStream:
    def __init__(self, samplerate=16000, blocksize=8000, channels=1, device=None):
        self.q = queue.Queue()
        self.samplerate = samplerate
        self.blocksize = blocksize
        self.channels = channels
        self.device = device
        self.stream = None

    def _callback(self, indata, frames, time, status):
        if status:
            logger.warning(f"Audio status: {status}")
        self.q.put(bytes(indata))

    def start(self):
        self.stream = sd.RawInputStream(
            samplerate=self.samplerate,
            blocksize=self.blocksize,
            device=self.device,
            dtype="int16",
            channels=self.channels,
            callback=self._callback
        )
        self.stream.start()
        logger.info("AudioStream started")

    def read(self):
        return self.q.get()

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            logger.info("AudioStream stopped")