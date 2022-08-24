# event handler class
class DLW_EventHandler:

    def __init__(self):
        # list of callback functions to call every time the event handler object is triggered
        self.callbacks = []

    # overloading '+=' operator to add new callback functions easily
    def __iadd__(self, callback):
        self.callbacks.append(callback)

        return self

    # overloading '-=' operator to remove existing callback functions easily
    def __isub__(self, callback):
        self.callbacks.remove(callback)

        return self

    # overloading '()' operator to trigger the event handler
    def __call__(self, *args, **kwargs):
        for callback in self.callbacks:
            callback(*args, **kwargs)
