# SEAT.PY

# Ethan Payne
# CS 499
# Dr. Crk - SIUE

class Seat:
    def __init__(self):
        self._label = 'no_label'
        self._occupationStatus = 'not_occupied'
        self._accomedations = 'none'
        self._user = 'no_user'
        self._xVal = 0
        self._yVal = 0

    def get_label(self):
        return self._label
    def set_label(self, x):
        self._label = x
    def del_label(self):
        del self.label

    def get_occupationStatus(self):
        return self._occupationStatus
    def set_occupationStatus(self, x):
        self._occupationStatus = x
    def del_occupationStatus(self):
        del self.occupationStatus

    def get_accomedations(self):
        return self._accomedations
    def set_accomedations(self, x):
        self._accomedations = x
    def del_accomedations(self):
        del self.accomedations

    def get_user(self):
        return self._user
    def set_user(self, x):
        self._user = x
    def del_user(self):
        del self.user

    def get_xVal(self):
        return self._xVal
    def set_xVal(self, x):
        self._xVal = x
    def del_xVal(self):
        del self.xVal

    def get_yVal(self):
        return self._yVal
    def set_yVal(self, x):
        self._yVal = x
    def del_yVal(self):
        del self.yVal

    label = property(get_label, set_label, del_label)
    occupationStatus = property(get_occupationStatus, set_occupationStatus, del_occupationStatus)
    accomedations = property(get_accomedations, set_accomedations, del_accomedations)
    user = property(get_user, set_user, del_user)
    xVal = property(get_xVal, set_xVal, del_xVal)
    yVal = property(get_yVal, set_yVal, del_yVal)