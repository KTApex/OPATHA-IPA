#!/usr/bin/env python3
"""Generate a valid PhotosApp.xcodeproj using plistlib.
Recreates the project on CI so we don't need to commit .xcodeproj."""
import os
import plistlib
import uuid

PROJ = "PhotosApp"

def uid():
    return uuid.uuid4().hex.upper()[:24]

# Collect source files
srcs = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if not d.startswith(".") and d != ".build" and d != ".github" and d != "Sources"]
    for f in sorted(files):
        if f.endswith(".swift") and f != "Package.swift":
            full = os.path.join(root, f).replace("\\", "/").lstrip("./")
            srcs.append(full)

srcs.sort()

# Generate IDs
frefs = {s: uid() for s in srcs}
bfs = {s: uid() for s in srcs}
info_id = uid()
prod_id = uid()
group_id = uid()
src_ph = uid()
fw_ph = uid()
res_ph = uid()
p_debug = uid()
p_release = uid()
t_debug = uid()
t_release = uid()
p_cl = uid()
t_cl = uid()
tgt_id = uid()
root_id = uid()

objects = {}

# File references
for s in srcs:
    objects[frefs[s]] = {
        "isa": "PBXFileReference",
        "lastKnownFileType": "sourcecode.swift",
        "name": os.path.basename(s),
        "path": s,
        "sourceTree": "<group>",
    }

objects[info_id] = {
    "isa": "PBXFileReference",
    "lastKnownFileType": "text.plist.xml",
    "name": "Info.plist",
    "path": "Info.plist",
    "sourceTree": "<group>",
}

objects[prod_id] = {
    "isa": "PBXFileReference",
    "explicitFileType": "wrapper.application",
    "includeInIndex": 0,
    "path": "PhotosApp.app",
    "sourceTree": "BUILT_PRODUCTS_DIR",
}

# Build files
for s in srcs:
    objects[bfs[s]] = {
        "isa": "PBXBuildFile",
        "fileRef": frefs[s],
    }

# Group
objects[group_id] = {
    "isa": "PBXGroup",
    "children": [frefs[s] for s in srcs] + [info_id],
    "name": PROJ,
    "sourceTree": "<group>",
}

# Build phases
objects[src_ph] = {
    "isa": "PBXSourcesBuildPhase",
    "buildActionMask": 2147483647,
    "files": [bfs[s] for s in srcs],
    "runOnlyForDeploymentPostprocessing": 0,
}

objects[fw_ph] = {
    "isa": "PBXFrameworksBuildPhase",
    "buildActionMask": 2147483647,
    "files": [],
    "runOnlyForDeploymentPostprocessing": 0,
}

objects[res_ph] = {
    "isa": "PBXResourcesBuildPhase",
    "buildActionMask": 2147483647,
    "files": [],
    "runOnlyForDeploymentPostprocessing": 0,
}

# Build configs - project level
objects[p_debug] = {
    "isa": "XCBuildConfiguration",
    "buildSettings": {
        "ALWAYS_SEARCH_USER_PATHS": "NO",
        "CLANG_ENABLE_MODULES": "YES",
        "CODE_SIGN_IDENTITY": "",
        "CODE_SIGNING_ALLOWED": "NO",
        "CODE_SIGNING_REQUIRED": "NO",
        "IPHONEOS_DEPLOYMENT_TARGET": "15.0",
        "SDKROOT": "iphoneos",
        "SWIFT_ACTIVE_COMPILATION_CONDITIONS": "DEBUG",
        "SWIFT_OPTIMIZATION_LEVEL": "-Onone",
    },
    "name": "Debug",
}

objects[p_release] = {
    "isa": "XCBuildConfiguration",
    "buildSettings": {
        "ALWAYS_SEARCH_USER_PATHS": "NO",
        "CLANG_ENABLE_MODULES": "YES",
        "CODE_SIGN_IDENTITY": "",
        "CODE_SIGNING_ALLOWED": "NO",
        "CODE_SIGNING_REQUIRED": "NO",
        "IPHONEOS_DEPLOYMENT_TARGET": "15.0",
        "SDKROOT": "iphoneos",
        "SWIFT_OPTIMIZATION_LEVEL": "-O",
        "VALIDATE_PRODUCT": "YES",
    },
    "name": "Release",
}

objects[p_cl] = {
    "isa": "XCConfigurationList",
    "buildConfigurations": [p_debug, p_release],
    "defaultConfigurationIsVisible": 0,
    "defaultConfigurationName": "Release",
}

# Build configs - target level
objects[t_debug] = {
    "isa": "XCBuildConfiguration",
    "buildSettings": {
        "ASSETCATALOG_COMPILER_APPICON_NAME": "AppIcon",
        "CODE_SIGN_IDENTITY": "",
        "CODE_SIGNING_ALLOWED": "NO",
        "CODE_SIGNING_REQUIRED": "NO",
        "CURRENT_PROJECT_VERSION": "1",
        "ENABLE_PREVIEWS": "YES",
        "INFOPLIST_FILE": "Info.plist",
        "IPHONEOS_DEPLOYMENT_TARGET": "15.0",
        "LD_RUNPATH_SEARCH_PATHS": ["$(inherited)", "@executable_path/Frameworks"],
        "MARKETING_VERSION": "1.0",
        "PRODUCT_BUNDLE_IDENTIFIER": "com.example.photosapp",
        "PRODUCT_NAME": "$(TARGET_NAME)",
        "SWIFT_OPTIMIZATION_LEVEL": "-Onone",
        "SWIFT_VERSION": "5.0",
        "TARGETED_DEVICE_FAMILY": "1,2",
    },
    "name": "Debug",
}

