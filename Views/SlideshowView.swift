import SwiftUI

/// Full-screen slideshow player with animated transitions.
struct SlideshowView: View {
    let photos: [PhotoItem]
    let onDismiss: () -> Void

    @StateObject private var viewModel = SlideshowViewModel()
    @State private var showOptions = false

    /// Used to force transition triggers.
    @State private var transitionTrigger = false

    var body: some View {
        ZStack {
            Color.black.ignoresSafeArea()

            if let current = viewModel.currentPhotoRespectingShuffle() {
                photoContent(current)
                    .id(current.id)
                    .transition(currentTransition)
                    .animation(.easeInOut(duration: 0.5), value: transitionTrigger)
            } else {
                Text("No photos")
                    .foregroundColor(.white)
            }

            // Overlay controls
            VStack {
                Spacer()
                controlsBar
            }
            .padding(.bottom, 40)
        }
        .onAppear {
            viewModel.loadPhotos(photos)
            viewModel.play()
        }
        .onDisappear {
            viewModel.stop()
        }
        .onChange(of: viewModel.currentIndex) { _ in
            transitionTrigger.toggle()
        }
        .sheet(isPresented: $showOptions) {
            optionsSheet
        }
        .statusBar(hidden: true)
    }

    // MARK: - Photo Content

    @ViewBuilder
    private func photoContent(_ photo: PhotoItem) -> some View {
        ZStack {
            Color(photo.colorName)
            Image(systemName: photo.systemImageName)
                .font(.system(size: 120))
                .foregroundColor(.white)
        }
        .aspectRatio(contentMode: .fit)
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .padding(40)
    }

    // MARK: - Transition

    private var currentTransition: AnyTransition {
        switch viewModel.options.transition {
        case .fade:
            return .opacity
        case .slide:
            return .asymmetric(
                insertion: .move(edge: .trailing),
                removal: .move(edge: .leading)
            )
        case .zoom:
            return .scale(scale: 0.2).combined(with: .opacity)
        case .flip:
            return .asymmetric(
                insertion: .rotation3D(
                    angle: .degrees(90),
                    axis: (x: 0, y: 1, z: 0),
                    anchor: .center,
                    anchorZ: 0,
                    perspective: 0.3
                ),
                removal: .opacity
            )
        case .blur:
            return .opacity // We handle blur via a modifier
        case .pageCurl:
            return .asymmetric(
                insertion: .move(edge: .trailing).combined(with: .opacity),
                removal: .move(edge: .leading).combined(with: .opacity)
            )
        case .wipe:
            return .asymmetric(
                insertion: .move(edge: .bottom),
                removal: .move(edge: .top)
            )
        case .none:
            return .identity
        }
    }

    // MARK: - Controls

    private var controlsBar: some View {
        HStack(spacing: 40) {
            Button {
                viewModel.previousPhoto()
            } label: {
                Image(systemName: "backward.fill")
                    .font(.title2)
                    .foregroundColor(.white)
            }

            Button {
                viewModel.isPlaying ? viewModel.pause() : viewModel.play()
            } label: {
                Image(systemName: viewModel.isPlaying ? "pause.fill" : "play.fill")
                    .font(.largeTitle)
                    .foregroundColor(.white)
            }

            Button {
                viewModel.nextPhoto()
            } label: {
                Image(systemName: "forward.fill")
                    .font(.title2)
                    .foregroundColor(.white)
            }

            Button {
                showOptions = true
            } label: {
                Image(systemName: "gearshape.fill")
                    .font(.title2)
                    .foregroundColor(.white)
            }

            Button {
                viewModel.stop()
                onDismiss()
            } label: {
                Image(systemName: "xmark.circle.fill")
                    .font(.title2)
                    .foregroundColor(.white)
            }
        }
        .padding()
        .background(Color.black.opacity(0.5))
        .clipShape(Capsule())
    }

    // MARK: - Options Sheet

    private var optionsSheet: some View {
        NavigationView {
            Form {
                Section("Transition Style") {
                    Picker("Style", selection: $viewModel.options.transition) {
                        ForEach(SlideshowOptions.TransitionStyle.allCases) { style in
                            Text(style.rawValue.capitalized)
                                .tag(style)
                        }
                    }
                    .pickerStyle(.menu)
                }

                Section("Speed") {
                    Picker("Seconds per photo", selection: $viewModel.options.speed) {
                        ForEach(SlideshowOptions.speedOptions, id: \.self) { speed in
                            Text("\(Int(speed))s").tag(speed)
                        }
                    }
                    .pickerStyle(.segmented)
                }

                Section {
                    Toggle("Loop Slideshow", isOn: $viewModel.options.loopEnabled)
                    Toggle("Shuffle Order", isOn: $viewModel.options.shuffleEnabled)
                }
            }
            .navigationTitle("Slideshow Options")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") {
                        // Reload photos with new shuffle setting
                        viewModel.loadPhotos(photos)
                        if viewModel.isPlaying {
                            viewModel.play()
                        }
                        showOptions = false
                    }
                }
            }
        }
    }
}

#Preview {
    SlideshowView(photos: PhotoItem.mockPhotos, onDismiss: {})
        .preferredColorScheme(.dark)
}
