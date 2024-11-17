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
        }
        .padding()
    }

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

    private func uploadCSV(data: Data) {
        guard let url = URL(string: serverURL) else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"

        let boundary = UUID().uuidString
        let contentType = "multipart/form-data; boundary=\(boundary)"
        request.setValue(contentType, forHTTPHeaderField: "Content-Type")

        var body = Data()
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"\(selectedFileName)\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: text/csv\r\n\r\n".data(using: .utf8)!)
        body.append(data)
        body.append("\r\n".data(using: .utf8)!)
        body.append("--\(boundary)--\r\n".data(using: .utf8)!)

        request.httpBody = body

        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                DispatchQueue.main.async {
                    self.errorMessage = "Upload failed: \(error.localizedDescription)"
                }
                return
            }

            guard let data = data else {
                DispatchQueue.main.async {
                    self.errorMessage = "No data received from server"
                }
                return
            }

            if let responseMessage = try? JSONDecoder().decode([String: String].self, from: data),
               let message = responseMessage["message"] {
                DispatchQueue.main.async {
                    if message.contains("Successfully cleaned and saved") {
                        self.successMessage = message
                    } else {
                        self.errorMessage = message
                    }
                }
            } else {
                DispatchQueue.main.async {
                    self.errorMessage = "Invalid response from server"
                }
            }
        }
        task.resume()
    }
}

struct UploadDataSet_Previews: PreviewProvider {
    static var previews: some View {
        UploadDataSet()
    }
}
