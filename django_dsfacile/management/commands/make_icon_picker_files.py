import json
import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Add some initial sample data for the example app."

    def handle(self, *args, **options):
        # Note: the command should be able to be run several times without creating
        # duplicate objects.
        icons_root = "dsfacile/static/dsfacile/dist/icons/"
        icons_folders = os.listdir(icons_root)
        icons_folders.sort()

        json_root = "dsfacile/static/django-dsfacile/icon-picker/assets/icons-libraries/"

        all_folders = []

        for folder in icons_folders:
            icons_dict = {
                "prefix": "dsfacile-icon-",
                "version": "1.11.2",
                "icons": [],
            }

            files = os.listdir(os.path.join(icons_root, folder))
            files_without_extensions = [f.split(".")[0].replace("dsfacile--", "") for f in files]
            files_without_extensions.sort()

            dsfacile_folder = f"dsfacile-{folder}"
            dsfacile_folder_json = dsfacile_folder + ".json"
            icons_dict["icons"] = files_without_extensions
            icons_dict["icon-style"] = dsfacile_folder
            icons_dict["list-label"] = f"dsfacile {folder.title()}"

            all_folders.append(dsfacile_folder_json)

            json_file = os.path.join(json_root, dsfacile_folder_json)
            with open(json_file, "w") as fp:
                json.dump(icons_dict, fp)

        print("Folders created or updated: ", all_folders)
