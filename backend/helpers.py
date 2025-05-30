import subprocess
from pathlib import Path
from pydub import AudioSegment
import speech_recognition as sr
from langdetect import detect, LangDetectException
import torch, torchaudio, soundfile as sf
from speechbrain.pretrained.interfaces import foreign_class
import os

os.environ["HF_HUB_DISABLE_SYMLINKS_WINDOWS"] = "1"   # avoid symlink on Win

def extract_audio_from_url(url, output_wav):
    output_path = Path(output_wav)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        result = subprocess.run([
            "yt-dlp",
            "-x",
            "--audio-format", "wav",
            "-o", output_wav,
            url
        ], check=True, capture_output=True, text=True)
        print(f"Audio extracted: {output_wav}")
    except Exception as e:
        print(f"Failed to extract audio: {e}")


def trim_to_60s(src_audio: str | Path, out_path: str | Path) -> Path:
    audio = AudioSegment.from_file(src_audio)
    audio[:60_000].export(out_path, format="wav")   


def transcribe_google_wav(wav_path: Path) -> str:
    r = sr.Recognizer()
    with sr.AudioFile(str(wav_path)) as source:
        audio = r.record(source)        
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        raise RuntimeError(f"Google Web Speech request failed: {e}")
    

def transcribe_and_detect(in_audio: str | Path, trimmed_audio: str | Path):
    trim_to_60s(in_audio, trimmed_audio)
    transcript = transcribe_google_wav(trimmed_audio)
    if not transcript:
        raise RuntimeError("Speech could not be transcribed — unclear or silent audio.")
    
    try:
        lang_code = detect(transcript)
    except LangDetectException:
        lang_code = "und"               

    print("— TRANSCRIPT —")
    print(transcript)
    print("\nDetected language code:", lang_code)
    return lang_code

def load_accent_classifier(device="cpu"):
    return foreign_class(
        source="Jzuluaga/accent-id-commonaccent_xlsr-en-english",
        pymodule_file="custom_interface.py",
        classname="CustomEncoderWav2vec2Classifier",
        run_opts={"device": device},
    )



def classify_accent(classifier, wav_path):
    # absolute path with forward slashes avoids torchaudio URI quirk
    wav_path = Path(wav_path).resolve()
    if not wav_path.is_file():
        raise FileNotFoundError(wav_path)

    out_prob, top_score, top_idx, top_label = classifier.classify_file(wav_path.as_posix())

    probs = out_prob.squeeze(0)      
    labels = classifier.hparams.label_encoder.decode_torch(
        torch.arange(probs.shape[-1])
    )

    return sorted(
        [(lab, float(prob) * 100) for lab, prob in zip(labels, probs)],
        key=lambda x: x[1],
        reverse=True
    )


def remove_audio_files(full, trimmed):
    os.remove(full)
    os.remove(trimmed)