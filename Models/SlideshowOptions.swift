import Foundation

/// All configurable slideshow options.
struct SlideshowOptions: Equatable {
    var transition: TransitionStyle = .fade
    var speed: TimeInterval = 3.0
    var loopEnabled = true
    var shuffleEnabled = false

    enum TransitionStyle: String, CaseIterable, Identifiable {
        case fade
        case slide
        case zoom
        case flip
        case blur
        case pageCurl = "Page Curl"
        case wipe
        case none

        var id: String { rawValue }
    }

    /// Returns the display-friendly name for each speed option.
    static let speedOptions: [TimeInterval] = [2, 3, 5, 10, 15, 30]
}
