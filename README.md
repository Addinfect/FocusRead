# SuperFastReader – RSVP Reader

A Python application with Tkinter that implements Rapid Serial Visual Presentation (RSVP) reading, displaying words one by one with a highlighted fixation character to reduce eye movement and increase reading speed.

## Features

- **Two-window architecture**: Main window for text input and settings, separate reader window for distraction-free reading.
- **Fixation point highlighting**: One character per word is positioned at the screen center and highlighted in red. The fixation point remains fixed, eliminating eye movement.
- **Adjustable speed**: Range 60–1200 words per minute (wpm), default 250 wpm (optimal comprehension).
- **Real-time speed control**: Up/Down arrow keys adjust speed by ±10 wpm.
- **Keyboard navigation**:
  - **SPACE**: Pause/resume playback
  - **LEFT/RIGHT**: Move to previous/next word (pauses playback)
  - **UP/DOWN**: Increase/decrease reading speed
- **Font scaling**: Text automatically resizes when window is resized.
- **Progress display**: Shows current word index and total word count.
- **Loop mode**: Option to restart from beginning after finishing the text.
- **Comprehension warning**: Visual cue when speed exceeds 400 wpm (where comprehension may drop).
- **Dark theme**: Black background with white text and red fixation character.

## Installation

SuperFastReader requires Python 3.6+ with Tkinter (usually included with Python).

1. Clone or download this repository.
2. No additional dependencies needed.

## Usage

Run the application:

```bash
python superfastreader.py
```

1. Paste or type your text into the main window.
2. Set desired reading speed (default 250 wpm).
3. Check "Loop" if you want the text to repeat automatically.
4. Click "Start Reading".
5. Use keyboard shortcuts in the reader window to control playback.

## Scientific Background

RSVP reading can significantly increase reading speed by eliminating eye movements. The fixation point (highlighted character) is placed according to word length:

- 1‑letter word: the only character
- 2‑4 letters: second character
- 5+ letters: approximately one‑third into the word (max(1, min(len‑1, int(len×0.33))))

Research suggests optimal comprehension below 300 wpm; a warning appears when speed exceeds 400 wpm.

## Implementation Details

- Built with `tkinter`, using `Canvas` for precise text rendering.
- Font size scales proportionally to window size.
- Timing uses `after()` method for precise word intervals.
- Word tokenization: simple whitespace splitting (punctuation stays attached).

## Testing

Run the unit tests:

```bash
python test_fixation.py
python check_import.py
```

## Packaging

To create a standalone executable with PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed superfastreader.py
```

The executable will be in the `dist/` folder.

## Future Enhancements

- Comprehension check with multiple‑choice questions after reading.
- Support for text files and URLs.
- Custom color schemes.
- Reading statistics (time, estimated comprehension).
- Bookmarking and session saving.

## License

MIT License.