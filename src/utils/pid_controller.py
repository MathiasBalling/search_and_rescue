class PIDController:
    def __init__(
        self,
        kp: float,
        ki: float,
        kd: float,
        output_limits=(None, None),
        setpoint=0.0,
    ):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.output_limits = output_limits

        self._last_error = 0.0
        self._integral = 0.0
        self._last_time = None

    def reset(self):
        self._last_error = 0.0
        self._integral = 0.0
        self._last_time = None

    def compute(self, measured_value: float, current_time: float) -> float:
        error = self.setpoint - measured_value
        delta_time = 0.0
        if self._last_time is not None:
            delta_time = current_time - self._last_time

        # Proportional term
        p = self.kp * error

        # Integral term
        if delta_time > 0:
            self._integral += error * delta_time
        i = self.ki * self._integral

        # Derivative term
        d = 0.0
        if delta_time > 0:
            d = self.kd * (error - self._last_error) / delta_time

        # Save for next iteration
        self._last_error = error
        self._last_time = current_time

        output = p + i + d

        # Apply output limits
        low, high = self.output_limits
        if low is not None:
            output = max(low, output)
        if high is not None:
            output = min(high, output)

        return output
