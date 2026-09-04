import argparse
import sys
import os

# Ensure clean imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.pipeline import TraceChainPipeline

class OutputLogger:
    """Duplicates terminal output to a log file in real-time."""
    def __init__(self, filepath):
        self.terminal = sys.stdout
        # Use utf-8 to ensure emojis like 🕵️ and 🟢 save correctly
        self.log = open(filepath, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush() # Force write to file immediately

    def flush(self):
        self.terminal.flush()
        self.log.flush()
        
    def close(self):
        self.log.close()

def main():
    parser = argparse.ArgumentParser(
        description="TraceChain: AI & Blockchain Social Media Verification"
    )
    
    parser.add_argument(
        "image_path", 
        type=str, 
        help="Path to the image you want to verify"
    )

    args = parser.parse_args()

    if not os.path.exists(args.image_path):
        print(f"❌ Error: Image not found at '{args.image_path}'")
        sys.exit(1)

    # 1. Prepare the output directory and filename
    os.makedirs("output", exist_ok=True)
    
    # Extract just the filename without the extension (e.g., 'data/input/test.webp' -> 'test')
    base_filename = os.path.basename(args.image_path)
    image_name, _ = os.path.splitext(base_filename)
    
    log_filepath = os.path.join("output", f"run_{image_name}.txt")

    # 2. Hijack the standard output to log to both terminal and file
    logger = OutputLogger(log_filepath)
    sys.stdout = logger

    try:
        pipeline = TraceChainPipeline()
        pipeline.process_image(args.image_path)
    except Exception as e:
        print(f"\n❌ PIPELINE ERROR: {e}")
    finally:
        # 3. Safely restore the original terminal output when finished
        sys.stdout = logger.terminal
        logger.close()
        print(f"\n📁 Session log saved to: {log_filepath}")

if __name__ == "__main__":
    main()