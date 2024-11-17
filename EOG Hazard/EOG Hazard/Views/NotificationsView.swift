import SwiftUI

struct NotificationsView: View {
    var body: some View {
        VStack {
            Text("Notifications")
                .font(.largeTitle)
                .fontWeight(.bold)
                .padding()
            
            // Add your notifications content here
            
            Spacer()
        }
        .padding()
        // .navigationBarTitle("Notifications", displayMode: .inline)
    }
}

struct NotificationsView_Previews: PreviewProvider {
    static var previews: some View {
        NotificationsView()
    }
}
