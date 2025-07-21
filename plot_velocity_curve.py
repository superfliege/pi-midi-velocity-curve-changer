import json
import matplotlib.pyplot as plt
import math
from enum import Enum
from dataclasses import dataclass
from typing import Optional, List

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
    custom_points: Optional[List[dict]] = None

class MIDIVelocityProcessor:
    def __init__(self, config: VelocityCurveConfig):
        self.config = config

    def adjust_velocity(self, velocity: int) -> int:
        if velocity <= self.config.threshold:
            return velocity
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
        normalized = velocity / 127.0
        adjusted = normalized * self.config.sensitivity
        return max(0, min(127, int(adjusted * 127)))

    def _exponential_adjustment(self, velocity: int) -> int:
        normalized = velocity / 127.0
        adjusted = math.pow(normalized, self.config.exponent)
        return max(0, min(127, int(adjusted * 127)))

    def _bezier_adjustment(self, velocity: int) -> int:
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
        if not self.config.custom_points:
            return velocity
        for i in range(len(self.config.custom_points) - 1):
            if (self.config.custom_points[i]['input'] <= velocity <= 
                self.config.custom_points[i + 1]['input']):
                x1, y1 = self.config.custom_points[i]['input'], self.config.custom_points[i]['output']
                x2, y2 = self.config.custom_points[i + 1]['input'], self.config.custom_points[i + 1]['output']
                ratio = (velocity - x1) / (x2 - x1)
                result = y1 + ratio * (y2 - y1)
                return max(0, min(127, int(result)))
        return velocity

def plot_velocity_curve(config_path="config.json"):
    with open(config_path, 'r') as f:
        config = json.load(f)
    curve_type_str = config.get('curve_type', 'bezier')
    try:
        curve_type = VelocityCurveType(curve_type_str)
    except ValueError:
        curve_type = VelocityCurveType.BEZIER
    processor = MIDIVelocityProcessor(
        VelocityCurveConfig(
            curve_type=curve_type,
            exponent=config.get('midi_exponent', 0.6),
            sensitivity=config.get('sensitivity', 1.0),
            threshold=config.get('threshold', 0),
            custom_points=config.get('custom_points')
        )
    )
    input_velocities = list(range(128))
    output_velocities = [processor.adjust_velocity(v) for v in input_velocities]
    plt.figure(figsize=(8, 5))
    plt.plot(input_velocities, output_velocities, label=f"{curve_type.value} curve")
    plt.plot(input_velocities, input_velocities, '--', color='gray', label='Linear (reference)')
    plt.xlabel('Input Velocity')
    plt.ylabel('Output Velocity')
    plt.title('MIDI Velocity Curve')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_velocity_curve("config.json") 