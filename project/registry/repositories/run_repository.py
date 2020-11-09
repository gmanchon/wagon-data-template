
import uuid


class RunRepository():

    def __init__(self):

        # get conf
        pass

    def get_run_id(self):
        """
        returns run id
        """

        # return run id
        return "run_" + uuid.uuid4().hex
