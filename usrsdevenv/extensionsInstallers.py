import os
import json

def extensions_installer(software, platform, extensionsList):
    """
    Provide the following to see if there is a special way to install extensions

    Keyword arguments:
    software -- 'chrome'
    platform -- 'posix'|'nt'
    extensionsList -- A list of extensions to install
    """

    if 'chrome' == software:
    # Chrome does not provide a means of installing extensions via CLI,
    # But, you can set a policy to have them installed.
    # https://github.com/mdamien/chrome-extensions-archive/issues/8
    # https://www.chromium.org/administrators/policy-list-3#ExtensionInstallForcelist

        chromeKeysToAddExtensionTo = ['ExtensionInstallForcelist',
                                      'ExtensionInstallWhitelist']
        print("Attempting to add the following package IDs to Chrome:")
        print(extensionsList)
        if 'posix' == platform:
            policyDirPath = '/etc/opt/chrome/policies/managed/'
            policyFilename = 'mypolicy.json'
            os.makedirs(policyDirPath, exist_ok=True)
            mypolicy = {}
            policyFile = os.path.join(policyDirPath, policyFilename)

            if os.path.isfile(policyFile):
                with open(policyFile, 'r') as f:
                    mypolicy = json.load(f)
                os.remove(policyFile)
            for chromeKey in chromeKeysToAddExtensionTo:
                if (chromeKey in mypolicy and len(mypolicy[chromeKey]) > 0):
                    for extension in extensionsList:
                        if extension in mypolicy[chromeKey]:
                            print("{} Already in {}".format(extension, chromeKey))
                        else:
                            mypolicy[chromeKey].append(extension)
            else:
                mypolicy['ExtensionInstallForcelist'] = extensionsList
                mypolicy['ExtensionInstallWhitelist'] = extensionsList
            with open(policyFile, 'w') as f:
                json.dump(mypolicy, f, indent=4)
        else:
            raise Exception('{} extension installation not yet supported on {}'.format(software, platform))
    else:
        raise Exception('No built-in function for installing {} extensions'.format(software))