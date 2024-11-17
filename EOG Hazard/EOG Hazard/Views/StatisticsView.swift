//  import SwiftUI

//  struct StatisticsView: View {
//      var body: some View {
//          VStack {
//              Text("Statistics")
//                  .font(.largeTitle)
//                  .fontWeight(.bold)
//                  .padding()
            
//              // Add your statistics content here


//              Spacer()
//          }
//          .padding()
//          //.navigationBarTitle("Statistics", displayMode: .inline)
//      }
//  }

//  struct StatisticsView_Previews: PreviewProvider {
//      static var previews: some View {
//          StatisticsView()
//      }
//  }
import SwiftUI
import WebKit

struct StatisticsView: View {
    var body: some View {
        ScrollView {
            VStack {
                Text("Statistics")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                    .padding()
                
                ForEach(1..<9) { index in
                    VStack {
                        ZoomableImage(imageName: "graph\(index)")
                            .frame(height: 200)
                            .padding()
                            .background(Color.white)
                            .cornerRadius(10)
                            .shadow(radius: 5)
                        
                        Text("The statistical hydrate detection in graph \(index)")
                            .font(.subheadline)
                            .padding(.top, 8)
                    }
                    .padding(.bottom, 16)
                }
                
                Spacer()
            }
            .padding()
        }
        //.navigationBarTitle("Statistics", displayMode: .inline)
    }
}

struct ZoomableImage: UIViewRepresentable {
    let imageName: String

    func makeUIView(context: Context) -> UIScrollView {
        let scrollView = UIScrollView()
        scrollView.minimumZoomScale = 1.0
        scrollView.maximumZoomScale = 5.0
        scrollView.delegate = context.coordinator

        let imageView = UIImageView(image: UIImage(named: imageName))
        imageView.contentMode = .scaleAspectFit
        imageView.frame = scrollView.bounds
        imageView.autoresizingMask = [.flexibleWidth, .flexibleHeight]

        scrollView.addSubview(imageView)
        return scrollView
    }

    func updateUIView(_ uiView: UIScrollView, context: Context) {
        if let imageView = uiView.subviews.first as? UIImageView {
            imageView.image = UIImage(named: imageName)
        }
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject, UIScrollViewDelegate {
        var parent: ZoomableImage

        init(_ parent: ZoomableImage) {
            self.parent = parent
        }

        func viewForZooming(in scrollView: UIScrollView) -> UIView? {
            return scrollView.subviews.first
        }
    }
}

struct WebView: UIViewRepresentable {
    let url: URL

    func makeUIView(context: Context) -> WKWebView {
        return WKWebView()
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {
        let request = URLRequest(url: url)
        uiView.load(request)
    }
}

struct StatisticsView_Previews: PreviewProvider {
    static var previews: some View {
        StatisticsView()
    }
}

//import SwiftUI
//import Foundation
//
//
//struct StatisticsView: View {
//    @State private var dataRows: [DataRow] = [] // Holds parsed CSV data
//    
//    var body: some View {
//        VStack {
//            Text("Statistics")
//                .font(.largeTitle)
//                .fontWeight(.bold)
//                .padding()
//            
//            if dataRows.isEmpty {
//                Text("Loading data...")
//                    .onAppear {
//                        dataRows = parseCSV() // Parse the CSV file
//                    }
//            } else {
//                LineChartView(dataRows: dataRows) // Add the graph here
//                    .frame(height: 400) // Adjust the size as needed
//                    .padding()
//            }
//            
//            Spacer()
//        }
//        .padding()
//        //.navigationBarTitle("Statistics", displayMode: .inline)
//    }
//}
//
//struct StatisticsView_Previews: PreviewProvider {
//    static var previews: some View {
//        StatisticsView()
//    }
//}

