#!/usr/bin/env python3
"""Generate a minimal PhotosApp.xcodeproj on the CI runner.
No need to commit binary .xcodeproj to the repo."""
import os
import uuid
import subprocess

PROJ = "PhotosApp"

def uid():
    return uuid.uuid4().hex.upper()[:24]

# Collect all .swift files
srcs = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if not d.startswith(".") and d != ".build" and d != ".github"]
    for f in files:
        if f.endswith(".swift") and f != "Package.swift":
            srcs.append(os.path.join(root, f).replace("\\", "/").lstrip("./"))
srcs.sort()

# IDs
fref_ids = {s: uid() for s in srcs}
bf_ids   = {s: uid() for s in srcs}
info_plist_id    = uid()
product_ref_id   = uid()
group_id         = uid()
src_phase_id     = uid()
fw_phase_id      = uid()
res_phase_id     = uid()
proj_debug_id    = uid()
proj_release_id  = uid()
tgt_debug_id     = uid()
tgt_release_id   = uid()
proj_cl_id       = uid()
tgt_cl_id        = uid()
target_id        = uid()
root_obj_id      = uid()

# Build lines
lines = [
    "// !$*UTF8*$!",
    "{",
    "\tarchiveVersion = 1;",
    "\tclasses = {",
    "\t};",
    "\tobjectVersion = 56;",
    "\tobjects = {",
]

def add(obj_id, isa, body):
    lines.append(f"\n/* Begin {isa} section */")
    lines.append(f"\t\t{obj_id} /* {PROJ} */ = {{")
    lines.append(f"\t\t\tisa = {isa};")
    for k, v in body:
        if isinstance(v, list):
            items = ",\n".join(f"\t\t\t\t\t{x}" for x in v)
            lines.append(f"\t\t\t{k} = (\n{items}\n\t\t\t);")
        elif isinstance(v, str):
            lines.append(f'\t\t\t{k} = "{v}";')
        elif isinstance(v, bool):
            lines.append(f"\t\t\t{k} = {'YES' if v else 'NO'};")
        else:
            lines.append(f"\t\t\t{k} = {v};")
    lines.append("\t\t};")
    lines.append(f"/* End {isa} section */")

# File references
for s in srcs:
    add(fref_ids[s], "PBXFileReference", [
        ("lastKnownFileType", "sourcecode.swift"),
        ("name", os.path.basename(s)),
        ("path", s),
        ("sourceTree", "<group>"),
    ])

add(info_plist_id, "PBXFileReference", [
    ("lastKnownFileType", "text.plist.xml"),
    ("name", "Info.plist"),
    ("path", "Info.plist"),
    ("sourceTree", "<group>"),
])

add(product_ref_id, "PBXFileReference", [
    ("explicitFileType", "wrapper.application"),
    ("includeInIndex", 0),
    ("path", f"{PROJ}.app"),
    ("sourceTree", "BUILT_PRODUCTS_DIR"),
])

# Build files
for s in srcs:
    add(bf_ids[s], "PBXBuildFile", [
        ("fileRef", fref_ids[s]),
    ])

# Group
all_children = [fref_ids[s] for s in srcs] + [info_plist_id]
add(group_id, "PBXGroup", [
    ("children", all_children),
    ("name", PROJ),
    ("sourceTree", "<group>"),
])

# Build phases
add(src_phase_id, "PBXSourcesBuildPhase", [
    ("buildActionMask", 2147483647),
    ("files", [bf_ids[s] for s in srcs]),
    ("runOnlyForDeploymentPostprocessing", 0),
])

add(fw_phase_id, "PBXFrameworksBuildPhase", [
    ("buildActionMask", 2147483647),
    ("files", []),
    ("runOnlyForDeploymentPostprocessing", 0),
])

add(res_phase_id, "PBXResourcesBuildPhase", [
    ("buildActionMask", 2147483647),
    ("files", []),
    ("runOnlyForDeploymentPostprocessing", 0),
])

# Build configs (project level)
add(proj_debug_id, "XCBuildConfiguration", [
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

add(proj_release_id, "XCBuildConfiguration", [
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

add(proj_cl_id, "XCConfigurationList", [
    ("buildConfigurations", [proj_debug_id, proj_release_id]),
    ("defaultConfigurationIsVisible", 0),
    ("defaultConfigurationName", "Release"),
])

# Build configs (target level)
common_build = {
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

add(tgt_debug_id, "XCBuildConfiguration", [
    ("buildSettings", dict(common_build, **{"SWIFT_OPTIMIZATION_LEVEL": "-Onone"})),
    ("name", "Debug"),
])

add(tgt_release_id, "XCBuildConfiguration", [
    ("buildSettings", common_build),
    ("name", "Release"),
])

add(tgt_cl_id, "XCConfigurationList", [
    ("buildConfigurations", [tgt_debug_id, tgt_release_id]),
    ("defaultConfigurationIsVisible", 0),
    ("defaultConfigurationName", "Release"),
])

# Target
add(target_id, "PBXNativeTarget", [
    ("buildConfigurationList", tgt_cl_id),
    ("buildPhases", [src_phase_id, fw_phase_id, res_phase_id]),
    ("buildRules", []),
    ("dependencies", []),
    ("name", PROJ),
    ("productName", PROJ),
    ("productReference", product_ref_id),
    ("productType", "com.apple.product-type.application"),
])

# Root project
add(root_obj_id, "PBXProject", [
    ("attributes", {
        "BuildIndependentTargetsInParallel": 1,
        "LastSwiftUpdateCheck": 1500,
        "LastUpgradeCheck": 1500,
    }),
    ("buildConfigurationList", proj_cl_id),
    ("compatibilityVersion", "Xcode 13.0"),
    ("developmentRegion", "en"),
    ("hasScannedForEncodings", 0),
    ("knownRegions", ["en", "Base"]),
    ("mainGroup", group_id),
    ("productRefGroup", group_id),
    ("projectDirPath", ""),
    ("projectRoot", ""),
    ("targets", [target_id]),
])

lines.append("\t};")
lines.append(f"\trootObject = {root_obj_id};")
lines.append("}")

# Write
pbxproj = f"{PROJ}.xcodeproj/project.pbxproj"
os.makedirs(os.path.dirname(pbxproj), exist_ok=True)
with open(pbxproj, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"✓ Created {pbxproj} — {len(srcs)} source files, {len(lines)} lines")
for s in srcs:
    print(f"   {s}")
