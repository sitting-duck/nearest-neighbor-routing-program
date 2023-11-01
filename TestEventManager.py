from PackageEvent import *
from MatrixUtils import *
from TestPackageManager import TestPackageManager
class TestEventManager:

    def __init__(self, event_manager, package_manager):
        """
        Checks an event manager that it has a correct number of events and that each package is picked up and delivered
        exactly one time.
        :param event_manager: An event manager that holds an array of events to test. All events are of type PackageEvent.    
        """
        self.event_manager = event_manager
        self.package_manager = package_manager

        self.test_every_package_picked_up_one_time()
    def test_every_package_picked_up_one_time(self):
        packages = self.package_manager.get_all_packages()
        events = self.event_manager.get_all_events()

        num_packages = len(packages)

        for package in packages:
            num_pickups = 0
            for event in events:
                if package.id_unique == event.package_id and package.event_type == PackageEventType.pickup:
                    num_pickups += 1
            if num_pickups != 1:
                print("Test Failure: A package should only be picked up once.")


        pickups = []
        deliveries = []
        for event in events:
            if event.event_type == PackageEventType.pickup:
                pickups.append(event)
            elif event.event_type == PackageEventType.delivery:
                deliveries.append(event)
            else:
                print("Error while testing: Unknown event type")

        num_pickups = len(pickups)
        num_deliveries = len(deliveries)
        if num_pickups != num_deliveries:
            print(f"Error: num pickups should equal num deliveries. Pickups: {num_pickups} Deliveries: {num_deliveries}")
        else:
            print(f"Test Success: num pickups equals num deliveries")

