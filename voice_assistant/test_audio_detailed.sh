#!/bin/bash
echo "Testing different audio output methods..."

echo "1. Testing espeak directly:"
espeak "Testing direct espeak output"

echo "2. Testing espeak with analog output (3.5mm jack):"
amixer cset numid=3 1
espeak -a 200 "Testing analog output"

echo "3. Testing espeak through headphones card:"
espeak --stdout "Testing headphones card" | aplay -D plughw:1,0

echo "4. Testing espeak through ReSpeaker:"
espeak --stdout "Testing ReSpeaker output" | aplay -D plughw:3,0

echo "5. Check volume levels:"
amixer sget PCM
amixer sget Master

echo "6. Increase volume:"
amixer sset PCM 90%
amixer sset Master 90%

echo "7. Final test with increased volume:"
espeak -a 200 -s 150 "Testing with maximum volume"
