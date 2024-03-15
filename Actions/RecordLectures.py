import pyaudio
import logging
import wave


def record_lectures(file_name: str) -> None:
    print("Function needs to be implemented")
    logging.info("Started Recording lecture")
    
    # Shamelessly copied from stackoverflow, src: https://stackoverflow.com/questions/10733903/pyaudio-input-overflowed
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    WAVE_OUTPUT_FILENAME = file_name

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, 
                    channels=CHANNELS, 
                    rate=RATE, 
                    input=True, 
                    frames_per_buffer=CHUNK)

    try:
        logging.info("Recording")
        frames = []
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        p.terminate()
        logging.info("Recording stopped")


    with wave.open("RecordedLectures/"+WAVE_OUTPUT_FILENAME, 'wb') as file:
        file.setnchannels(CHANNELS)
        file.setframerate(RATE)
        file.setsampwidth(p.get_sample_size(FORMAT))
        file.writeframes(b''.join(frames))    
        logging.info("Recording saved")

    # Open a database connection
    # store the file in database
    # Close database connection


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET)
    record_lectures("output.wav")
