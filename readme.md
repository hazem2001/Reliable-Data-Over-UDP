# Reliable Data Transfer over UDP

A Python implementation of a **custom reliable data transfer protocol** built on top of UDP. Includes a sender and receiver with sliding-window transmission, retransmission on timeout, and in-order packet reconstruction.

## What I Implemented
- **sender.py** — full sender logic (windowing, timeouts, retransmissions, EOT)
- **receiver.py** — buffering, ACK generation, in-order delivery, logging
- Complete reliable transfer logic handling loss, duplication, and reordering

## Provided by Course
- **packet.py** — packet serialization/deserialization helper
- **network emulator** — simulates loss, delay, and reordering

## Features
- Custom packet format (DATA, ACK, EOT)
- Sliding-window flow control with adaptive behavior
- Buffered, in-order packet reconstruction
- Compatible with emulator for testing

## Run
```bash
python receiver.py <emulator_host> <ack_port> <recv_port> <buffer_size> <output_file>
python sender.py <emulator_host> <send_port> <ack_port> <timeout_ms> <window_max> <input_file>
