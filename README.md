Welcome to my own Jarvis Assistant

This was built using Python and Tkinter

This app is in very early stages of development and is very experimental so dont
expect everything to work perfectly.

## Download

You can download the latest version of Jarvis from the [Releases](https://github.com/YOUR_USERNAME/YOUR_REPO/releases) page.

Alternatively, visit the [GitHub Pages site](https://YOUR_USERNAME.github.io/YOUR_REPO/) for a simple download interface.

## What Jarvis can do

- Launch programs and applications
- Run Steam games
- Set timers
- Check for and install updates automatically

Update System

The application includes an automatic update system that allows it to stay current with the latest changes.

How Updates Work

1. **Version Checking**: The app checks a remote version.json file to see if a newer version is available
2. **Download**: If an update is found, it downloads the latest installer
3. **Installation**: The installer runs silently to update the application

Commands

- `update` or `check for updates` - Check for and install updates
- `version` - Show current version

Setting Up Updates

To enable updates, you need to:

1. Host the `version.json` file on a web server (GitHub, your website, etc.)
2. Update the `UPDATE_URL` in `Jarvis.py` to point to your version.json file
3. Host the installer executable and update `UPDATE_DOWNLOAD_URL` in `Jarvis.py`
4. Update the version number in both `Jarvis.py` and `version.json` when releasing new versions

Building

1. Run `build_exe.bat` to create the executable
2. Run `build_installer.bat` to create the installer

### Version Management

Use `update_version.bat` to update the version number and changelog:

```
update_version.bat 1.1.0 "Added new features and bug fixes"
```

This will update both `version.json` and `Jarvis.py` with the new version information.

Version History

- 1.0.0: Initial release with basic functionality (some point I want to incorperate AI into it but that will be for a later point)