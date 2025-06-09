# =============================================================================
# Thinking Spinner - ASCII Animation Utility
# =============================================================================
# Provides a visual indication that the AI is processing a request.
# This spinner runs in a separate thread to avoid blocking the main execution.
# =============================================================================

import threading
import time
import sys


class ThinkingSpinner:
    """ASCII spinner animation for showing AI processing status"""
    
    def __init__(self):
        self.spinning = False
        self.spinner_thread = None
        # Different spinner styles - using a brain/thinking theme
        self.frames = [
            "🧠 Thinking    ",
            "🧠 Thinking.   ",
            "🧠 Thinking..  ",
            "🧠 Thinking... ",
            "🧠 Thinking....",
            "🧠 Thinking... ",
            "🧠 Thinking..  ",
            "🧠 Thinking.   "
        ]
        self.current_frame = 0
    
    def _spin(self):
        """Internal method to display the spinner animation"""
        while self.spinning:
            # Clear the current line and print the spinner frame
            sys.stdout.write(f"\r{self.frames[self.current_frame]}")
            sys.stdout.flush()
            
            # Move to next frame
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            time.sleep(0.15)  # Animation speed
    
    def start(self):
        """Start the thinking animation"""
        if not self.spinning:
            self.spinning = True
            self.spinner_thread = threading.Thread(target=self._spin, daemon=True)
            self.spinner_thread.start()
    
    def stop(self):
        """Stop the thinking animation and clear the line"""
        if self.spinning:
            self.spinning = False
            if self.spinner_thread:
                self.spinner_thread.join(timeout=0.2)
            # Clear the spinner line
            sys.stdout.write("\r" + " " * 20 + "\r")
            sys.stdout.flush() 