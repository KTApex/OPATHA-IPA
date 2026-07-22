import SwiftUI

/// Full-screen detail view for a single photo, with a toolbar button to start a slideshow.
struct PhotoDetailView: View {
    let photo: PhotoItem
    let allPhotos: [PhotoItem]
    let onStartSlideshow: ([PhotoItem]) -> Void

    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationView {
            ZStack {
                Color.black.ignoresSafeArea()

                placeholderImage(for: photo)
                    .aspectRatio(contentMode: .fit)
                    .padding()
            }
            .navigationTitle(photo.title ?? "Photo")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Close") { dismiss() }
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button {
                        onStartSlideshow(allPhotos)
                        dismiss()
                    } label: {
                        Label("Play Slideshow", systemImage: "play.rectangle.fill")
                    }
                }
            }
        }
    }

    @ViewBuilder
    private func placeholderImage(for photo: PhotoItem) -> some View {
        ZStack {
            Color(photo.colorName)
            Image(systemName: photo.systemImageName)
                .font(.system(size: 80))
                .foregroundColor(.white)
        }
        .clipShape(RoundedRectangle(cornerRadius: 16))
    }
}
