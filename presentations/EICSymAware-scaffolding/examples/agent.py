import uuid
from typing import Callable

from testsimaware.mpi import Perception
from testsimaware.sisw import SituationAwareness, SystemStatus


class Agent:
    """
    Agent class.
    It combines all testsimaware modules together by creating and adding the
    desired callbacks.

    Attributes
    ----------
    _id:
        unique identifier of the agent. Can be provided by the user or
        automatically generated using uuid4.
    _running:
        whether the agent is running or not.
    _perception:
        Perception module.
    _situation_awareness:
        SituationAwareness module.
    """

    def __init__(self, agent_id: "uuid.UUID | None" = None):
        self._id = uuid.uuid4() if agent_id is None else agent_id
        self._running = False
        self._perception = Perception()
        self._situation_awareness = SituationAwareness()
        self._add_callbacks()

    def _on_low_status_value_callback(
        self, event: str
    ) -> Callable[[SystemStatus], None]:
        """
        Create a callback function to be called when any of the system status values is
        low, meaning the resource is going to be depleted soon.

        Parameters
        ----------
        event:
            identifier of the event that triggered the callback.
        """

        def callback(_: SystemStatus):
            print(
                f"Agent {self._id}:\tDetected event {event}. To prevent problems, the agent will stop."
            )
            self.stop()

        return callback

    def _add_callbacks(self):
        """
        Add callbacks to the Perception module.
        """
        self._perception.add("system_status", print)
        self._perception.add("system_status", self._situation_awareness.update)
        self._situation_awareness.add(
            "low_cpu", self._on_low_status_value_callback("low_cpu")
        )
        self._situation_awareness.add(
            "low_memory", self._on_low_status_value_callback("low_memory")
        )
        self._situation_awareness.add(
            "low_disk", self._on_low_status_value_callback("low_disk")
        )

    def start(self):
        """
        Start the agent.
        """
        self._running = True
        self._perception.start()

    def stop(self):
        """
        Stop the agent.
        """
        self._perception.stop()
        self._running = False

    @property
    def id(self) -> uuid.UUID:
        """
        Return the agent's id.

        Returns
        -------
        agent's id
        """
        return self._id

    @property
    def running(self) -> bool:
        """
        Return whether the agent is running or not.

        Returns
        -------
        whether the agent is running or not
        """
        return self._running

    def __repr__(self):
        return f"Agent {self._id}"

    def __eq__(self, other: "Agent"):
        return self._id == other._id

    def __hash__(self):
        return hash(self._id)


def main():
    agent = Agent()
    agent.start()


if __name__ == "__main__":
    main()
