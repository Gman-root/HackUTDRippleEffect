import SwiftUI
import UniformTypeIdentifiers
import UIKit

struct UploadDataSet: View {
    @State private var isImporting: Bool = false
    @State private var csvContent: String = ""
    @State private var errorMessage: String?
    @State private var selectedFileName: String = ""
    @State private var successMessage: String?

    let serverURL = "http://127.0.0.1:5000/upload_csv" // Update with your hostname address

    var body: some View {
        VStack(spacing: 20) {
            Button(action: {
                isImporting = true
            }) {
                Text("Upload CSV File")
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(8)
            }
            .fileImporter(
                isPresented: $isImporting,
                allowedContentTypes: [UTType.commaSeparatedText],
                allowsMultipleSelection: false
            ) { result in
                handleFileImport(result: result)
            }

            if isUploading {
                ProgressView("Uploading...")
                    .padding()
            }

            if let errorMessage = errorMessage {
                Text(errorMessage)
                    .foregroundColor(.red)
                    .padding()
            }

            if let successMessage = successMessage {
                Text(successMessage)
                    .foregroundColor(.green)
                    .padding()
            }

            if !selectedFileName.isEmpty {
                Text("Selected File: \(selectedFileName)")
                    .padding()
            }

            TextEditor(text: $csvContent)
                .padding()
                .border(Color.gray, width: 1)
                .frame(minHeight: 300)
                .frame(minHeight: 300)
        }
        .padding()
    }

    // Handle file import from the file picker
    private func handleFileImport(result: Result<[URL], Error>) {
        do {
            guard let selectedFile = try result.get().first else { return }
            selectedFileName = selectedFile.lastPathComponent
            if selectedFile.startAccessingSecurityScopedResource() {
                defer { selectedFile.stopAccessingSecurityScopedResource() }

                let data = try Data(contentsOf: selectedFile)
                csvContent = String(data: data, encoding: .utf8) ?? "Unable to read file"

                // Replace null values with the mean of the respective column
                var rows = csvContent.split(separator: "\n").map { $0.split(separator: ",") }
                let columnCount = rows.first?.count ?? 0
                var columnSums = [Double](repeating: 0.0, count: columnCount)
                var columnCounts = [Int](repeating: 0, count: columnCount)

                for row in rows {
                    for (index, value) in row.enumerated() {
                        if let doubleValue = Double(value) {
                            columnSums[index] += doubleValue
                            columnCounts[index] += 1
                        }
                    }
                }

                let columnMeans = columnSums.enumerated().map { $0.element / Double(columnCounts[$0.offset]) }

                for i in 0..<rows.count {
                    for j in 0..<rows[i].count {
                        if rows[i][j].isEmpty {
                            rows[i][j] = Substring(String(columnMeans[j]))
                        }
                    }
                }

                csvContent = rows.map { $0.joined(separator: ",") }.joined(separator: "\n")

                // Upload the CSV file
                uploadCSV(data: Data(csvContent.utf8))
            }
        } catch {
            errorMessage = "Error reading file: \(error.localizedDescription)"
        }
    }

    // Function to upload CSV data to the Flask server
    private func uploadCSV(data: Data) {
        guard let url = URL(string: serverURL) else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        // Set the Content-Type for multipart form-data
        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        // Prepare multipart form data
        let body = createMultipartFormData(data: data, boundary: boundary)
        request.httpBody = body

        isUploading = true  // Start showing upload indicator

        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            DispatchQueue.main.async {
                self.isUploading = false  // Hide upload indicator

                if let error = error {
                    self.errorMessage = "Upload failed: \(error.localizedDescription)"
                    return
                }

                guard let data = data else {
                    self.errorMessage = "No data received from server"
                    return
                }

                // Decode the JSON response from the server
                if let responseMessage = try? JSONDecoder().decode([String: String].self, from: data),
                   let message = responseMessage["message"] {
                    if message.contains("Successfully cleaned and saved") {
                        self.successMessage = message
                    } else {
                        self.errorMessage = message
                    }
                } else {
                    self.errorMessage = "Invalid response from server"
                }
            }
        }
        task.resume()
    }

    // Helper function to create multipart form-data body
    private func createMultipartFormData(data: Data, boundary: String) -> Data {
        var body = Data()

        // Add file data to request
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"\(selectedFileName)\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: text/csv\r\n\r\n".data(using: .utf8)!)
        body.append(data)
        body.append("\r\n".data(using: .utf8)!)
        body.append("--\(boundary)--\r\n".data(using: .utf8)!)

        return body
    }
}

struct UploadDataSet_Previews: PreviewProvider {
    static var previews: some View {
        UploadDataSet()
    }
}

