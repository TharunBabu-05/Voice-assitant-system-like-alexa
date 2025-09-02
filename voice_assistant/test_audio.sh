#!/bin/bash
# Script to test and configure audio output on Raspberry Pi

echo "Testing audio output devices..."

# List audio output devices
echo "Available audio output devices:"
aplay -l

echo ""
echo "Testing audio output with a test sound..."

# Test different audio outputs
echo "Testing analog output (3.5mm jack):"
amixer cset numid=3 1  # Force analog output
speaker-test -t sine -f 440 -c 2 -l 1 -s 1

echo ""
echo "Testing HDMI output:"
amixer cset numid=3 2  # Force HDMI output
speaker-test -t sine -f 440 -c 2 -l 1 -s 1

echo ""
echo "Testing with espeak directly:"
espeak "Hello, this is a test of the audio system"

echo ""
echo "Current audio configuration:"
amixer cget numid=3
