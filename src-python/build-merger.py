import PyInstaller.__main__

PyInstaller.__main__.run([
    './src/merger.py',
    '--onefile',
    '--name=merger-x86_64-pc-windows-msvc.exe',
])
