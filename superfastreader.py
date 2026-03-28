"""
SuperFastReader – RSVP (Rapid Serial Visual Presentation) reader
Scientifically informed reading tool with fixation point highlighting.
"""

import tkinter as tk
from tkinter import font, ttk, messagebox
import math


class SuperFastReader:
    """Main application with text input and settings."""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SuperFastReader")
        self.root.geometry("800x600")
        
        # Variables
        self.reader = None
        
        self.setup_main()
        
    def setup_main(self):
        """Create main window widgets."""
        # Frame for better organization
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title label
        title_label = ttk.Label(main_frame, text="SuperFastReader", font=("Helvetica", 24, "bold"))
        title_label.pack(pady=(0, 20))
        settings_frame = ttk.Frame(main_frame)
        settings_frame.pack(fill=tk.X, pady=(0, 20))
        # Instructions
        instructions = (
            "Instructions:\n"
            "• Paste text in the box below and click 'Start Reading'\n"
            "• In the reader window:\n"
            "  - SPACE: Pause/Resume\n"
            "  - LEFT/RIGHT: Previous/Next word\n"
            "  - UP/DOWN: Increase/Decrease speed by 10 wpm\n"
            "• Close reader window to return to editor"
        )
        instructions_label = ttk.Label(main_frame, text=instructions, justify=tk.LEFT)
        instructions_label.pack(anchor=tk.W, pady=(0, 20))
        
        # Text input label
        text_label = ttk.Label(main_frame, text="Paste your text below:")
        text_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Text input widget with scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.text_input = tk.Text(text_frame, wrap=tk.WORD, font=("Helvetica", 12))
        text_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_input.yview)
        self.text_input.configure(yscrollcommand=text_scrollbar.set)
        
        self.text_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Speed control
        speed_label = ttk.Label(settings_frame, text="Reading Speed (wpm):")
        speed_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.speed_var = tk.IntVar(value=250)  # Default speed
        speed_spinbox = ttk.Spinbox(
            settings_frame,
            from_=60,
            to=1200,
            increment=10,
            textvariable=self.speed_var,
            width=8
        )
        speed_spinbox.pack(side=tk.LEFT, padx=(0, 20))
        
        # Info label about optimal comprehension
        info_label = ttk.Label(
            settings_frame,
            text="Research suggests optimal comprehension below 300 wpm",
            font=("Helvetica", 9, "italic")
        )
        info_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Loop checkbox
        self.loop_var = tk.BooleanVar(value=False)
        loop_check = ttk.Checkbutton(
            settings_frame,
            text="Loop",
            variable=self.loop_var
        )
        loop_check.pack(side=tk.LEFT, padx=(0, 20))
        
        # Play button
        play_button = ttk.Button(main_frame, text="Start Reading", command=self.start_reading)
        play_button.pack(pady=(0, 10))
        

        
    def start_reading(self):
        """Create reader window with current text and speed."""
        # Get text and split into words
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("No Text", "Please enter some text to read.")
            return
        
        words = text.split()
        speed = self.speed_var.get()
        
        # Close existing reader window if open
        if self.reader and self.reader.window and self.reader.window.winfo_exists():
            self.reader.window.destroy()
        
        # Create new reader window
        self.reader = ReaderWindow(self.root, words, speed, loop=self.loop_var.get())
        
    def run(self):
        """Start the main event loop."""
        self.root.mainloop()


