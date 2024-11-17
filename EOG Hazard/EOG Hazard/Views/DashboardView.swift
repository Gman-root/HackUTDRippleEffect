// import SwiftUI

// struct DashboardView: View {
//     var body: some View {
//         GeometryReader { geometry in
//             ZStack {
//                 Color(UIColor.systemGray6)
//                     .edgesIgnoringSafeArea(.all)
                
//                 VStack(spacing: 20) {
//                     Spacer().frame(height: 50) // Add this line to push content down
                    
//                     Text("Welcome to the Dashboard!")
//                         .font(.largeTitle)
//                         .fontWeight(.bold)
//                         .foregroundColor(.white)
//                         .padding()
//                         .background(Color.blue)
//                         .cornerRadius(10)
                    
//                     HStack {
//                         VStack {
//                             Image(systemName: "chart.bar.fill")
//                                 .resizable()
//                                 .frame(width: 50, height: 50)
//                                 .foregroundColor(.blue)
//                             Text("Statistics")
//                                 .font(.headline)
//                         }
//                         .padding()
//                         .background(Color.white)
//                         .cornerRadius(10)
//                         .shadow(radius: 5)
                        
//                         VStack {
//                             Image(systemName: "bell.fill")
//                                 .resizable()
//                                 .frame(width: 50, height: 50)
//                                 .foregroundColor(.orange)
//                             Text("Notifications")
//                                 .font(.headline)
//                         }
//                         .padding()
//                         .background(Color.white)
//                         .cornerRadius(10)
//                         .shadow(radius: 5)
//                     }
                    
//                     Spacer()
//                 }
//                 .padding()
//                 .frame(width: geometry.size.width, height: geometry.size.height)
//             }
//         }
//         // .navigationBarTitle("Dashboard", displayMode: .inline)
//     }
// }

// struct DashboardView_Previews: PreviewProvider {
//     static var previews: some View {
//         DashboardView()
//     }
// }

import SwiftUI

struct DashboardView: View {
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                Color(UIColor.systemGray6)
                    .edgesIgnoringSafeArea(.all)
                
                VStack(spacing: 20) {
                    Spacer().frame(height: 50) // Add this line to push content down
                    
                    Text("Welcome to the Dashboard!")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                        .foregroundColor(.white)
                        .padding()
                        .background(Color.blue)
                        .cornerRadius(10)
                    
                    HStack {
                        NavigationLink(destination: StatisticsView()) {
                            VStack {
                                Image(systemName: "chart.bar.fill")
                                    .resizable()
                                    .frame(width: 50, height: 50)
                                    .foregroundColor(.blue)
                                Text("Statistics")
                                    .font(.headline)
                            }
                            .padding()
                            .background(Color.white)
                            .cornerRadius(10)
                            .shadow(radius: 5)
                        }
                        
                        NavigationLink(destination: NotificationsView()) {
                            VStack {
                                Image(systemName: "bell.fill")
                                    .resizable()
                                    .frame(width: 50, height: 50)
                                    .foregroundColor(.orange)
                                Text("Notifications")
                                    .font(.headline)
                            }
                            .padding()
                            .background(Color.white)
                            .cornerRadius(10)
                            .shadow(radius: 5)
                        }
                    }
                    
                    Spacer()
                }
                .padding()
                .frame(width: geometry.size.width, height: geometry.size.height)
            }
        }
        //.navigationBarTitle("Dashboard", displayMode: .inline)
    }
}

struct DashboardView_Previews: PreviewProvider {
    static var previews: some View {
        DashboardView()
    }
}
