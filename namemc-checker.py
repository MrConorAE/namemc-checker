# By Conor Eager, 2021. Licensed under the Mozilla Public License 2.0. See LICENSE file for details.
import requests
import time
print("NameMC Checker v1.0.2")
names = input(
    "Enter a list of names to check, seperated by a space: ").split(" ")
available = []
unavailable = []
error = []
invalid = []
i = 1
r = 0


def check(name, names, i, r):
    if (name == ''):
        print(f"[{i}/{len(names)}] Name is blank, skipping.")
        return
    print(f"[{i}/{len(names)} {name}] Requesting '{name}' from namemc.com...")
    # Make the request.
    try:
        request = requests.get(f"https://namemc.com/search?q={name}")
    except ConnectionError:
        print(f"[{i}/{len(names)} {name}] (!!) Connection error, exiting.")
        print("Check internet connection and try again.")
        exit()
    except ConnectionResetError:
        print(f"[{i}/{len(names)} {name}] (!!) Connection error (reset), exiting.")
        print("Connection was reset by system or server. Check internet connection and try again.")
        exit()
    except ConnectionAbortedError:
        print(f"[{i}/{len(names)} {name}] (!!) Connection error (aborted), exiting.")
        print("Connection was aborted by system or server. Check internet connection and try again.")
        exit()
    except ConnectionRefusedError:
        print(f"[{i}/{len(names)} {name}] (!!) Connection error (refused), exiting.")
        print("Connection was refused by server. Check internet connection and try again.")
        exit()
    print(f"[{i}/{len(names)} {name}] Response recieved, status {request.status_code}, {len(request.content)} bytes")
    # If not an error (e.g. >=400), continue
    if (request.ok):
        # Attempt to find availability using a simple find
        print(f"[{i}/{len(names)} {name}] Extracting availability...")
        if ("<div><strong>Status</strong></div>\n<div>Available*</div>" in request.text):
            # It's available!
            print(f"[{i}/{len(names)} {name}] {name} is available!")
            available.append(name)
        elif ("<div><strong>Status</strong></div>\n<div>Unavailable</div>" in request.text):
            # It's unavailable!
            print(f"[{i}/{len(names)} {name}] {name} is not available.")
            unavailable.append(name)
        elif ("<div><strong>Status</strong></div>\n<div>Available Later*</div>" in request.text):
            # It's unavailable!
            print(f"[{i}/{len(names)} {name}] {name} is available later.")
            unavailable.append(name)
        elif ("<div><strong>Status</strong></div>\n<div>Too Short</div>" in request.text):
            # It's too short!
            print(f"[{i}/{len(names)} {name}] {name} is too short.")
            invalid.append(name)
        elif ("<div><strong>Status</strong></div>\n<div>Too Long</div>" in request.text):
            # It's too long!
            print(f"[{i}/{len(names)} {name}] {name} is too long.")
            invalid.append(name)
        elif ("<div><strong>Status</strong></div>\n<div>Invalid Characters</div>" in request.text):
            # It's got invalid characters!
            print(f"[{i}/{len(names)} {name}] {name} contains invalid characters.")
            invalid.append(name)
        else:
            # Something else
            print(
                f"[{i}/{len(names)} {name}] (!!) Could not extract availability, skipping.")
            error.append(name)
    # It's an error :(
    # Try to handle it
    elif (request.status_code >= 500):
        print(f"[{i}/{len(names)} {name}] (!!) 5xx Server Error, exiting.")
        print("Try again later.")
        exit()
    elif (request.status_code == 429):
        if r == 6:
            # Too many retries. Give up and move on.
            raise RecursionError()
        print(
            f"[{i}/{len(names)} {name}] (!!) 429 Too Many Requests, retrying after 30s.")
        print("If you wish to abort and stop all checking, press Ctrl-C to force quit and exit now.")
        time.sleep(30)
        # Recursion! Yay!
        r += 1
        check(name, names, i, r)
    elif (request.status_code == 404):
        print(f"[{i}/{len(names)} {name}] (!!) 404 Not Found, exiting.")
        print("Check request URL is correct and accessible by browser, then try again.")
        exit()
    else:
        print(f"[{i}/{len(names)} {name}] (!!) Response is an error, skipping.")
        error.append(name)


if len(names) >= 50:
    print("\nWARNING ==========================")
    print(
        f"Currently, the list of names to check contains {len(names)} usernames.")
    print("This will cause some name checks to FAIL due to rate limits on the NameMC servers.")
    print("(Names that fail will be listed as 'errors'. You can then try them again later.)")
    print(
        f"\nEstimated failures: {round(len(names)/40)} of {len(names)} names (~{round(((len(names)/40)/len(names))*100, 2)}%)")
    print(
        f"\n- To proceed and check {len(names)} usernames, type 'Proceed' and then press ENTER.")
    print("- To quit and re-enter your list of names, type anything else or just press ENTER.")
    if (input("> ") == "Proceed"):
        print(f"Proceeding to check {len(names)}.")
        pass
    else:
        exit()

round(((len(names)/40)/len(names))*100)

for name in names:
    print("==========")
    try:
        check(name, names, i, 0)
    except RecursionError:
        print(f"[{i}/{len(names)} {name}] (!!) Too many retries, skipping.")
        error.append(name)
        continue
    except:
        print(f"[{i}/{len(names)} {name}] (!!) Unknown error, exiting.")
        print("Please check your internet connection and try again.")
        exit()
    i += 1
print(
    f"\n\[COMPLETE] All requested names complete. {len(error)} errored, {len(available)} available, {len(unavailable)} unavailable of {len(names)} names.")
print("\nAVAILABLE:")
print(", ".join(available))
print("\nUNAVAILABLE or AVAILABLE LATER:")
print(", ".join(unavailable))
print("\nINVALID:")
print(", ".join(invalid))
print("\nERRORS")
print(", ".join(error))
print("\nDone.")
input("Press ENTER to quit.")
