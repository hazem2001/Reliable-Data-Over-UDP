# Reliable Data Transfer over UDP

A Python implementation of a custom reliable data transfer protocol built on top of UDP. Includes a sender and receiver that support retransmissions, timeout handling, buffering, and in-order file reconstruction over an unreliable network emulator.

## What I Implemented
- **sender.py** — full sender logic (managing timeouts, retransmissions, window behavior, and EOT handling)
- **receiver.py** — buffering, ACK handling, in-order delivery, and arrival logging
- Complete reliable transfer flow on top of UDP, handling loss, duplication, and reordering

## Provided by Course
- **packet.py** — packet serialization/deserialization helper
- **network emulator** — simulates delay, loss, and reordering

## Usage
```bash
python receiver.py <emulator_host> <ack_port> <recv_port> <buffer_size> <output_file>
python sender.py <emulator_host> <send_port> <ack_port> <timeout_ms> <window_max> <input_file>
