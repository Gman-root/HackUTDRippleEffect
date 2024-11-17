// import SwiftUI

// enum AppState {
//     case login
//     case createAccount
//     case dashboard
// }

// struct ContentView: View {
//     @State private var username: String = ""
//     @State private var password: String = ""
//     @State private var loginMessage: String = ""
//     @State private var appState: AppState = .login
//     @State private var showDashboard: Bool = false

//     var body: some View {
//         NavigationView {
//             VStack {
//                 if appState == .login {
//                     loginView
//                 } else if appState == .createAccount {
//                     AccountCreationView(appState: $appState)
//                 } else if appState == .dashboard {
//                     DashboardView()
//                         .transition(.slide)
//                         .animation(.easeInOut(duration: 0.5))
//                 }
//             }
//             .padding()
//             .background(LinearGradient(gradient: Gradient(colors: [Color.blue, Color.purple]), startPoint: .top, endPoint: .bottom))
//             .edgesIgnoringSafeArea(.all)
//         }
//     }
    
//     var loginView: some View {
//         VStack {
//             // Top logo
//             Image("Eog hydrate logo")
//                 .resizable()
//                 .aspectRatio(contentMode: .fit)
//                 .frame(width: 100, height: 100)
//                 .clipShape(Circle())
//                 .overlay(Circle().stroke(Color.white, lineWidth: 4))
//                 .shadow(radius: 10)
//                 .padding(.top, 40)
            
//             Spacer()
            
//             Text("EOG Hazard")
//                 .font(.largeTitle)
//                 .fontWeight(.bold)
//                 .foregroundColor(.white)
//                 .padding(.bottom, 40)
            
//             Image(systemName: "person.circle")
//                 .resizable()
//                 .frame(width: 100, height: 100)
//                 .foregroundColor(.white)
//                 .padding(.bottom, 40)
            
//             VStack(alignment: .leading, spacing: 15) {
//                 TextField("Username", text: $username)
//                     .padding()
//                     .background(Color.white.opacity(0.8))
//                     .cornerRadius(5.0)
//                     .shadow(radius: 5)
                
//                 SecureField("Password", text: $password)
//                     .padding()
//                     .background(Color.white.opacity(0.8))
//                     .cornerRadius(5.0)
//                     .shadow(radius: 5)
//             }
//             .padding(.horizontal, 20)
            
//             Button(action: {
//                 handleLogin()
//             }) {
//                 Text("Login")
//                     .font(.headline)
//                     .foregroundColor(.white)
//                     .padding()
//                     .frame(width: 220, height: 60)
//                     .background(LinearGradient(gradient: Gradient(colors: [Color.blue, Color.purple]), startPoint: .leading, endPoint: .trailing))
//                     .cornerRadius(15.0)
//                     .shadow(radius: 10)
//             }
//             .padding(.top, 30)
            
//             Text(loginMessage)
//                 .foregroundColor(.red)
//                 .padding(.top, 20)
            
//             Button(action: {
//                 appState = .createAccount
//             }) {
//                 Text("Create Account")
//                     .foregroundColor(.white)
//                     .underline()
//                     .padding(.top, 20)
//             }
            
//             Spacer()
//         }
//     }
    
//     func handleLogin() {
//         // Implement your login logic here
//         if username.isEmpty || password.isEmpty {
//             loginMessage = "Please enter both username and password."
//         } else {
//             // Assuming login is successful
//             loginMessage = ""
//             withAnimation {
//                 appState = .dashboard
//             }
//         }
//     }
// }

// struct ContentView_Previews: PreviewProvider {
//     static var previews: some View {
//         ContentView()
//     }
// }

import SwiftUI

enum AppState {
    case login
    case createAccount
    case dashboard
}

struct ContentView: View {
    @State private var username: String = ""
    @State private var password: String = ""
    @State private var loginMessage: String = ""
    @State private var appState: AppState = .login

    var body: some View {
        NavigationView {
            VStack {
                if appState == .login {
                    loginView
                } else if appState == .createAccount {
                    AccountCreationView(appState: $appState)
                } else if appState == .dashboard {
                    DashboardView()
                }
            }
            .padding()
            .background(LinearGradient(gradient: Gradient(colors: [Color.blue, Color.purple]), startPoint: .top, endPoint: .bottom))
            .edgesIgnoringSafeArea(.all)
        }
    }
    
    var loginView: some View {
        VStack {
            // Top logo
            Image("Eog hydrate logo")
                .resizable()
                .aspectRatio(contentMode: .fit)
                .frame(width: 100, height: 100)
                .clipShape(Circle())
                .overlay(Circle().stroke(Color.white, lineWidth: 4))
                .shadow(radius: 10)
                .padding(.top, 40)
            
            Spacer()
            
            Text("EOG Hydrate")
                .font(.largeTitle)
                .fontWeight(.bold)
                .foregroundColor(.white)
                .padding(.bottom, 40)
            
            Image(systemName: "person.circle")
                .resizable()
                .frame(width: 100, height: 100)
                .foregroundColor(.white)
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
            }
            .padding(.horizontal, 20)
            
            Button(action: {
                handleLogin()
            }) {
                Text("Login")
                    .font(.headline)
                    .foregroundColor(.white)
                    .padding()
                    .frame(width: 220, height: 60)
                    .background(LinearGradient(gradient: Gradient(colors: [Color.blue, Color.purple]), startPoint: .leading, endPoint: .trailing))
                    .cornerRadius(15.0)
                    .shadow(radius: 10)
            }
            .padding(.top, 30)
            
            Text(loginMessage)
                .foregroundColor(.red)
                .padding(.top, 20)
            
            Button(action: {
                appState = .createAccount
            }) {
                Text("Create Account")
                    .foregroundColor(.white)
                    .underline()
                    .padding(.top, 20)
            }
            
            Spacer()
        }
    }
    
    func handleLogin() {
        // Implement your login logic here
        if username.isEmpty || password.isEmpty {
            loginMessage = "Please enter both username and password."
        } else {
            // Assuming login is successful
            loginMessage = ""
            appState = .dashboard
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
