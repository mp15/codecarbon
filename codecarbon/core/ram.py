import abc
from typing import Dict, Tuple

try:
    from codecarbon.core.perf import Perf
except ImportError:
    Perf = None
from codecarbon.core.units import Time
from codecarbon.external.logger import logger


def is_perf_ram_available():
    try:
        if Perf is not None:
            Perf(["energy-ram"])
            return True
        else:
            return False
    except Exception as e:
        logger.debug(
            "Not using the Perf interface, an exception occurred while instantiating "
            + f"Perf : {e}",
        )
        return False

class BaseRAMHardwareMeasurement(abc.ABC):
    @abc.abstractmethod
    def start(self) -> None:
        pass

    @abc.abstractmethod
    def get_ram_details(self, **kwargs) -> Dict:
        pass

class PerfRAMWrapper(BaseRAMHardwareMeasurement):
    def __init__(self) -> None:
        self._perfinterface = Perf(["energy-ram"])

    def start(self):
        self._perfinterface.start()

    def stop(self):
        self._perfinterface.stop()

    def get_energy(self,  duration: Time) -> Dict:
        """
        Return CPU details without computing them.
        """
        logger.debug(f"get_energy {self.cpu_details}")

        return self._perfinterface.delta(
            duration.seconds
        )

