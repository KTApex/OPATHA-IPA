import SwiftUI

@main
struct PhotosApp: App {
    @StateObject private var authService = AuthenticationService()

    @Environment(\.scenePhase) private var scenePhase

    var body: some Scene {
        WindowGroup {
            ZStack {
                if authService.isUnlocked {
                    PhotosGridView()
                        .transition(.opacity)
                } else {
                    LockScreenView {
                        authService.authenticate()
                    }
                    .transition(.opacity)
                }
            }
            .animation(.easeInOut(duration: 0.3), value: authService.isUnlocked)
            .onAppear {
                authService.authenticate()
            }
            .onChange(of: scenePhase) { newPhase in
                switch newPhase {
                case .active:
                    if !authService.isUnlocked {
                        authService.authenticate()
                    }
                case .background, .inactive:
                    authService.lock()
                @unknown default:
                    break
                }
            }
            .alert("Authentication", isPresented: $authService.showAlert) {
                Button("OK", role: .cancel) { }
                Button("Try Again") { authService.authenticate() }
            } message: {
                Text(authService.alertMessage)
            }
        }
    }
}
