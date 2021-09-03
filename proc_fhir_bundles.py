from scratch.test_bundle import *
import json


def bundle_validator(bun):
    if bun['entry'][0]['resource']['code']['coding'][0]['display'] == "ASA":
        return False
    return True


def bundle(bun):
    try:
        for res in bun['entry']:
            fn_name = res['resource']['resourceType'].lower()
            functions[fn_name](res)
    except KeyError as e:
        print("Unknown key: {} in the bundle.".format(e))


def observation(res):
    res['fullUrl'] = "Observation/" + res['resource']['id']

    # Todo: Inform ngCAP team about this.
    #  The patient resource has string whereas Observation resource has an integer.
    res['resource']['meta']['versionId'] = str(res['resource']['meta']['versionId'])


def patient(res):
    res['fullUrl'] = "Patient/" + res['resource']['id']


functions = {'bundle': bundle, 'observation': observation, 'patient': patient}


if __name__ == "__main__":
    if bundle_validator(test_bundle_1): # TODO: Drop this once the Outbound Filter is fixed.
        try:
            func = test_bundle_1['resourceType'].lower()
            functions[func](test_bundle_1)
        except KeyError:
            print("Unknown resourceType:", test_bundle_1['resourceType'])

    print(json.dumps(test_bundle_1, indent=3))

    if bundle_validator(test_bundle_2): # TODO: Drop this once the Outbound Filter is fixed.
        try:
            func = test_bundle_2['resourceType'].lower()
            functions[func](test_bundle_2)
        except KeyError:
            print("Unknown resourceType:", test_bundle_2['resourceType'])
