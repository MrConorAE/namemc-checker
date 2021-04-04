# By Conor Eager, 2021. Licensed under the Mozilla Public License 2.0. See LICENSE file for details.
import requests
print("NameMC Checker v1.0")
names = input(
    "Enter a list of names to check, seperated by a space: ").split(" ")
available = []
unavailable = []
error = []
i = 1
for name in names:
    print("==========")
    print(f"[{i}/{len(names)} {name}] Requesting '{name}' from namemc.com...")
    request = requests.get(f"https://namemc.com/search?q={name}")
    print(f"[{i}/{len(names)} {name}] Response recieved, status {request.status_code}, {len(request.content)} bytes")
    if (request.ok):
        print(f"[{i}/{len(names)} {name}] Extracting availability...")
        if ("<div><strong>Status</strong></div>\n<div>Available*</div>" in request.text):
            print(f"[{i}/{len(names)} {name}] {name} is available!")
            available.append(name)
        elif ("<div><strong>Status</strong></div>\n<div>Unavailable</div>" in request.text):
            print(f"[{i}/{len(names)} {name}] {name} is not available.")
            unavailable.append(name)
        else:
            print(
                f"[{i}/{len(names)} {name}] (!!) Could not extract availability, skipping.")
            error.append(name)
    else:
        print(f"[{i}/{len(names)} {name}] (!!) Response is an error, skipping.")
        error.append(name)
    i += 1
print(
    f"[COMPLETE] All requested names complete. {len(error)} errored, {len(available)} available, {len(unavailable)} unavailable of {len(names)} names.")
print("AVAILABLE:")
print(", ".join(available))
print("\nUNAVAILABLE:")
print(", ".join(unavailable))
print("\nERRORS")
print(", ".join(error))
print("\nDone.")
input("Press ENTER to quit.")
