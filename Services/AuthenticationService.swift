import LocalAuthentication
import SwiftUI

/// Manages Face ID / Touch ID / Passcode authentication using LocalAuthentication.
@MainActor
final class AuthenticationService: ObservableObject {
    @Published var isUnlocked = false
    @Published var showAlert = false
    @Published var alertMessage = ""

    private var context = LAContext()

    /// Call on app launch or scene phase change to .active.
    func authenticate() {
        context = LAContext()
        context.localizedFallbackTitle = "Enter Passcode"

        var error: NSError?
        let canEvaluate = context.canEvaluatePolicy(
            .deviceOwnerAuthentication,
            error: &error
        )

        guard canEvaluate else {
            alertMessage = "No Face ID / Touch ID or Passcode configured on this device."
            showAlert = true
            isUnlocked = true // fall back to allow access
            return
        }

        context.evaluatePolicy(
            .deviceOwnerAuthentication,
            localizedReason: "Unlock Photos to view your images."
        ) { [weak self] success, evalError in
            Task { @MainActor in
                if success {
                    self?.isUnlocked = true
                } else {
                    self?.alertMessage = evalError?.localizedDescription ?? "Authentication failed."
                    self?.showAlert = true
                }
            }
        }
    }

    func lock() {
        isUnlocked = false
    }
}