class ReaderWindow:
    """Window that displays words using RSVP with fixation point."""
    def __init__(self, parent, words, speed, loop=False):
        self.parent = parent
        self.words = words
        self.current_index = 0
        self.speed = speed  # words per minute
        self.loop = loop
        self.is_playing = True
        self.after_id = None
        
        # Font for rendering words
        self.font = font.Font(family="Helvetica", size=20)
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title(f"SuperFastReader - {len(self.words)} words")
        self.window.configure(bg="black")
        
        # Canvas for drawing text
        self.canvas = tk.Canvas(self.window, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Speed display label (semi-transparent)
        self.speed_label = tk.Label(
            self.window,
            text=f"{self.speed} wpm",
            font=("Helvetica", 12),
            bg="black",
            fg="gray",
            relief=tk.FLAT
        )
        self.speed_label.place(relx=1.0, rely=0.0, anchor=tk.NE, x=-10, y=10)
        
        # Progress display
        self.progress_label = tk.Label(
            self.window,
            text=f"0/{len(self.words)}",
            font=("Helvetica", 10),
            bg="black",
            fg="gray",
            relief=tk.FLAT
        )
        self.progress_label.place(relx=0.0, rely=1.0, anchor=tk.SW, x=10, y=-10)
        
        # Pause indicator (hidden initially)
        self.pause_label = tk.Label(
            self.window,
            text="PAUSED",
            font=("Helvetica", 16, "bold"),
            bg="black",
            fg="yellow",
            relief=tk.FLAT
        )
        self.pause_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        self.pause_label.place_forget()
        
        # Comprehension warning (shown when speed > 400 wpm)
        self.warning_label = tk.Label(
            self.window,
            text="⚠ Comprehension may drop above 400 wpm",
            font=("Helvetica", 10, "italic"),
            bg="black",
            fg="orange",
            relief=tk.FLAT
        )
        if self.speed > 400:
            self.warning_label.place(relx=0.5, rely=0.95, anchor=tk.CENTER)
        else:
            self.warning_label.place_forget()
        
        # Bind events
        self.bind_events()
        
        # Initial display
        self.window.update_idletasks()  # Ensure geometry is computed
        self.update_font_size()         # Set font based on actual window size
        self.update_display()
        self.schedule_next()
        
        # Handle window closing
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def bind_events(self):
        """Bind keyboard and resize events."""
        self.window.bind("<KeyPress>", self.on_key_press)
        self.window.bind("<Configure>", self.on_resize)
        # Focus the window for keyboard input
        self.window.focus_set()
        
    def on_key_press(self, event):
        """Handle keyboard shortcuts."""
        key = event.keysym
        if key == "space":
            self.toggle_play()
        elif key == "Left":
            self.prev_word()
        elif key == "Right":
            self.next_word()
        elif key == "Up":
            self.increase_speed()
        elif key == "Down":
            self.decrease_speed()
        elif key == "Home":
            self.go_to_first_word()
        elif key == "End":
            self.go_to_last_word()
        # Return "break" to prevent default handling
        return "break"
    
    def toggle_play(self):
        """Pause or resume playback."""
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.pause_label.place_forget()
            self.schedule_next()
        else:
            self.pause_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
            self.cancel_schedule()
        self.update_speed_display()
        
    def prev_word(self):
        """Move to previous word."""
        self.cancel_schedule()
        self.current_index = max(0, self.current_index - 1)
        self.update_display()
        self.is_playing = False
        self.pause_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        self.update_speed_display()
        
    def next_word(self):
        """Move to next word."""
        self.cancel_schedule()
        self.current_index = min(len(self.words) - 1, self.current_index + 1)
        self.update_display()
        self.is_playing = False
        self.pause_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        self.update_speed_display()

    def go_to_first_word(self):
        """Jump to the first word."""
        self.cancel_schedule()
        self.current_index = 0
        self.update_display()
        self.is_playing = False
        self.pause_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        self.update_speed_display()

    def go_to_last_word(self):
        """Jump to the last word."""
        self.cancel_schedule()
        self.current_index = len(self.words) - 1
        self.update_display()
        self.is_playing = False
        self.pause_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        self.update_speed_display()

    def increase_speed(self):
        """Increase speed by 10 wpm, clamped to 1200."""
        new_speed = min(1200, self.speed + 10)
        if new_speed != self.speed:
            self.speed = new_speed
            self.update_speed_display()
            # If playing, reschedule with new speed
            if self.is_playing:
                self.cancel_schedule()
                self.schedule_next()
    
    def decrease_speed(self):
        """Decrease speed by 10 wpm, clamped to 60."""
        new_speed = max(60, self.speed - 10)
        if new_speed != self.speed:
            self.speed = new_speed
            self.update_speed_display()
            # If playing, reschedule with new speed
            if self.is_playing:
                self.cancel_schedule()
                self.schedule_next()
    
    def update_speed_display(self):
        """Update speed label and warning."""
        self.speed_label.config(text=f"{self.speed} wpm")
        # Show/hide comprehension warning
        if self.speed > 400:
            self.warning_label.place(relx=0.5, rely=0.95, anchor=tk.CENTER)
        else:
            self.warning_label.place_forget()
    
    def on_resize(self, event):
        """Handle window resize to adjust font size."""
        if event.widget == self.window:
            self.update_font_size()
            self.update_display()
    
    def update_font_size(self):
        """Calculate and set font size based on canvas dimensions."""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # Use a proportion of the smaller dimension
        # Aim for text height ~1/10 of canvas height, but not less than 10pt
        new_size = max(10, int(min(width, height) / 10))
        self.font.configure(size=new_size)
    
    def get_fixation_index(self, word):
        """Compute fixation index according to specification."""
        length = len(word)
        if length == 1:
            return 0
        elif 2 <= length <= 4:
            return 1
        else:  # length >= 5
            # max(1, min(len(word)-1, int(len(word) * 0.5)))
            idx = int(length * 0.5)
            idx = max(1, min(length - 1, idx))
            return idx
    
    def draw_word(self, word):
        """Draw word on canvas with fixation point highlighted."""
        # Clear previous drawings
        self.canvas.delete("all")
        
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Compute fixation index
        fix_idx = self.get_fixation_index(word)
        
        # Split word
        left_part = word[:fix_idx]
        fix_char = word[fix_idx]
        right_part = word[fix_idx + 1:]
        
        # Measure widths
        left_width = self.font.measure(left_part)
        fix_width = self.font.measure(fix_char)
        right_width = self.font.measure(right_part)
        
        # Calculate positions so fixation character is centered
        # Fixation character center should align with canvas center
        x_fix_center = canvas_width / 2
        y_pos = canvas_height / 2 - self.font.metrics("linespace") / 2
        
        # Position fixation character (left edge)
        x_fix = x_fix_center - fix_width / 2
        
        # Draw left part (white)
        if left_part:
            self.canvas.create_text(
                x_fix - left_width, y_pos,
                text=left_part,
                font=self.font,
                fill="white",
                anchor=tk.NW
            )
        
        # Draw fixation character (red)
        if fix_char:
            self.canvas.create_text(
                x_fix, y_pos,
                text=fix_char,
                font=self.font,
                fill="red",
                anchor=tk.NW
            )
        
        # Draw right part (white)
        if right_part:
            self.canvas.create_text(
                x_fix + fix_width, y_pos,
                text=right_part,
                font=self.font,
                fill="white",
                anchor=tk.NW
            )
    
    def update_display(self):
        """Update canvas with current word and progress."""
        if 0 <= self.current_index < len(self.words):
            word = self.words[self.current_index]
            self.draw_word(word)
            
            # Update progress display
            self.progress_label.config(text=f"{self.current_index + 1}/{len(self.words)}")
    
    def schedule_next(self):
        """Schedule next word display."""
        if self.is_playing and (self.current_index < len(self.words) - 1 or self.loop):
            # Convert wpm to milliseconds per word
            delay_ms = int(60000 / self.speed)
            self.after_id = self.window.after(delay_ms, self.display_next_word)
    
    def display_next_word(self):
        """Display next word and schedule again."""
        if self.current_index < len(self.words) - 1:
            self.current_index += 1
            self.update_display()
            self.schedule_next()
        else:
            # Reached end of text
            if self.loop:
                # Loop back to beginning
                self.current_index = 0
                self.update_display()
                self.schedule_next()
            else:
                self.is_playing = False
                self.pause_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
                self.cancel_schedule()
    
    def cancel_schedule(self):
        """Cancel pending after callback."""
        if self.after_id:
            self.window.after_cancel(self.after_id)
            self.after_id = None
    
    def on_close(self):
        """Clean up when window is closed."""
        self.cancel_schedule()
        self.window.destroy()


def main():
    """Entry point."""
    app = SuperFastReader()
    app.run()


if __name__ == "__main__":
    main()