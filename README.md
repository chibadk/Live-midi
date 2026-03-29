# MIDI Maestro Live

**Professional MIDI Live Player** with 16-channel mixer, fanfare pads, and karaoke display.

Optimized for **Roland SC-88/M-GS64** hardware synthesizers with real-time MIDI control.

---

## 🎯 Features

✅ **16-Channel GS Mixer**
- Vertical volume sliders (0-127)
- VU meters with color transition (Green → Yellow → Red)
- Mute/Solo per channel
- Real-time MIDI CC7 output

✅ **16 Fanfare Pads** (4x4 Grid)
- Load MIDI files to pads
- Trigger playback on demand
- Right-click context menu to clear
- Visual feedback (Green when loaded)

✅ **MIDI File Playback**
- Double-click file browser to load
- Tempo control (0.25x - 2.0x speed)
- Time display (current / total)
- Play / Pause / Stop controls

✅ **Karaoke Display**
- 36px green font on black background
- Real-time lyrics extraction from MIDI text events
- Status messages during playback

✅ **Professional UI**
- 6 dark themes (Dark, Midnight, Forest Green, Red Passion, Brown Wood, Ocean Blue)
- Proportional layout: 30% File Browser | 35% Pads | 25% Karaoke | 40% Mixer
- Clean, responsive design

✅ **Hardware Integration**
- Real-time MIDI I/O with python-rtmidi
- Roland GS System Exclusive (SysEx) commands
- GS Reset button for hardware initialization
- All Notes Off panic function

---

## 📋 System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, macOS, Linux
- **MIDI Hardware**: Roland SC-88, M-GS64, or any GM2-compatible device
- **GUI**: X11 (Linux), native (Windows/macOS)

---

## 🚀 Installation

### 1. Clone the Repository

```
git clone https://github.com/chibadk/Live-midi.git
cd Live-midi
```

### 2. Create Virtual Environment (Recommended)

```
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Create Data Directory

```
mkdir data
# Add your MIDI files here (.mid files)
```

### 5. Run Application

```
python main.py
```

---

## 📖 Usage Guide

### Transport Controls (Top Panel)

```
▶ Play    - Start MIDI playback
⏸ Pause   - Pause (resume from same position)
⏹ Stop    - Stop and reset to beginning
Tempo     - Speed control (0.25x to 2.0x)
Time      - Current / Total duration display
🔄 GS Reset - Send Roland GS Reset to hardware
```

### File Browser (Left Panel, 30%)

- Files from data/ directory appear here
- Double-click to load into sequencer
- Status shows in karaoke display

### Fanfare Pads (Center Panel, 35%)

4x4 Grid (16 Pads):

- Left-Click → Load MIDI file
- Right-Click → Play loaded file
- Context Menu → Clear pad

Visual States:
- Gray = Empty pad
- Green = File loaded
- Yellow = Playing

### Karaoke Display (Right Panel, 25%)

- Shows status messages
- Displays extracted lyrics from MIDI text events
- 36px bold green text on black background
- Real-time sync with playback

### 16-Channel Mixer (Bottom Panel, 40%)

Per Channel (Ch1-Ch16):

- Volume Slider → 0-127 (sends MIDI CC7)
- VU Meter → Visual level indicator (Green → Yellow → Red)
- M Button → Mute channel (sends All Notes Off CC123)
- S Button → Solo channel (mute others)

---

## 🎨 Themes

Six professional dark themes available:

| Theme | Background | Foreground |
|-------|-----------|-----------|
| **Dark** | #1e1e1e | #ffffff |
| **Midnight** | #0a0e27 | #e0e0e0 |
| **Forest Green** | #1b4332 | #d8f3dc |
| **Red Passion** | #3d0000 | #ffcccc |
| **Brown Wood** | #3e2723 | #d7ccc8 |
| **Ocean Blue** | #004e89 | #c7e9ff |

Change theme in `config/settings.json` by updating the "theme" value.

---

## 📁 Project Structure

```
Live-midi/
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
├── README.md                     # This file
│
├── midi_engine/                  # MIDI core modules
│   ├── __init__.py
│   ├── midi_handler.py           # Real-time I/O (python-rtmidi)
│   ├── sequencer.py              # MIDI file playback engine
│   └── gs_commands.py            # Roland GS SysEx commands
│
├── ui/                           # PyQt6 GUI components
│   ├── __init__.py
│   └── main_window.py            # Main window with all layouts
│
├── config/                       # Configuration files (JSON)
│   ├── settings.json             # User preferences & window setup
│   ├── themes.json               # 6 color themes
│   └── roland_sc88.json          # SC-88 instrument database
│
└── data/                         # MIDI files directory
    └── (add your .mid files here)
```

---

## 🔧 Configuration

### config/settings.json

Contains window size, theme selection, and MIDI device settings.

### config/themes.json

Defines 6 color themes with background, foreground, and accent colors.

### config/roland_sc88.json

Contains Roland SC-88 instrument bank with program numbers and names.

---

## 🎹 MIDI Implementation

### Supported MIDI Messages

- **Control Change (CC)**: Volume (CC7), All Notes Off (CC123)
- **Program Change**: Instrument selection per channel
- **System Exclusive (SysEx)**: Roland GS Reset, Bank Select
- **Note On/Off**: Playback control

### Roland GS Commands

The application sends proper Roland GS System Exclusive commands for:
- GS Reset (hardware initialization)
- Bank Select (instrument switching)
- Program Change (sound selection)
- All Notes Off (panic/mute)

---

## 🐛 Troubleshooting

### MIDI Device Not Found

**Error:** MIDI init error: rtmidi.SystemError

**Solution:**
- Ensure hardware is connected and powered on
- Check USB connection
- Try virtual MIDI ports on macOS/Linux
- Install LoopMIDI on Windows for virtual ports

### No Sound Output

**Error:** GS Reset fails silently

**Solution:**
- Click "🔄 GS Reset" button to initialize hardware
- Check MIDI output device selection in settings.json
- Verify hardware is in GS mode (not XG/CM-64)

### File Not Loading

**Error:** File appears in browser but won't load

**Solution:**
- Ensure MIDI file is valid (.mid format)
- Place files in `data/` directory
- Check file permissions
- Try a different MIDI file to test

---

## 📚 Dependencies

- **PyQt6** - GUI framework for the user interface
- **python-rtmidi** - Real-time MIDI input/output communication
- **mido** - MIDI file parsing and processing

See `requirements.txt` for specific versions.

---

## 🔜 Future Enhancements

- [ ] Pad file loading dialog (left-click load, right-click play)
- [ ] Solo mode (mute all other channels)
- [ ] Real-time karaoke sync from MIDI lyrics
- [ ] Hardware mapping (Behringer FCB1010, Akai APC mini)
- [ ] Recording support
- [ ] Preset save/load system
- [ ] Master volume fader
- [ ] Channel strip effects (reverb, chorus)
- [ ] Song setlist manager
- [ ] Network MIDI support

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing](#)
