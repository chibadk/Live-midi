"""
MIDI Sequencer - Handles MIDI file playback and timing
""" 

import mido
from typing import Optional, Callable, List
from pathlib import Path
import time


class MIDISequencer:
    """MIDI file sequencer with play/pause/stop control"""
    
    def __init__(self, midi_handler=None):
        self.midi_handler = midi_handler
        self.current_file: Optional[mido.MidiFile] = None
        self.is_playing = False
        self.is_paused = False
        self.tempo = 1.0  # Tempo multiplier (0.25 - 2.0)
        self.current_time = 0.0
        self.start_time = 0.0
        self.on_position_changed: Optional[Callable] = None
        self.on_song_end: Optional[Callable] = None
    
    def load_file(self, file_path: str) -> bool:
        """Load MIDI file"""
        try:
            self.current_file = mido.MidiFile(file_path)
            self.current_time = 0.0
            return True
        except Exception as e:
            print(f"Error loading MIDI file: {e}")
            return False
    
    def get_file_info(self) -> dict:
        """Get information about loaded file"""
        if not self.current_file:
            return {}
        
        return {
            'filename': self.current_file.filename,
            'ticks_per_beat': self.current_file.ticks_per_beat,
            'duration': self.get_duration(),
            'tracks': len(self.current_file.tracks)
        }
    
    def get_duration(self) -> float:
        """Get total duration in seconds"""
        if not self.current_file:
            return 0.0
        
        total_time = 0.0
        tempo = 500000  # Default tempo: 500000 microseconds per beat
        
        for track in self.current_file.tracks:
            time = 0.0
            for msg in track:
                time += msg.time
                if msg.type == 'set_tempo':
                    tempo = msg.tempo
            
            total_time = max(total_time, time)
        
        # Convert from ticks to seconds
        return (total_time * tempo) / (self.current_file.ticks_per_beat * 1_000_000)
    
    def play(self) -> bool:
        """Start playback"""
        if not self.current_file:
            return False
        
        self.is_playing = True
        self.is_paused = False
        self.start_time = time.time() - self.current_time
        return True
    
    def pause(self) -> bool:
        """Pause playback"""
        if not self.is_playing:
            return False
        
        self.is_paused = True
        self.is_playing = False
        return True
    
    def resume(self) -> bool:
        """Resume from pause"""
        if not self.is_paused:
            return False
        
        self.is_paused = False
        self.is_playing = True
        self.start_time = time.time() - self.current_time
        return True
    
    def stop(self) -> bool:
        """Stop playback and reset position"""
        self.is_playing = False
        self.is_paused = False
        self.current_time = 0.0
        
        # Send all notes off
        if self.midi_handler:
            for channel in range(16):
                self.midi_handler.send_cc(channel, 123, 0)  # All Notes Off
        
        if self.on_position_changed:
            self.on_position_changed(0.0)
        
        return True
    
    def set_tempo(self, tempo: float):
        """Set tempo multiplier (0.25 - 2.0)"""
        self.tempo = max(0.25, min(2.0, tempo))
    
    def seek(self, position: float):
        """Seek to position in seconds"""
        duration = self.get_duration()
        self.current_time = max(0.0, min(position, duration))
        self.start_time = time.time() - self.current_time
    
    def update(self) -> bool:
        """Update playback position (call regularly)"""
        if not self.is_playing:
            return False
        
        elapsed = time.time() - self.start_time
        self.current_time = elapsed / self.tempo
        duration = self.get_duration()
        
        if self.current_time >= duration:
            self.stop()
            if self.on_song_end:
                self.on_song_end()
            return False
        
        if self.on_position_changed:
            self.on_position_changed(self.current_time)
        
        return True
    
    def get_lyrics_at_time(self, time_seconds: float) -> str:
        """Extract lyrics at specific time (if available)"""
        if not self.current_file:
            return ""
        
        # Parse text meta events from MIDI file
        for track in self.current_file.tracks:
            current_time = 0.0
            tempo = 500000
            
            for msg in track:
                current_time += (msg.time * tempo) / (self.current_file.ticks_per_beat * 1_000_000)
                
                if msg.type == 'set_tempo':
                    tempo = msg.tempo
                elif msg.type == 'text' and abs(current_time - time_seconds) < 0.5:
                    return msg.text
        
        return ""