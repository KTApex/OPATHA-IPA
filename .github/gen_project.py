#!/usr/bin/env python3
"""Generate a valid PhotosApp.xcodeproj on the CI runner.
Handles nested dicts in Xcode's old-style plist format."""
import os
import uuid

PROJ = "PhotosApp"

def uid():
    return uuid.uuid4().hex.upper()[:24]

# Collect .swift files
srcs = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if not d.startswith(".") and d != ".build"]
    for f in files:
        if f.endswith(".swift") and f != "Package.swift":
            srcs.append(os.path.join(root, f).replace("\\", "/").lstrip("./"))
srcs.sort()

fref_ids = {s: uid() for s in srcs}
bf_ids = {s: uid() for s in srcs}
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
tgt = uid()
root = uid()

def fmt_val(v, indent=3):
    """Format a value in Xcode pbxproj format."""
    tab = "\t" * indent
    if isinstance(v, dict):
        items = []
        for k, v2 in v.items():
            items.append(f"{tab}{k} = {fmt_val(v2, indent+1)};")
        return "{\n" + "\n".join(items) + "\n" + ("\t" * (indent-1)) + "}"
    elif isinstance(v, list):
        if not v:
            return "(\n\n" + ("\t" * (indent-1)) + ")"
        items = ",\n".join(f"{tab}{fmt_val(x, indent+1)}" for x in v)
        return "(\n" + items + "\n" + ("\t" * (indent-1)) + ")"
    elif isinstance(v, bool):
        return "YES" if v else "NO"
    elif isinstance(v, int):
        return str(v)
    elif isinstance(v, str):
        if v.startswith("$("):
            return v
        return f'"{v}"'
    return str(v)

def add(oid, isa, body):
    lines.append(f"\n/* Begin {isa} section */")
    lines.append(f"\t\t{oid} /* {PROJ} */ = {{")
    lines.append(f"\t\t\tisa = {isa};")
    for k, v in body:
        lines.append(f"\t\t\t{k} = {fmt_val(v)};")
    lines.append("\t\t};")
    lines.append(f"/* End {isa} section */")

lines = [
    "// !$*UTF8*$!",
    "{",
    "\tarchiveVersion = 1;",
    "\tclasses = {",
    "\t};",
    "\tobjectVersion = 56;",
    "\tobjects = {",
]

# File references
for s in srcs:
    add(fref_ids[s], "PBXFileReference", [
        ("lastKnownFileType", "sourcecode.swift"),
        ("name", os.path.basename(s)),
        ("path", s),
        ("sourceTree", "<group>"),
    ])

add(info_id, "PBXFileReference", [
    ("lastKnownFileType", "text.plist.xml"),
    ("name", "Info.plist"),
    ("path", "Info.plist"),
    ("sourceTree", "<group>"),
])

add(prod_id, "PBXFileReference", [
    ("explicitFileType", "wrapper.application"),
    ("includeInIndex", 0),
    ("path", "PhotosApp.app"),
    ("sourceTree", "BUILT_PRODUCTS_DIR"),
])

# Build files
for s in srcs:
    add(bf_ids[s], "PBXBuildFile", [
        ("fileRef", fref_ids[s]),
    ])

# Group
all_children = [fref_ids[s] for s in srcs] + [info_id]
add(group_id, "PBXGroup", [
    ("children", all_children),
    ("name", PROJ),
    ("sourceTree", "<group>"),
])

# Build phases
add(src_ph, "PBXSourcesBuildPhase", [
    ("buildActionMask", 2147483647),
    ("files", [bf_ids[s] for s in srcs]),
    ("runOnlyForDeploymentPostprocessing", 0),
])

add(fw_ph, "PBXFrameworksBuildPhase", [
    ("buildActionMask", 2147483647),
    ("files", []),
    ("runOnlyForDeploymentPostprocessing", 0),
])

add(res_ph, "PBXResourcesBuildPhase", [
    ("buildActionMask", 2147483647),
    ("files", []),
    ("runOnlyForDeploymentPostprocessing", 0),
])

# Project level configs
add(p_debug, "XCBuildConfiguration", [
    ("buildSettings", {
        "ALWAYS_SEARCH_USER_PATHS": "NO",
        "CLANG_ENABLE_MODULES": "YES",
        "CODE_SIGN_IDENTITY": "",
        "CODE_SIGNING_ALLOWED": "NO",
        "CODE_SIGNING_REQUIRED": "NO",
        "IPHONEOS_DEPLOYMENT_TARGET": "15.0",
        "SDKROOT": "iphoneos",
        "SWIFT_OPTIMIZATION_LEVEL": "-Onone",
        "SWIFT_ACTIVE_COMPILATION_CONDITIONS": "DEBUG",
    }),
    ("name", "Debug"),
])

add(p_release, "XCBuildConfiguration", [
    ("buildSettings", {
        "ALWAYS_SEARCH_USER_PATHS": "NO",
        "CLANG_ENABLE_MODULES": "YES",
        "CODE_SIGN_IDENTITY": "",
        "CODE_SIGNING_ALLOWED": "NO",
        "CODE_SIGNING_REQUIRED": "NO",
        "IPHONEOS_DEPLOYMENT_TARGET": "15.0",
        "SDKROOT": "iphoneos",
        "SWIFT_OPTIMIZATION_LEVEL": "-O",
        "VALIDATE_PRODUCT": "YES",
    }),
    ("name", "Release"),
])

add(p_cl, "XCConfigurationList", [
    ("buildConfigurations", [p_debug, p_release]),
    ("defaultConfigurationIsVisible", 0),
    ("defaultConfigurationName", "Release"),
])

# Target level configs
common = {
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
}

add(t_debug, "XCBuildConfiguration", [
    ("buildSettings", dict(common, SWIFT_OPTIMIZATION_LEVEL="-Onone")),
    ("name", "Debug"),
])

add(t_release, "XCBuildConfiguration", [
    ("buildSettings", common),
    ("name", "Release"),
])

add(t_cl, "XCConfigurationList", [
    ("buildConfigurations", [t_debug, t_release]),
    ("defaultConfigurationIsVisible", 0),
    ("defaultConfigurationName", "Release"),
])

# Target
add(tgt, "PBXNativeTarget", [
    ("buildConfigurationList", t_cl),
    ("buildPhases", [src_ph, fw_ph, res_ph]),
    ("buildRules", []),
    ("dependencies", []),
    ("name", PROJ),
    ("productName", PROJ),
    ("productReference", prod_id),
    ("productType", "com.apple.product-type.application"),
])

# Root project
add(root, "PBXProject", [
    ("attributes", {
        "BuildIndependentTargetsInParallel": 1,
        "LastSwiftUpdateCheck": 1500,
        "LastUpgradeCheck": 1500,
    }),
    ("buildConfigurationList", p_cl),
    ("compatibilityVersion", "Xcode 13.0"),
    ("developmentRegion", "en"),
    ("hasScannedForEncodings", 0),
    ("knownRegions", ["en", "Base"]),
    ("mainGroup", group_id),
    ("productRefGroup", group_id),
    ("projectDirPath", ""),
    ("projectRoot", ""),
    ("targets", [tgt]),
])

lines.append("\t};")
lines.append(f"\trootObject = {root};")
lines.append("}")

pbxproj = f"{PROJ}.xcodeproj/project.pbxproj"
os.makedirs(os.path.dirname(pbxproj), exist_ok=True)
with open(pbxproj, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"✓ Created {pbxproj} — {len(srcs)} source files")
for s in srcs:
    print(f"   {s}")
