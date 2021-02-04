import fnmatch
import os
import re


def find_all_daedalus_files(dir_path):
    paths = []
    entries = os.listdir(dir_path)
    for entry in entries:
        full_path = os.path.join(dir_path, entry)
        if os.path.isdir(full_path):
            paths.extend(find_all_daedalus_files(full_path))
        else:
            if os.path.splitext(full_path)[1] == ".d":
                paths.append(full_path)
    return paths


class SrcHelper:
    def __init__(self, src_path):
        self.src_path = src_path
        self.dir_path = os.path.dirname(src_path)
        paths = self.get_paths(self.dir_path)
        self.lowercase_path_2_path = {path.lower(): path for path in paths}

    @classmethod
    def get_paths(cls, dir_path):
        paths = []
        entries = os.listdir(dir_path)
        for entry in entries:
            full_path = os.path.join(dir_path, entry)
            if os.path.isdir(full_path):
                paths.append(full_path)
                paths.extend(cls.get_paths(full_path))
            else:
                if os.path.splitext(full_path)[1].lower() == ".d":
                    paths.append(full_path)
        return paths

    @staticmethod
    def find_files(pattern, path):
        rule = re.compile(fnmatch.translate(pattern), re.IGNORECASE)
        return [
            os.path.join(path, name)
            for name in os.listdir(path)
            if rule.match(name)
        ]

    def get_daedalus_files_from_single_line(self, dir_path, parts):
        path = dir_path
        for part in parts:
            if '*' in part:
                # wildcard can appear only in the last part
                case_sensitive_path = self.lowercase_path_2_path[path.lower()]
                return self.find_files(part, case_sensitive_path)
            path = os.path.join(path, part)

        case_sensitive_path = self.lowercase_path_2_path[path.lower()]
        return [case_sensitive_path]

    def get_daedalus_files(self):
        result = []
        with open(self.src_path) as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if '//' in line:
                line = line.split('//')[0]

            if line:
                parts = re.split(r'[/\\]', line)
                result.extend(self.get_daedalus_files_from_single_line(self.dir_path, parts))

        return result
