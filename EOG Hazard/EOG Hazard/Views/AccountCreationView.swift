// import SwiftUI

// struct AccountCreationView: View {
//     @State private var username: String = ""
//     @State private var password: String = ""
//     @State private var confirmPassword: String = ""
//     @State private var message: String = ""
//     @State private var accountCreated: Bool = false

//     var body: some View {
//         NavigationView {
//             VStack {
//                 Spacer().frame(height: 50) // Add this line to bring the prompt down

//                 Text("Create Account")
//                     .font(.largeTitle)
//                     .fontWeight(.bold)
//                     .padding(.bottom, 40)
                
//                 VStack(alignment: .leading, spacing: 15) {
//                     TextField("Username", text: $username)
//                         .padding()
//                         .background(Color.white.opacity(0.8))
//                         .cornerRadius(5.0)
//                         .shadow(radius: 5)
                    
//                     SecureField("Password", text: $password)
//                         .padding()
//                         .background(Color.white.opacity(0.8))
//                         .cornerRadius(5.0)
//                         .shadow(radius: 5)
                    
//                     SecureField("Confirm Password", text: $confirmPassword)
//                         .padding()
//                         .background(Color.white.opacity(0.8))
//                         .cornerRadius(5.0)
//                         .shadow(radius: 5)
//                 }
//                 .padding(.horizontal, 20)
                
//                 Button(action: {
//                     handleCreateAccount()
//                 }) {
//                     Text("Create Account")
//                         .font(.headline)
//                         .foregroundColor(.white)
//                         .padding()
//                         .frame(width: 220, height: 60)
//                         .background(LinearGradient(gradient: Gradient(colors: [Color.blue, Color.purple]), startPoint: .leading, endPoint: .trailing))
//                         .cornerRadius(15.0)
//                         .shadow(radius: 10)
//                 }
//                 .padding(.top, 30)
                
//                 Text(message)
//                     .foregroundColor(.red)
//                     .padding(.top, 20)
                
//                 Spacer()
                
//                 NavigationLink(destination: ContentView(), isActive: $accountCreated) {
//                     EmptyView()
//                 }
//             }
//             .padding()
//             .background(LinearGradient(gradient: Gradient(colors: [Color.blue, Color.purple]), startPoint: .top, endPoint: .bottom))
//             .edgesIgnoringSafeArea(.all)
//         }
//     }
    
//     func handleCreateAccount() {
//         // Implement your account creation logic here
//         if username.isEmpty || password.isEmpty || confirmPassword.isEmpty {
//             message = "Please fill in all fields."
//         } else if password != confirmPassword {
//             message = "Passwords do not match."
//         } else {
//             // Assuming account creation is successful
//             message = "Account created successfully!"
//             accountCreated = true
//         }
//     }
// }

// struct AccountCreationView_Previews: PreviewProvider {
//     static var previews: some View {
//         AccountCreationView()
//     }
// }

import SwiftUI

struct AccountCreationView: View {
    @State private var username: String = ""
    @State private var password: String = ""
    @State private var confirmPassword: String = ""
    @State private var message: String = ""
    @Binding var appState: AppState

    var body: some View {
        VStack {
            Spacer().frame(height: 50) // Add this line to bring the prompt down

            Text("Create Account")
                .font(.largeTitle)
                .fontWeight(.bold)
                .padding(.bottom, 40)
            
            VStack(alignment: .leading, spacing: 15) {
                TextField("Username", text: $username)
                    .padding()
                    .background(Color.white.opacity(0.8))
                    .cornerRadius(5.0)
                    .shadow(radius: 5)
                
                SecureField("Password", text: $password)
                    .padding()
                    .background(Color.white.opacity(0.8))
                    .cornerRadius(5.0)
                    .shadow(radius: 5)
                
                SecureField("Confirm Password", text: $confirmPassword)
                    .padding()
                    .background(Color.white.opacity(0.8))
                    .cornerRadius(5.0)
                    .shadow(radius: 5)
            }
            .padding(.horizontal, 20)
            
            Button(action: {
                handleCreateAccount()
            }) {
                Text("Create Account")
                    .font(.headline)
                    .foregroundColor(.white)
                    .padding()
                    .frame(width: 220, height: 60)
                    .background(LinearGradient(gradient: Gradient(colors: [Color.blue, Color.purple]), startPoint: .leading, endPoint: .trailing))
                    .cornerRadius(15.0)
                    .shadow(radius: 10)
            }
            .padding(.top, 30)
            
            Text(message)
                .foregroundColor(.red)
                .padding(.top, 20)
            
            Spacer()
        }
        .padding()
        .background(LinearGradient(gradient: Gradient(colors: [Color.blue, Color.purple]), startPoint: .top, endPoint: .bottom))
        .edgesIgnoringSafeArea(.all)
    }
    
    func handleCreateAccount() {
        // Implement your account creation logic here
        if username.isEmpty || password.isEmpty || confirmPassword.isEmpty {
            message = "Please fill in all fields."
        } else if password != confirmPassword {
            message = "Passwords do not match."
        } else {
            // Assuming account creation is successful
            message = "Account created successfully!"
            DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
                appState = .login
            }
        }
    }
}

struct AccountCreationView_Previews: PreviewProvider {
    static var previews: some View {
        AccountCreationView(appState: .constant(.login))
    }
}