import pvporcupine
import struct
import pyaudio

class WakeWordDetector:
    def __init__(self, model_path, access_key):
        self.model_path = model_path
        self.access_key = access_key
        self.audio = pyaudio.PyAudio()
        self.handle = pvporcupine.create(
            access_key=self.access_key,
            keyword_paths=[self.model_path]
        )

    def start_detection(self):
        if self.audio is None or self.handle is None:
            raise Exception("Engine is not initialized. Call the constructor first.")

        try:
            stream = self.audio.open(
                rate=self.handle.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.handle.frame_length
            )

            while True:
                pcm = stream.read(self.handle.frame_length)
                pcm = struct.unpack_from("h" * self.handle.frame_length, pcm)
                keyword_index = self.handle.process(pcm)
                if keyword_index >= 0:
                    return True  # Return True when the wake word is detected

        except KeyboardInterrupt:
            print("Shutting down...")

        finally:
            if stream:
                stream.close()
            if self.audio:
                self.audio.terminate()
            if self.handle:
                self.handle.delete()

        return False  # Return False if the detection loop exits without detecting the wake word
