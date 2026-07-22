import Foundation

/// Represents a single photo item. Replace the `systemImageName` with a real `url` when integrating actual images.
struct PhotoItem: Identifiable, Equatable {
    let id = UUID()
    let systemImageName: String  // SF Symbol name (placeholder)
    let colorName: String        // Color name for background (placeholder)
    let title: String?

    init(systemImageName: String, colorName: String = "gray", title: String? = nil) {
        self.systemImageName = systemImageName
        self.colorName = colorName
        self.title = title
    }
}
