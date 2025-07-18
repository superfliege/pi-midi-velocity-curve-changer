#!/usr/bin/env python3
"""
Improved MIDI Velocity Curve Changer
Enhanced version with better performance, error handling, and additional features
"""

import mido
import math
import threading
import argparse
import time
import logging
import signal
import sys
from typing import Optional, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum
import json
import os

# Type hints for mido messages to help the linter
MIDIMessage = Union[mido.Message, Any]

class VelocityCurveType(Enum):
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    BEZIER = "bezier"
    CUSTOM = "custom"

@dataclass
class VelocityCurveConfig:
    curve_type: VelocityCurveType
    exponent: float = 0.6
    sensitivity: float = 1.0
    threshold: int = 0
    custom_points: Optional[list] = None

class MIDIVelocityProcessor:
    def __init__(self, config: VelocityCurveConfig):
        self.config = config
        self.running = False
        self.stats = {
            'messages_processed': 0,
            'velocity_adjustments': 0,
            'start_time': time.time()
        }
        
    def adjust_velocity(self, velocity: int) -> int:
        """Enhanced velocity adjustment with multiple curve types"""
        if velocity <= self.config.threshold:
            return velocity
            
        self.stats['velocity_adjustments'] += 1
        
        if self.config.curve_type == VelocityCurveType.LINEAR:
            return self._linear_adjustment(velocity)
        elif self.config.curve_type == VelocityCurveType.EXPONENTIAL:
            return self._exponential_adjustment(velocity)
        elif self.config.curve_type == VelocityCurveType.BEZIER:
            return self._bezier_adjustment(velocity)
        elif self.config.curve_type == VelocityCurveType.CUSTOM:
            return self._custom_adjustment(velocity)
        
        return velocity
    
    def _linear_adjustment(self, velocity: int) -> int:
        """Linear velocity adjustment"""
        normalized = velocity / 127.0
        adjusted = normalized * self.config.sensitivity
        return max(0, min(127, int(adjusted * 127)))
    
    def _exponential_adjustment(self, velocity: int) -> int:
        """Exponential velocity adjustment"""
        normalized = velocity / 127.0
        adjusted = math.pow(normalized, self.config.exponent)
        return max(0, min(127, int(adjusted * 127)))
    
    def _bezier_adjustment(self, velocity: int) -> int:
        """Quadratic Bezier curve adjustment (original method)"""
        if self.config.exponent < -100 or self.config.exponent > 100:
            raise ValueError("Exponent must be between -100 and 100")
            
        min_midi = 0.0
        max_midi = 127.0
        mid_midi = 63.5
        
        control_point_x = mid_midi + ((self.config.exponent / 100) * mid_midi)
        t = float(velocity) / max_midi
        
        delta = int(round(2 * (1 - t) * t * control_point_x + (t * t * max_midi)))
        result = 2 * velocity - delta
        
        return max(0, min(127, int(result)))
    
    def _custom_adjustment(self, velocity: int) -> int:
        """Custom velocity adjustment using interpolation"""
        if not self.config.custom_points:
            return velocity
            
        # Find the two closest points and interpolate
        for i in range(len(self.config.custom_points) - 1):
            if (self.config.custom_points[i]['input'] <= velocity <= 
                self.config.custom_points[i + 1]['input']):
                
                x1, y1 = self.config.custom_points[i]['input'], self.config.custom_points[i]['output']
                x2, y2 = self.config.custom_points[i + 1]['input'], self.config.custom_points[i + 1]['output']
                
                # Linear interpolation
                ratio = (velocity - x1) / (x2 - x1)
                result = y1 + ratio * (y2 - y1)
                return max(0, min(127, int(result)))
        
        return velocity

