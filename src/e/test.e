name: Test Plugin
id: bm.enderzombi102.jsrefactor
desc: Polyfills for BM's CEF widgets
authors:
	ENDERZOMBI102
entrypoints:
	main: self.src.main
	event: self.src.event
dependencies:
	.Package:
		name: Pillow
		version: 1.7.0
		optional: false
	.Plugin:
		id: bm.enderzombi102.jsengine
		url: github.com/ENDERZOMBI102/plugins$jsengine
		version: 1.0.0+build.24