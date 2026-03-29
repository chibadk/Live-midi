"""
MIDI Handler - Real-time MIDI I/O using python-rtmidi
"""

import rtmidi
from typing import List, Optional, Callable


class MIDIHandler:
    """Manages MIDI input/output with real-time hardware communication"""
    
    def __init__(self):
        self.midi_out = rtmidi.MidiOut()
        self.midi_in = rtmidi.MidiIn()
        self.current_output_port = None
        self.current_input_port = None
        self.input_callback: Optional[Callable] = None
    
    def get_output_ports(self) -> List[str]:
        """Get list of available MIDI output ports"""
        return self.midi_out.get_ports() or ["Virtual Output"]
    
    def get_input_ports(self) -> List[str]:
        """Get list of available MIDI input ports"""
        return self.midi_in.get_ports() or ["Virtual Input"]
    
    def open_output(self, port_index: int = 0) -> bool:
        """Open MIDI output port"""
        try:
            if self.current_output_port is not None:
                self.midi_out.close_port()
            
            ports = self.midi_out.get_ports()
            if ports:
                self.midi_out.open_port(port_index)
            else:
                self.midi_out.open_virtual_port("MIDI Maestro Live Output")
            
            self.current_output_port = port_index
            return True
        except Exception as e:
            print(f"Error opening MIDI output: {e}")
            return False
    
    def open_input(self, port_index: int = 0) -> bool:
        """Open MIDI input port"""
        try:
            if self.current_input_port is not None:
                self.midi_in.close_port()
            
            ports = self.midi_in.get_ports()
            if ports:
                self.midi_in.open_port(port_index)
            else:
                self.midi_in.open_virtual_port("MIDI Maestro Live Input")
            
            self.current_input_port = port_index
            return True
        except Exception as e:
            print(f"Error opening MIDI input: {e}")
            return False
    
    def send_message(self, message: List[int]) -> bool:
        """Send MIDI message to output port"""
        try:
            self.midi_out.send_message(message)
            return True
        except Exception as e:
            print(f"Error sending MIDI message: {e}")
            return False
    
    def send_note_on(self, channel: int, note: int, velocity: int = 100) -> bool:
        """Send Note On message (0x90 + channel)"""
        message = [0x90 + (channel & 0x0F), note & 0x7F, velocity & 0x7F]
        return self.send_message(message)
    
    def send_note_off(self, channel: int, note: int, velocity: int = 0) -> bool:
        """Send Note Off message (0x80 + channel)"""
        message = [0x80 + (channel & 0x0F), note & 0x7F, velocity & 0x7F]
        return self.send_message(message)
    
    def send_cc(self, channel: int, controller: int, value: int) -> bool:
        """Send Control Change message (0xB0 + channel)"""
        message = [0xB0 + (channel & 0x0F), controller & 0x7F, value & 0x7F]
        return self.send_message(message)
    
    def send_program_change(self, channel: int, program: int) -> bool:
        """Send Program Change message (0xC0 + channel)"""
        message = [0xC0 + (channel & 0x0F), program & 0x7F]
        return self.send_message(message)
    
    def send_sysex(self, data: List[int]) -> bool:
        """Send System Exclusive message"""
        message = [0xF0] + data + [0xF7]
        return self.send_message(message)
    
    def close(self):
        """Close MIDI ports"""
        self.midi_out.close_port()
        self.midi_in.close_port()