class MIDIVelocityChanger:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        # Ensure curve_type is valid
        curve_type_str = config.get('curve_type', 'bezier')
        try:
            curve_type = VelocityCurveType(curve_type_str)
        except ValueError:
            print(f"Warning: Invalid curve_type '{curve_type_str}', using 'bezier'")
            curve_type = VelocityCurveType.BEZIER
            
        self.velocity_processor = MIDIVelocityProcessor(
            VelocityCurveConfig(
                curve_type=curve_type,
                exponent=config.get('midi_exponent', 0.6),
                sensitivity=config.get('sensitivity', 1.0),
                threshold=config.get('threshold', 0),
                custom_points=config.get('custom_points')
            )
        )
        
        self.input_port = None
        self.output_port = None
        self.control_port = None
        self.running = False
        
        # Setup logging
        logging.basicConfig(
            level=logging.DEBUG if config.get('debugmode') else logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Signal handling for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info(f"Received signal {signum}, shutting down...")
        self.stop()
        sys.exit(0)
    
    def find_midi_port(self, search_name: str, port_type: str) -> Optional[str]:
        """Find MIDI port by search name"""
        if not search_name:
            return None
            
        try:
            available_ports = mido.get_input_names() if port_type in ['input', 'control'] else mido.get_output_names()
            
            for port in available_ports:
                if search_name.lower() in port.lower():
                    self.logger.info(f"Found {port_type} port: {port}")
                    return port
            
            self.logger.error(f"No {port_type} port found matching '{search_name}'")
            self.logger.info(f"Available {port_type} ports: {available_ports}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error finding {port_type} port: {e}")
            return None
    
    def setup_ports(self):
        """Setup MIDI ports with error handling"""
        try:
            # Find and open input port
            input_port_name = self.find_midi_port(
                self.config['inputmididevicename'], 
                'input'
            )
            if not input_port_name:
                raise RuntimeError("Input port not found")
            
            try:
                self.input_port = mido.open_input(input_port_name)
                self.logger.info(f"Successfully opened input port: {input_port_name}")
            except Exception as e:
                raise RuntimeError(f"Failed to open input port '{input_port_name}': {e}")
            
            # Find and open output port
            output_port_name = self.find_midi_port(
                self.config['outputmididevicename'], 
                'output'
            )
            if not output_port_name:
                raise RuntimeError("Output port not found")
            
            try:
                self.output_port = mido.open_output(output_port_name)
                self.logger.info(f"Successfully opened output port: {output_port_name}")
            except Exception as e:
                raise RuntimeError(f"Failed to open output port '{output_port_name}': {e}")
            
            # Setup control port if specified
            if self.config.get('inputmididevicenamechannelcontrol'):
                control_port_name = self.find_midi_port(
                    self.config['inputmididevicenamechannelcontrol'],
                    'control'
                )
                if control_port_name:
                    self.control_port = mido.open_input(control_port_name)
                else:
                    self.logger.warning("Control port not found, continuing without channel control")
                    
        except Exception as e:
            self.logger.error(f"Failed to setup MIDI ports: {e}")
            raise
    
    def process_midi_message(self, msg: mido.Message) -> Optional[mido.Message]:  # type: ignore
        """Process a single MIDI message"""
        self.velocity_processor.stats['messages_processed'] += 1
        
        # Create a copy of the message to avoid modifying the original
        try:
            if msg.type == 'note_on':
                processed_msg = mido.Message('note_on', note=msg.note, velocity=msg.velocity, channel=msg.channel, time=msg.time)  # type: ignore
            elif msg.type == 'note_off':
                processed_msg = mido.Message('note_off', note=msg.note, velocity=msg.velocity, channel=msg.channel, time=msg.time)  # type: ignore
            elif msg.type == 'control_change':
                processed_msg = mido.Message('control_change', control=msg.control, value=msg.value, channel=msg.channel, time=msg.time)  # type: ignore
            elif msg.type == 'program_change':
                processed_msg = mido.Message('program_change', program=msg.program, channel=msg.channel, time=msg.time)  # type: ignore
            else:
                # For other message types, return the original message
                return msg
        except Exception as e:
            self.logger.warning(f"Could not copy message {msg.type}: {e}")
            return msg
        
        # Handle velocity adjustment for note messages
        if processed_msg.type in ['note_on', 'note_off'] and processed_msg.velocity > 0:
            original_velocity = processed_msg.velocity
            processed_msg.velocity = self.velocity_processor.adjust_velocity(processed_msg.velocity)
            
            if self.config.get('debugmode'):
                self.logger.debug(f"Velocity adjusted: {original_velocity} -> {processed_msg.velocity}")
        
        # Handle channel changes (only for non-control messages or specific control messages)
        if processed_msg.type != 'control_change':
            processed_msg.channel = self.config.get('channel', 0)
        elif processed_msg.type == 'control_change' and processed_msg.control == 1:
            processed_msg.channel = self.config.get('channel', 0)
        
        # Filter out specific control changes if needed
        if processed_msg.type == "control_change" and processed_msg.control == 65:
            self.logger.debug("Filtering control_change 65")
            return None
        
        return processed_msg
    
    def midi_thread(self):
        """Main MIDI processing thread"""
        self.logger.info("Starting MIDI processing thread")
        
        try:
            if self.input_port:
                for msg in self.input_port:
                    if not self.running:
                        break
                        
                    processed_msg = self.process_midi_message(msg)
                    if processed_msg and self.output_port:
                        self.output_port.send(processed_msg)
                        
        except Exception as e:
            self.logger.error(f"Error in MIDI thread: {e}")
    
    def control_thread(self):
        """Control channel processing thread"""
        if not self.control_port:
            return
            
        self.logger.info("Starting control thread")
        
        try:
            for msg in self.control_port:
                if not self.running:
                    break
                    
                if msg.type == "program_change":
                    self.config['channel'] = msg.program - 1
                    self.logger.info(f"Channel changed to: {self.config['channel']}")
                elif msg.type == "control_change" and msg.control == 65:
                    self.logger.debug("Control_change 65 received in control thread")
                elif self.output_port:
                    # Create a copy of the message for the output
                    try:
                        if msg.type == 'control_change':
                            output_msg = mido.Message('control_change', control=msg.control, value=msg.value, channel=msg.channel, time=msg.time)
                        elif msg.type == 'program_change':
                            output_msg = mido.Message('program_change', program=msg.program, channel=msg.channel, time=msg.time)
                        else:
                            output_msg = msg
                        self.output_port.send(output_msg)
                    except Exception as e:
                        self.logger.warning(f"Could not send control message: {e}")
                    
        except Exception as e:
            self.logger.error(f"Error in control thread: {e}")
    
    def start(self):
        """Start the MIDI velocity changer"""
        self.logger.info("Starting MIDI Velocity Curve Changer")
        
        try:
            self.setup_ports()
            self.running = True
            
            # Start processing threads
            midi_thread = threading.Thread(target=self.midi_thread, daemon=True)
            midi_thread.start()
            
            if self.control_port:
                control_thread = threading.Thread(target=self.control_thread, daemon=True)
                control_thread.start()
            
            # Main loop with statistics
            while self.running:
                time.sleep(5)
                self._print_stats()
                
        except Exception as e:
            self.logger.error(f"Failed to start: {e}")
            self.stop()
            raise
    
    def stop(self):
        """Stop the MIDI velocity changer"""
        self.logger.info("Stopping MIDI Velocity Curve Changer")
        self.running = False
        
        if self.input_port:
            self.input_port.close()
        if self.output_port:
            self.output_port.close()
        if self.control_port:
            self.control_port.close()
    
    def _print_stats(self):
        """Print processing statistics"""
        runtime = time.time() - self.velocity_processor.stats['start_time']
        msg_rate = self.velocity_processor.stats['messages_processed'] / runtime if runtime > 0 else 0
        
        self.logger.info(
            f"Stats: {self.velocity_processor.stats['messages_processed']} messages, "
            f"{self.velocity_processor.stats['velocity_adjustments']} adjustments, "
            f"{msg_rate:.1f} msg/s"
        )

def load_config_from_file(config_file: str) -> Dict[str, Any]:
    """Load configuration from JSON file"""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        print(f"Error parsing config file: {e}")
        return {}

def main():
    parser = argparse.ArgumentParser(description='Enhanced MIDI Velocity Curve Changer')
    parser.add_argument('--inputmididevicename', type=str, default="", 
                       help='Search name for input device')
    parser.add_argument('--outputmididevicename', type=str, default="", 
                       help='Search name for output device')
    parser.add_argument('--inputmididevicenamechannelcontrol', type=str, default="", 
                       help='Search name for input device to change midi channel')
    parser.add_argument('--midi_exponent', type=float, default=0.60, 
                       help='Exponent for velocity adjustment')
    parser.add_argument('--curve_type', type=str, default='bezier', 
                       choices=['linear', 'exponential', 'bezier', 'custom'],
                       help='Type of velocity curve')
    parser.add_argument('--sensitivity', type=float, default=1.0, 
                       help='Sensitivity multiplier')
    parser.add_argument('--threshold', type=int, default=0, 
                       help='Velocity threshold (values below this are not adjusted)')
    parser.add_argument('--debugmode', action='store_true', 
                       help='Enable debug mode for additional output')
    parser.add_argument('--config', type=str, 
                       help='Load configuration from JSON file')
    
    args = parser.parse_args()
    
    # Load config from file if specified
    config = load_config_from_file(args.config) if args.config else {}
    
    # Override with command line arguments (only if they are not empty)
    for key, value in vars(args).items():
        if value is not None and value != "":
            config[key] = value
    
    # Check if required parameters are provided
    if not config.get('inputmididevicename') or not config.get('outputmididevicename'):
        print("\033[91mError: Input and output MIDI device names are required.\033[0m")
        print("Use --config to specify a JSON file or provide --inputmididevicename and --outputmididevicename")
        print("\nExample:")
        print("  python midi.py --config config.json")
        print("  python midi.py --inputmididevicename 'KOMPLETE' --outputmididevicename 'U2MIDI' --midi_exponent -60")
        sys.exit(1)
    
    # List available ports
    print("\033[91mAvailable input ports:\033[0m")
    for port in mido.get_input_names():
        print(f"  {port}")
    
    print("\033[91m\nAvailable output ports:\033[0m")
    for port in mido.get_output_names():
        print(f"  {port}")
    
    # Create and start the MIDI velocity changer
    try:
        changer = MIDIVelocityChanger(config)
        changer.start()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 