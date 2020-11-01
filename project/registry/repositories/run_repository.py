
import uuid


class RunRepository():

    def __init__(self):

        # current run
        self.run = None

    def get_current_run(self):

        # check whether run was created
        if self.run is None:

            # create new run
            self.__new_run()

        return self.run

    def new_run(self):

        # create new run
        self.__new_run()

    def __new_run(self):

        # create run id
        self.run = uuid.uuid4().hex
