import heapq
from agents.patient import Patient


class HospitalBedAgent:

    def __init__(self, icu_beds, general_beds):
        self.icu_beds = icu_beds
        self.general_beds = general_beds

        self.waiting_queue = []   # heap queue
        self.allocated = {}       # name -> bed
        self.patients = {}        # name -> Patient object


    def _try_allocate(self, patient: Patient) -> bool:
        """
        Try to allocate a bed to the patient.
        Returns True if allocated, False otherwise.
        """
        if patient.condition == "critical":
            if self.icu_beds > 0:
                self.icu_beds -= 1
                self.allocated[patient.name] = "ICU"
                return True
            elif self.general_beds > 0:
                self.general_beds -= 1
                self.allocated[patient.name] = "General"
                return True
        else:   # serious or normal
            if self.general_beds > 0:
                self.general_beds -= 1
                self.allocated[patient.name] = "General"
                return True
        return False


    def admit_patient(self, patient: Patient):
        """Called when a new patient arrives."""
        self.patients[patient.name] = patient

        if not self._try_allocate(patient):
            # No bed available → go to waiting queue
            heapq.heappush(self.waiting_queue, patient)


    def discharge_patient(self, name):
        if name in self.allocated:
            bed = self.allocated.pop(name)
            if bed == "ICU":
                self.icu_beds += 1
            else:
                self.general_beds += 1
            self.patients.pop(name, None)
        else:
            # Remove from waiting queue
            self.waiting_queue = [p for p in self.waiting_queue if p.name != name]
            heapq.heapify(self.waiting_queue)


    def reassign_beds(self):
        """
        - Upgrade critical patients from General to ICU if possible.
        - Assign waiting patients to free beds.
        Returns list of moved patients (for animation).
        """
        moved = []

        # 1. Upgrade critical patients from General to ICU
        for name, bed in list(self.allocated.items()):
            if bed == "General":
                p = self.patients[name]
                if p.condition == "critical" and self.icu_beds > 0:
                    # Free General, occupy ICU
                    self.general_beds += 1
                    self.icu_beds -= 1
                    self.allocated[name] = "ICU"
                    moved.append(name)

        # 2. Try to assign waiting patients
        newly_allocated = []
        while self.waiting_queue:
            patient = heapq.heappop(self.waiting_queue)
            if self._try_allocate(patient):
                # Allocation succeeded
                newly_allocated.append(patient.name)
                moved.append(patient.name)
            else:
                # Still no bed → put back and stop (no point trying others)
                heapq.heappush(self.waiting_queue, patient)
                break

        # 3. If any waiting patient got a bed, they are already in allocated.
        #    No extra action needed.

        return moved


    def status(self):
        return {
            "ICU Beds": self.icu_beds,
            "General Beds": self.general_beds,
            "Allocated": self.allocated.copy(),
            "Waiting Queue": [p.name for p in self.waiting_queue]
        }