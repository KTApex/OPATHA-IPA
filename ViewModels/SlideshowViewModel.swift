import SwiftUI
import Combine

/// Manages the active slideshow state, timer, and transitions.
@MainActor
final class SlideshowViewModel: ObservableObject {
    @Published var options: SlideshowOptions = .init()
    @Published var currentIndex = 0
    @Published var isPlaying = false

    /// The current photo being displayed.
    var currentPhoto: PhotoItem? {
        guard !photos.isEmpty else { return nil }
        return photos[currentIndex]
    }

    private var photos: [PhotoItem] = []
    private var shuffledIndices: [Int] = []
    private var timer: Timer?

    // MARK: - Public API

    func loadPhotos(_ items: [PhotoItem]) {
        photos = items
        shuffledIndices = Array(0..<photos.count)
        if options.shuffleEnabled {
            shuffledIndices.shuffle()
        }
        currentIndex = 0
    }

    func play() {
        isPlaying = true
        startTimer()
    }

    func pause() {
        isPlaying = false
        stopTimer()
    }

    func stop() {
        isPlaying = false
        stopTimer()
        currentIndex = 0
    }

    func nextPhoto() {
        guard !photos.isEmpty else { return }

        let count = options.shuffleEnabled ? shuffledIndices.count : photos.count

        if currentIndex + 1 < count {
            currentIndex += 1
        } else if options.loopEnabled {
            currentIndex = 0
            if options.shuffleEnabled {
                shuffledIndices.shuffle()
            }
        } else {
            // Reached the end — stop
            pause()
        }
    }

    func previousPhoto() {
        guard !photos.isEmpty else { return }

        if currentIndex > 0 {
            currentIndex -= 1
        } else if options.loopEnabled {
            let count = options.shuffleEnabled ? shuffledIndices.count : photos.count
            currentIndex = count - 1
        }
    }

    /// Returns the actual PhotoItem at the given logical index (applying shuffle if enabled).
    func photoAtIndex(_ index: Int) -> PhotoItem {
        if options.shuffleEnabled {
            return photos[shuffledIndices[index]]
        }
        return photos[index]
    }

    /// Returns the current photo, respecting shuffle.
    func currentPhotoRespectingShuffle() -> PhotoItem? {
        guard !photos.isEmpty else { return nil }
        return photoAtIndex(currentIndex)
    }

    /// The total number of photos in this slideshow run.
    var photoCount: Int {
        options.shuffleEnabled ? shuffledIndices.count : photos.count
    }

    // MARK: - Timer

    private func startTimer() {
        stopTimer()
        timer = Timer.scheduledTimer(withTimeInterval: options.speed, repeats: true) { [weak self] _ in
            Task { @MainActor in
                self?.nextPhoto()
            }
        }
    }

    private func stopTimer() {
        timer?.invalidate()
        timer = nil
    }

    deinit {
        stopTimer()
    }
}
