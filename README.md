# Photos App (iOS 15.8 Clone)

A SwiftUI clone of the native iOS 15.8 Photos app with Face ID security, a 3-column image grid, and an advanced slideshow player. Designed to be sideloaded via **TrollStore** (unsigned .ipa).

## Features

- **Face ID / Touch ID / Passcode** – Locks the app on launch and when it backgrounds; requires authentication before showing photos.
- **Image Gallery** – 3-column `LazyVGrid` mimicking the iOS 15 Photos layout. Ships with 24 SF Symbol placeholders; swap in real images by adding a `url` property to `PhotoItem`.
- **Photo Detail** – Tap any thumbnail for a full-screen view with a "Play Slideshow" button.
- **Slideshow** – Full-screen player with on-screen controls (play/pause, skip, settings, close).
- **8 Transitions** – Fade, Slide, Zoom, Flip, Blur, Page Curl, Wipe, None.
- **Slideshow Options** – Configurable speed (2s–30s), Loop toggle, Shuffle toggle.
- **GitHub Actions CI** – Automatically builds an unsigned `.ipa` on every push to `main`.

## Xcode Project Setup

1. **Create a new Xcode project**:
   - File → New → Project → iOS → App
   - Interface: **SwiftUI**, Language: **Swift**
   - Product Name: `PhotosApp` (must match the GitHub Actions workflow)
   - Team: **None**

2. **Add the source files**:
   - Drag all `.swift` files from this repo into Xcode's Project Navigator.
   - Make sure "Create groups" is selected.

3. **Set up Info.plist**:
   - The provided `Info.plist` includes `NSFaceIDUsageDescription`. If Xcode generated its own `Info.plist`, merge the `NSFaceIDUsageDescription` key into it.
   - Value: `"Photos uses Face ID to protect access to your private photos and albums."`

4. **Enable Face ID capability**:
   - Target → Signing & Capabilities → `+` → **Face ID**

5. **Build settings** (for unsigned sideloading):
   - Set **Code Signing Identity** to `Don't Code Sign`
   - Set **Code Signing Style** to `Manual`

6. **Run on simulator** to verify it compiles and works.

## GitHub Actions (Unsigned .ipa)

1. Push this repo to GitHub (on the `main` branch).
2. Go to the **Actions** tab in your GitHub repository.
3. Select the **Build Unsigned IPA (TrollStore)** workflow.
4. Click **Run workflow** (or it runs automatically on push to `main`).
5. When the workflow finishes, download the `.ipa` artifact from the workflow run summary.
6. Transfer the `.ipa` to your iOS 15.8 device and open it in **TrollStore** to install.

## Switching to Real Images

In `Models/PhotoItem.swift`, replace the `systemImageName` and `colorName` properties with a `url: URL` property. Then update the placeholder views (`thumbnail`, `photoContent`) to load images via `AsyncImage` or a caching library like `Kingfisher` / `SDWebImageSwiftUI`.

## Requirements

- Xcode 14+ (for iOS 15+ deployment target)
- iOS 15.0+ device (tested on 15.8)
- TrollStore for sideloading (no Apple Developer account needed)

## License

MIT — free to use, modify, and distribute.
