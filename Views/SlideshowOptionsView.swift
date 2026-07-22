import SwiftUI

/// A sheet presented from the grid view to configure and start a slideshow.
struct SlideshowOptionsView: View {
    let photos: [PhotoItem]
    let onStart: (SlideshowOptions) -> Void

    @State private var options = SlideshowOptions()
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationView {
            Form {
                Section("Transition Style") {
                    Picker("Style", selection: $options.transition) {
                        ForEach(SlideshowOptions.TransitionStyle.allCases) { style in
                            Text(style.rawValue.capitalized)
                                .tag(style)
                        }
                    }
                    .pickerStyle(.menu)
                }

                Section("Speed") {
                    Picker("Seconds per photo", selection: $options.speed) {
                        ForEach(SlideshowOptions.speedOptions, id: \.self) { speed in
                            Text("\(Int(speed))s").tag(speed)
                        }
                    }
                    .pickerStyle(.segmented)
                }

                Section {
                    Toggle("Loop Slideshow", isOn: $options.loopEnabled)
                    Toggle("Shuffle Order", isOn: $options.shuffleEnabled)
                }

                Section {
                    Button("Start Slideshow") {
                        onStart(options)
                        dismiss()
                    }
                    .font(.headline)
                    .frame(maxWidth: .infinity)
                    .foregroundColor(.white)
                    .listRowBackground(Color.blue)
                }
            }
            .navigationTitle("Slideshow Options")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                }
            }
        }
    }
}

#Preview {
    SlideshowOptionsView(photos: PhotoItem.mockPhotos, onStart: { _ in })
}
