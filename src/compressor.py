import ffmpeg

def compress_video(input_file: str, output_file: str) -> bool:
    """Compress a video."""
    try:
        stream = ffmpeg.input(input_file)
        stream = ffmpeg.output(
            stream, output_file, vcodec="libx264", crf=28, preset="fast", acodec="aac"
        )
        ffmpeg.run(stream)
        return True
    except Exception as e:
        print(f"Compression failed: {e}")
        return False