import argparse
import json
import semver

ap = argparse.ArgumentParser("Updates Version in json")

ap.add_argument("-t", "--tag", help="Version to be set to",)
ap.add_argument("--timestamp", help="Timestamp to be set for the version",)
args = vars(ap.parse_args())


def updateWithTag(ver):
    if not semver.VersionInfo.isvalid(ver):
        raise ValueError('No Valid Semver in Tag')
    return ver


def updateWithTimestamp(timestamp):
    version = "str"
    with open('sovtoken/sovtoken/metadata.json', 'r') as f:
        data = json.load(f)
        v = semver.VersionInfo.parse(data["version"])
        v = v.replace(prerelease="dev" + timestamp)
        version = str(v)
    return version


version = "string"

if args['tag'] is not None:
    version = updateWithTag(args['tag'])
    print("Version will be updated to: " + version)
else:
    if args['timestamp'] is not None:
        version = updateWithTimestamp(args['timestamp'])
        print("Replacing  Dev-Version with UX-timestamp: " + version)
    else:
        raise ValueError("Either timestamp or tag must be provided")

with open('sovtoken/sovtoken/metadata.json', 'r') as f:
    data = json.load(f)
    data["version"] = version
    json.dump(data, open("sovtoken/sovtoken/metadata.json", "w"), indent=2)

with open('sovtokenfees/sovtokenfees/metadata.json', 'r') as f:
    data = json.load(f)
    data["version"] = version
    json.dump(data, open("sovtokenfees/sovtokenfees/metadata.json", "w"), indent=2)

print("Updated version of sovtoken and sovtokenfees metadata.json to: ", version)
