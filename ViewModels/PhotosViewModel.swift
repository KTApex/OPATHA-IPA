import SwiftUI

/// Main ViewModel for managing the photo library, selection, and navigation state.
@MainActor
final class PhotosViewModel: ObservableObject {
    @Published var photos: [PhotoItem] = PhotoItem.mockPhotos
    @Published var selectedPhoto: PhotoItem?
    @Published var showSlideshow = false
    @Published var slideshowPhotos: [PhotoItem] = []

    // MARK: - Selection for slideshow

    /// Start a slideshow with the currently visible/selected photos.
    func startSlideshow(with items: [PhotoItem]) {
        slideshowPhotos = items
        showSlideshow = true
    }

    /// Start a slideshow from a single photo (the album's photos would need to be passed separately).
    func startSlideshowFromDetail(photo: PhotoItem, allPhotos: [PhotoItem]) {
        slideshowPhotos = allPhotos
        if let index = allPhotos.firstIndex(of: photo) {
            // Reorder so the current photo is first
            var reordered = allPhotos
            let item = reordered.remove(at: index)
            reordered.insert(item, at: 0)
            slideshowPhotos = reordered
        }
        showSlideshow = true
    }

    func stopSlideshow() {
        showSlideshow = false
        slideshowPhotos = []
    }
}
