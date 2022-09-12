#!/usr/bin/env python3

import json
import logging
from os import remove
from pathlib import Path
from time import sleep

import inotify.adapters
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from azure.storage.blob import BlobClient

logging.basicConfig(level=logging.WARNING)


with open("config.json", "r") as f:
    config = json.load(f)


def main():
    i = inotify.adapters.Inotify()
    for u in config:
        i.add_watch(config[u]["path"])

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event
        if "IN_CLOSE_WRITE" in type_names:
            user = Path(path).parts[2]
            dsn = config[user]["dsn"]
            container = config[user]["container"]
            blob_name = f"{config[user]['slug']}/{filename}"
            for i in range(3):
                try:
                    blob = BlobClient.from_connection_string(
                        conn_str=dsn, container_name=container, blob_name=blob_name
                    )
                    with open(f"{path}/{filename}", "rb") as f:
                        logging.warning(f"Uploading: ['{path}/{filename}'] to ['{container}'] as ['{blob_name}']")
                        blob.upload_blob(f)
                    remove(f"{path}/{filename}")
                    break
                except ResourceExistsError:
                    logging.error(f"File with name '{blob_name}' already exists")
                    break
                except ResourceNotFoundError:
                    logging.error(f"Container: '{container}' does not exist")
                    break
                except Exception as e:
                    logging.error(e)
                    pass
                sleep(10)


if __name__ == "__main__":
    main()
