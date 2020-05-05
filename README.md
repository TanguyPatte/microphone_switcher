# Microphone switcher

## Purpose

The purpose of this code is to provide an app that display a microphone icon in the top bar of gnome shell to indicate if microphone is recording.
It is usefull when you have a lot of online meeting.

## Usage

Start the script on the opening of your user session by running `gnome-session-properties`.
Configure a shortcut to call the app function to switch microphone status :
`dbus-send --session --type=method_call --dest=org.tanguy.microphone_status /org/tanguy/microphone_status org.tanguy.microphone_status.capture_toogler`
