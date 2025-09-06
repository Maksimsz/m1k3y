import json
import logging
from vosk import Model, KaldiRecognizer

logger = logging.getLogger(__name__)

class Transcriber:
    def __init__(self, model_path: str = "vosk-model-small-en-us-0.15", rate=16000):
        # Expect user to download model manually if not present
        self.model = Model(model_path)
        self.rec = KaldiRecognizer(self.model, rate)

    def accept_audio(self, data: bytes):
        if self.rec.AcceptWaveform(data):
            result = self.rec.Result()
            try:
                return json.loads(result).get("text", "")
            except:
                return ""
        else:
            partial = self.rec.PartialResult()
            try:
                return json.loads(partial).get("partial", "")
            except:
                return ""