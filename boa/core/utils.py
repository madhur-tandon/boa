import collections

from conda_build.config import get_or_merge_config
from conda_build.variants import find_config_files, parse_config_file
from conda_build import __version__ as cb_version

cb_split_version = tuple(int(x) for x in cb_version.split("."))


def get_config(folder):
    config = get_or_merge_config(None, {})
    if cb_split_version >= (3, 20, 5):
        config_files = find_config_files(folder, config)
    else:
        config_files = find_config_files(folder)
    parsed_cfg = collections.OrderedDict()
    for f in config_files:
        parsed_cfg[f] = parse_config_file(f, config)
        normalized = {}
        for k in parsed_cfg[f].keys():
            if "_" in k:
                n = k.replace("_", "-")
                normalized[n] = parsed_cfg[f][k]
        parsed_cfg[f].update(normalized)

    # TODO just using latest config here, should merge!
    if len(config_files):
        cbc = parsed_cfg[config_files[-1]]
    else:
        cbc = {}

    return cbc, config
