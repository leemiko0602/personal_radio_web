#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    #import pdb; pdb.set_trace()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_Web.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
