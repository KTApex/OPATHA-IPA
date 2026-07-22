import SwiftUI

/// Provides a set of mock photos for development. Swap `systemImageName` for a `url` property later.
extension PhotoItem {
    /// Returns an array of 24 placeholder photos using SF Symbols and varied colors.
    static let mockPhotos: [PhotoItem] = [
        PhotoItem(systemImageName: "photo", colorName: "blue"),
        PhotoItem(systemImageName: "photo.fill", colorName: "red"),
        PhotoItem(systemImageName: "camera", colorName: "green"),
        PhotoItem(systemImageName: "camera.fill", colorName: "orange"),
        PhotoItem(systemImageName: "sun.max", colorName: "yellow"),
        PhotoItem(systemImageName: "sun.max.fill", colorName: "pink"),
        PhotoItem(systemImageName: "moon", colorName: "purple"),
        PhotoItem(systemImageName: "moon.fill", colorName: "indigo"),
        PhotoItem(systemImageName: "star", colorName: "teal"),
        PhotoItem(systemImageName: "star.fill", colorName: "cyan"),
        PhotoItem(systemImageName: "heart", colorName: "mint"),
        PhotoItem(systemImageName: "heart.fill", colorName: "brown"),
        PhotoItem(systemImageName: "house", colorName: "gray"),
        PhotoItem(systemImageName: "house.fill", colorName: "blue"),
        PhotoItem(systemImageName: "gearshape", colorName: "red"),
        PhotoItem(systemImageName: "gearshape.fill", colorName: "green"),
        PhotoItem(systemImageName: "bell", colorName: "orange"),
        PhotoItem(systemImageName: "bell.fill", colorName: "yellow"),
        PhotoItem(systemImageName: "tag", colorName: "pink"),
        PhotoItem(systemImageName: "tag.fill", colorName: "purple"),
        PhotoItem(systemImageName: "bookmark", colorName: "indigo"),
        PhotoItem(systemImageName: "bookmark.fill", colorName: "teal"),
        PhotoItem(systemImageName: "flag", colorName: "cyan"),
        PhotoItem(systemImageName: "flag.fill", colorName: "mint"),
    ]
}
