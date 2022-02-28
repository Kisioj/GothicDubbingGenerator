# import librosa
import glob
import soundfile as sf

wav_paths = glob.glob("output/*.WAV")
# for wav_path in wav_paths[:10]:
#     f = sf.SoundFile(wav_path)
#     print(f'{wav_path} samples={f.frames} samplerate={f.samplerate} seconds={f.frames/f.samplerate}')
# print(len(wav_paths))

seconds = 0
for wav_path in wav_paths:
    f = sf.SoundFile(wav_path)
    seconds += f.frames/f.samplerate


print(f'seconds: {seconds}')
print(f'minutes: {seconds/60}')
print(f'hours: {seconds/60/60}')

