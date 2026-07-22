import SwiftUI

/// Main grid view mimicking the iOS 15 Photos app "Photos" tab.
struct PhotosGridView: View {
    @StateObject private var viewModel = PhotosViewModel()
    @State private var selectedPhoto: PhotoItem?
    @State private var showSlideshowOptions = false

    private let columns = [
        GridItem(.flexible(), spacing: 1),
        GridItem(.flexible(), spacing: 1),
        GridItem(.flexible(), spacing: 1),
    ]

    var body: some View {
        NavigationView {
            ScrollView {
                LazyVGrid(columns: columns, spacing: 1) {
                    ForEach(viewModel.photos) { photo in
                        thumbnail(for: photo)
                            .aspectRatio(1, contentMode: .fill)
                            .clipped()
                            .onTapGesture {
                                selectedPhoto = photo
                            }
                    }
                }
                .padding(.horizontal, 0)
            }
            .navigationTitle("Photos")
            .navigationBarTitleDisplayMode(.large)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button {
                        showSlideshowOptions = true
                    } label: {
                        Image(systemName: "play.rectangle.fill")
                            .font(.title3)
                    }
                }
            }
            .background(Color.black)
            .sheet(item: $selectedPhoto) { photo in
                PhotoDetailView(
                    photo: photo,
                    allPhotos: viewModel.photos,
                    onStartSlideshow: { items in
                        viewModel.startSlideshow(with: items)
                        selectedPhoto = nil
                    }
                )
            }
            .sheet(isPresented: $showSlideshowOptions) {
                SlideshowOptionsView(
                    photos: viewModel.photos,
                    onStart: { options in
                        viewModel.startSlideshow(with: viewModel.photos)
                        showSlideshowOptions = false
                    }
                )
            }
            .fullScreenCover(isPresented: $viewModel.showSlideshow) {
                SlideshowView(photos: viewModel.slideshowPhotos) {
                    viewModel.stopSlideshow()
                }
            }
        }
        .navigationViewStyle(.stack)
    }

    @ViewBuilder
    private func thumbnail(for photo: PhotoItem) -> some View {
        ZStack {
            Color(photo.colorName)
            Image(systemName: photo.systemImageName)
                .font(.largeTitle)
                .foregroundColor(.white)
        }
    }
}

#Preview {
    PhotosGridView()
        .preferredColorScheme(.dark)
}
