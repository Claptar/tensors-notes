// Render a URL with WebKit, the engine Safari uses, in a light or dark appearance; save a PNG.
// Used by snap_svg.py (compiled once with swiftc into a cache folder). Safari is the strictest of
// the browsers about SVG features, so it is the one figures are checked in.
// usage: webkit_snap <url> <out.png> <light|dark> [width] [height] [wait-seconds]
import Cocoa
import WebKit

let args = CommandLine.arguments
guard args.count >= 4, let url = URL(string: args[1]) else {
    print("usage: webkit_snap <url> <out.png> <light|dark> [width] [height] [wait-seconds]"); exit(2)
}
let out = args[2]
let dark = args[3] == "dark"
let width = args.count > 4 ? Double(args[4])! : 1280
let height = args.count > 5 ? Double(args[5])! : 2000
let wait = args.count > 6 ? Double(args[6])! : 4.0   // time for page scripts to finish rendering

final class Delegate: NSObject, WKNavigationDelegate {
    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        // Give page scripts (e.g. the website reader) time to fetch and render.
        DispatchQueue.main.asyncAfter(deadline: .now() + wait) {
            webView.takeSnapshot(with: WKSnapshotConfiguration()) { image, error in
                guard let image = image, let tiff = image.tiffRepresentation,
                      let rep = NSBitmapImageRep(data: tiff),
                      let png = rep.representation(using: .png, properties: [:]) else {
                    print("snapshot failed: \(String(describing: error))"); exit(1)
                }
                try! png.write(to: URL(fileURLWithPath: out))
                print(out); exit(0)
            }
        }
    }
    func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
        print("load failed: \(error)"); exit(1)
    }
}

let app = NSApplication.shared
app.setActivationPolicy(.prohibited)
let appearance = NSAppearance(named: dark ? .darkAqua : .aqua)
app.appearance = appearance
let config = WKWebViewConfiguration()
config.preferences.setValue(true, forKey: "allowFileAccessFromFileURLs")
let webView = WKWebView(frame: NSRect(x: 0, y: 0, width: width, height: height), configuration: config)
webView.appearance = appearance
let delegate = Delegate()
webView.navigationDelegate = delegate
let window = NSWindow(contentRect: webView.frame, styleMask: [.borderless], backing: .buffered, defer: false)
window.appearance = appearance
window.contentView = webView
if url.isFileURL {
    webView.loadFileURL(url, allowingReadAccessTo: URL(fileURLWithPath: "/"))
} else {
    webView.load(URLRequest(url: url, cachePolicy: .reloadIgnoringLocalAndRemoteCacheData))
}
DispatchQueue.main.asyncAfter(deadline: .now() + 40) { print("timeout"); exit(1) }
app.run()
