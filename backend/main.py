import subprocess

def extract_audio_from_url(url, output_wav):
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


extract_audio_from_url("https://www.youtube.com/watch?v=-AOQl94ZYn8&ab_channel=LearnEnglishwithBobtheCanadian", "audio.wav")