objects[t_release] = {
    "isa": "XCBuildConfiguration",
    "buildSettings": {
        "ASSETCATALOG_COMPILER_APPICON_NAME": "AppIcon",
        "CODE_SIGN_IDENTITY": "",
        "CODE_SIGNING_ALLOWED": "NO",
        "CODE_SIGNING_REQUIRED": "NO",
        "CURRENT_PROJECT_VERSION": "1",
        "ENABLE_PREVIEWS": "YES",
        "INFOPLIST_FILE": "Info.plist",
        "IPHONEOS_DEPLOYMENT_TARGET": "15.0",
        "LD_RUNPATH_SEARCH_PATHS": ["$(inherited)", "@executable_path/Frameworks"],
        "MARKETING_VERSION": "1.0",
        "PRODUCT_BUNDLE_IDENTIFIER": "com.example.photosapp",
        "PRODUCT_NAME": "$(TARGET_NAME)",
        "SWIFT_VERSION": "5.0",
        "TARGETED_DEVICE_FAMILY": "1,2",
    },
    "name": "Release",
}

objects[t_cl] = {
    "isa": "XCConfigurationList",
    "buildConfigurations": [t_debug, t_release],
    "defaultConfigurationIsVisible": 0,
    "defaultConfigurationName": "Release",
}

# Target
objects[tgt_id] = {
    "isa": "PBXNativeTarget",
    "buildConfigurationList": t_cl,
    "buildPhases": [src_ph, fw_ph, res_ph],
    "buildRules": [],
    "dependencies": [],
    "name": PROJ,
    "productName": PROJ,
    "productReference": prod_id,
    "productType": "com.apple.product-type.application",
}

# Root project
objects[root_id] = {
    "isa": "PBXProject",
    "attributes": {
        "BuildIndependentTargetsInParallel": 1,
        "LastSwiftUpdateCheck": 1500,
        "LastUpgradeCheck": 1500,
    },
    "buildConfigurationList": p_cl,
    "compatibilityVersion": "Xcode 13.0",
    "developmentRegion": "en",
    "hasScannedForEncodings": 0,
    "knownRegions": ["en", "Base"],
    "mainGroup": group_id,
    "productRefGroup": group_id,
    "projectDirPath": "",
    "projectRoot": "",
    "targets": [tgt_id],
}

# Build the project dir
pbxproj = f"{PROJ}.xcodeproj/project.pbxproj"
os.makedirs(os.path.dirname(pbxproj), exist_ok=True)

# Write as ASCII plist
with open(pbxproj, "wb") as f:
    plistlib.dump(objects, f, fmt=plistlib.FMT_XML)

# Re-read and convert to old-style format manually
with open(pbxproj, "r") as f:
    content = f.read()

# Wrap in pbxproj structure
header = "// !$*UTF8*$!\n"
outer = '''{
\tarchiveVersion = 1;
\tclasses = {
\t};
\tobjectVersion = 56;
\tobjects = {
'''
footer = "\t};\n\trootObject = " + root_id + ";\n}\n"

# Convert XML plist to old-style ascii plist
# plistlib can output XML, but xcodebuild also accepts XML plist for .pbxproj
# Actually no - xcodebuild only accepts old-style. Let me write old-style manually.

lines = []
lines.append("// !$*UTF8*$!")
lines.append("{")
lines.append("\tarchiveVersion = 1;")
lines.append("\tclasses = {")
lines.append("\t};")
lines.append("\tobjectVersion = 56;")
lines.append("\tobjects = {")

def fmt_val_ascii(v, indent=3):
    tab = "\t" * indent
    inner = "\t" * (indent + 1)
    if isinstance(v, dict):
        items = []
        for k, v2 in v.items():
            items.append(f"{inner}{k} = {fmt_val_ascii(v2, indent + 2)};")
        return "{\n" + "\n".join(items) + "\n" + tab + "}"
    elif isinstance(v, list):
        if not v:
            return "(\n" + tab + ")"
        items = ",\n".join(f"{inner}{fmt_val_ascii(x, indent + 1)}" for x in v)
        return "(\n" + items + "\n" + tab + ")"
    elif isinstance(v, bool):
        return "YES" if v else "NO"
    elif isinstance(v, (int, float)):
        return str(v)
    else:
        s = str(v)
        if s.startswith("$("):
            return s
        return f'"{s}"'

for oid in sorted(objects.keys()):
    obj = objects[oid]
    isa = obj["isa"]
    lines.append(f"\n/* Begin {isa} section */")
    lines.append(f"\t\t{oid} /* {PROJ} */ = {{")
    lines.append(f"\t\t\tisa = {isa};")
    for k, v in obj.items():
        if k == "isa":
            continue
        lines.append(f"\t\t\t{k} = {fmt_val_ascii(v)};")
    lines.append("\t\t};")
    lines.append(f"/* End {isa} section */")

lines.append("\t};")
lines.append(f"\trootObject = {root_id};")
lines.append("}")

with open(pbxproj, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"✓ Created {pbxproj} — {len(srcs)} source files")
for s in srcs:
    print(f"   {s}")
