
from google.cloud import storage

from os.path import join

import re


class ModelRepository():

    def __init__(self, conf):

        # get conf
        self.bucket_name = conf.bucket_name
        self.storage_path = conf.storage_path
        self.local_path = conf.local_path
        self.model_filename = conf.model_filename

        # client
        self.storage_client = storage.Client()

    def store_model(self, experiment, run):

        # get storage path
        storage_path = self.__get_model_storage_path(experiment, run)

        # build local model file path
        local_model_path = join(self.local_path, self.model_filename)

        # build storage model file path
        storage_model_path = join(storage_path, self.model_filename)

        # store model on bucket
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(storage_model_path)
        blob.upload_from_filename(local_model_path)

    def list_models(self):

        # list blobs from bucket
        blobs = self.storage_client.list_blobs(self.bucket_name)

        paths = "".join([blob.name for blob in blobs])

        # extract runs from blob paths
        runs = re.findall(r"/([a-z0-9]{32})/", paths)

        return runs

    def get_model(self, experiment, run):

        # get storage path
        storage_path = self.__get_model_storage_path(experiment, run)

        # build local model file path
        local_model_path = join(self.local_path, self.model_filename)

        # build storage model file path
        storage_model_path = join(storage_path, self.model_filename)

        # get model from bucket
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(storage_model_path)
        blob.download_to_filename(local_model_path)

    def __get_model_storage_path(self, experiment, run):

        # build storage path from expirement and current run
        storage_path = self.storage_path \
            .replace(":experiment", experiment) \
            .replace(":run", run)

        return storage_path
