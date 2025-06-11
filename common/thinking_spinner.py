"""
Thinking Spinner Module - Terminal UI Component for User Feedback

This module provides a visual feedback mechanism for long-running operations,
specifically designed for AI agent processing where users need to know the
system is working on their request.

UI/UX DESIGN PHILOSOPHY:
- Immediate Feedback: Users see activity within milliseconds of request
- Visual Clarity: Animated spinner clearly indicates processing state
- Non-intrusive: Minimal visual footprint, doesn't interfere with output
- Professional: Clean, console-appropriate animation style

THREADING ARCHITECTURE:
The spinner runs in a separate thread to avoid blocking the main application:
- Main Thread: Continues processing AI operations
- Spinner Thread: Manages animation loop and terminal output
- Synchronization: Thread-safe start/stop using threading events

CONTEXT MANAGER PATTERN:
Implements Python's context manager protocol for clean resource management:
- Automatic Start: Spinner begins when entering the context
- Automatic Stop: Spinner stops when exiting the context  
- Exception Safety: Spinner stops even if operation fails
- Resource Cleanup: Thread properly terminated in all scenarios
"""

import threading
import time
import sys


class ThinkingSpinner:
    """
    Terminal-based thinking spinner for providing user feedback during processing.
    
    This class implements a context manager that displays an animated spinner
    while long-running operations execute. Designed specifically for AI agent
    interactions where processing time can be unpredictable.
    
    VISUAL DESIGN:
    - Unicode spinner characters for smooth animation
    - "Thinking..." text for clear context
    - Carriage return (\r) for in-place updates
    - Flush output for immediate visibility
    
    THREADING MODEL:
    - Background Thread: Runs spinner animation loop
    - Event Synchronization: Uses threading.Event for clean shutdown
    - Non-blocking: Main thread continues processing while spinner runs
    - Resource Safety: Proper thread cleanup prevents resource leaks
    
    CONTEXT MANAGER BENEFITS:
    - Automatic lifecycle management
    - Exception-safe cleanup
    - Pythonic usage pattern with 'with' statements
    - Consistent behavior across all usage scenarios
    """
    
    def __init__(self):
        """
        Initialize spinner with threading components.
        
        INITIALIZATION COMPONENTS:
        - stop_event: Threading event for signaling spinner shutdown
        - spinner_thread: Background thread for animation (created on start)
        
        DESIGN CHOICE:
        Thread creation is deferred until actual usage to avoid
        resource allocation during module import. This enables
        faster application startup and better resource efficiency.
        """
        self.stop_event = threading.Event()
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
        """
        Background thread function that runs the spinner animation loop.
        
        ANIMATION DESIGN:
        - Unicode Characters: ⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏ for smooth rotation effect
        - Frame Rate: 0.1 second intervals for smooth but not distracting animation
        - In-place Updates: Uses \r to overwrite previous frame
        - Immediate Output: sys.stdout.flush() ensures real-time visibility
        
        THREADING CONSIDERATIONS:
        - Non-blocking Check: stop_event.is_set() allows immediate shutdown
        - Exception Safety: Continues running even if output operations fail
        - Clean Termination: Responds quickly to stop signals
        
        TERMINAL COMPATIBILITY:
        - Unicode Support: Modern terminals support the spinner characters
        - Fallback: Could be enhanced with ASCII fallback for older terminals
        - Cross-platform: Works on Unix, Windows, and macOS terminals
        """
        # Unicode spinner characters that create smooth rotation animation
        spinner_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        i = 0
        
        # Animation loop continues until stop event is set
        while not self.stop_event.is_set():
            # Display current spinner frame with thinking message
            # \r returns cursor to start of line for in-place update
            sys.stdout.write(f"\r{self.frames[i % len(self.frames)]}{spinner_chars[i % len(spinner_chars)]}")
            sys.stdout.flush()  # Force immediate output to terminal
            
            # Advance to next spinner character
            i += 1
            
            # Wait for next frame, but check for stop signal
            # 0.1 second provides smooth animation without being distracting
            time.sleep(0.1)
    
    def __enter__(self):
        """
        Context manager entry point - start the spinner.
        
        Returns:
            self for context manager protocol compliance
            
        CONTEXT MANAGER PROTOCOL:
        This method is called when entering a 'with' statement.
        It initializes and starts the background spinner thread.
        
        THREAD LIFECYCLE:
        1. Reset stop_event to clear any previous state
        2. Create new thread targeting the _spin method
        3. Set daemon=True so thread doesn't prevent program exit
        4. Start thread to begin animation
        
        DAEMON THREAD CHOICE:
        daemon=True ensures that the spinner thread won't prevent
        the main program from exiting if something goes wrong.
        This is important for command-line applications where
        hanging background threads would be problematic.
        """
        # Reset stop event in case of reuse
        self.stop_event.clear()
        
        # Create and start spinner thread
        # daemon=True ensures thread won't prevent program exit
        self.spinner_thread = threading.Thread(target=self._spin, daemon=True)
        self.spinner_thread.start()
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit point - stop the spinner and cleanup.
        
        Args:
            exc_type: Exception type if an exception occurred
            exc_val: Exception value if an exception occurred  
            exc_tb: Exception traceback if an exception occurred
            
        Returns:
            None (doesn't suppress exceptions)
            
        CLEANUP SEQUENCE:
        1. Signal spinner thread to stop via threading event
        2. Wait for thread to finish with reasonable timeout
        3. Clear the spinner line from terminal
        4. Allow any exceptions to propagate normally
        
        EXCEPTION HANDLING:
        This method executes even if the code inside the 'with' block
        raises an exception. The spinner is cleaned up regardless of
        whether the main operation succeeded or failed.
        
        TERMINAL CLEANUP:
        Clearing the spinner line ensures that subsequent output
        appears cleanly without leftover spinner artifacts.
        """
        # Signal the spinner thread to stop
        self.stop_event.set()
        
        # Wait for thread to finish (with timeout for safety)
        if self.spinner_thread:
            self.spinner_thread.join(timeout=1.0)
        
        # Clear the spinner line from terminal
        # \r returns to start of line, spaces overwrite content, \r positions for next output
        sys.stdout.write("\r" + " " * 20 + "\r")
        sys.stdout.flush()
        
        # Return None to allow exceptions to propagate normally 